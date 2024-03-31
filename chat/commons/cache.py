# from momento import simple_cache_client as momento_client
from datetime import timedelta
import pickle
import re
from momento import CacheClient, Configurations, CredentialProvider
from momento.responses import CacheGet, CacheSet, CacheIncrement, DeleteCache

from django.core.cache.backends.base import DEFAULT_TIMEOUT, BaseCache
from django.utils.functional import cached_property
from django.utils.module_loading import import_string


class MomentoSerializer:
    def __init__(self, protocol=None):
        self.protocol = pickle.HIGHEST_PROTOCOL if protocol is None else protocol

    def dumps(self, obj):
        # Only skip pickling for integers, a int subclasses as bool should be
        # pickled.
        if isinstance(obj, int):
            return obj
        return pickle.dumps(obj, self.protocol)

    def loads(self, data):
        try:
            return int(data)
        except ValueError:
            return pickle.loads(data)


class MomentoCacheClient:
    def __init__(
        self,
        cache_name,
        serializer=None,
        **options,
    ):
        import momento

        self._lib = momento
        self._cache_name = cache_name

        momento_auth_token = CredentialProvider.from_environment_variable(
            "MOMENTO_API_KEY"
        )
        ttl = timedelta(seconds=options.get("default_ttl_seconds", 600))
        config = {
            "configuration": Configurations.Laptop.v1(),
            "credential_provider": momento_auth_token,
            "default_ttl": ttl,
        }
        self._client = CacheClient.create(**config)

        if isinstance(serializer, str):
            serializer = import_string(serializer)
        if callable(serializer):
            serializer = serializer()
        self._serializer = serializer or MomentoSerializer()

    def get(self, key, default=None):
        resp = self._client.get(self._cache_name, key)
        match resp:
            case CacheGet.Hit():
                return self._serializer.loads(resp.value_string)
            case _:
                return default

    def set(self, key, value, timeout=None):
        resp = self._client.set(
            self._cache_name, key, self._serializer.dumps(value), timeout
        )
        match resp:
            case CacheSet.Success():
                return True
            case _:
                return False

    def delete(self, key):
        resp = self._client.delete(self._cache_name, key)
        match resp:
            case DeleteCache.Success():
                return True
            case _:
                return False

    def get_many(self, keys):
        values = [self._client.get(self._cache_name, key) for key in keys]
        return {
            key: self._serializer.loads(value.value_string)
            for key, value in zip(keys, values)
            if isinstance(value, CacheGet.Hit)
        }

    def set_many(self, data, timeout=None):
        items = {k: self._serializer.dumps(v) for k, v in data.items()}
        return all(self.set(key, value, timeout) for key, value in items.items())

    def incr(self, key, delta=1):
        resp = self._client.increment(self._cache_name, key, delta)
        match resp:
            case CacheIncrement.Success():
                return resp.value
            case _:
                raise ValueError(f"Key '{key}' not found.")

    def has_key(self, key):
        resp = self._client.get(self._cache_name, key)
        match resp:
            case CacheGet.Hit():
                return True
            case _:
                return False

    def delete_many(self, keys):
        for key in keys:
            self._client.delete(self._cache_name, key)

    def touch(self, key, timeout):
        resp = self._client.set(self._cache_name, key, self.get(key), timeout)
        match resp:
            case CacheSet.Success():
                return True
            case _:
                return False

    def clear(self):
        resp = self._client.flush_cache(self._cache_name)
        match resp:
            case DeleteCache.Success():
                return True
            case _:
                return False


class MomentoCache(BaseCache):
    def __init__(self, server, params):
        super().__init__(params)
        if isinstance(server, str):
            self._servers = re.split("[;,]", server)
        else:
            self._servers = server

        self._class = MomentoCacheClient
        self._options = params.get("OPTIONS", {})

    @cached_property
    def _cache(self):
        return self._class(self._servers, **self._options)

    def get_backend_timeout(self, timeout=DEFAULT_TIMEOUT):
        if timeout == DEFAULT_TIMEOUT:
            timeout = self.default_timeout
        # The key will be made persistent if None used as a timeout.
        # Non-positive values will cause the key to be deleted.
        return None if timeout is None else max(0, int(timeout))

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_and_validate_key(key, version=version)
        return self._cache.add(key, value, self.get_backend_timeout(timeout))

    def get(self, key, default=None, version=None):
        key = self.make_and_validate_key(key, version=version)
        return self._cache.get(key, default)

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_and_validate_key(key, version=version)
        self._cache.set(key, value, self.get_backend_timeout(timeout))

    def touch(self, key, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_and_validate_key(key, version=version)
        return self._cache.touch(key, self.get_backend_timeout(timeout))

    def delete(self, key, version=None):
        key = self.make_and_validate_key(key, version=version)
        return self._cache.delete(key)

    def get_many(self, keys, version=None):
        key_map = {
            self.make_and_validate_key(key, version=version): key for key in keys
        }
        ret = self._cache.get_many(key_map.keys())
        return {key_map[k]: v for k, v in ret.items()}

    def has_key(self, key, version=None):
        key = self.make_and_validate_key(key, version=version)
        return self._cache.has_key(key)

    def incr(self, key, delta=1, version=None):
        key = self.make_and_validate_key(key, version=version)
        return self._cache.incr(key, delta)

    def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None):
        if not data:
            return []
        safe_data = {}
        for key, value in data.items():
            key = self.make_and_validate_key(key, version=version)
            safe_data[key] = value
        self._cache.set_many(safe_data, self.get_backend_timeout(timeout))
        return []

    def delete_many(self, keys, version=None):
        if not keys:
            return
        safe_keys = [self.make_and_validate_key(key, version=version) for key in keys]
        self._cache.delete_many(safe_keys)

    def clear(self):
        return self._cache.clear()
