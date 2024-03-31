from django.db import models
from cuid2 import Cuid

cuid = Cuid()


def create_id() -> str:
    return cuid.generate()


class Cuid2Field(models.CharField):
    description = "A cuid2 string"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 24
        kwargs["default"] = create_id
        super().__init__(*args, **kwargs)


class BaseModel(models.Model):
    """Base Django Model with default autoincremented ID field replaced with UUIDT."""

    class Meta:
        abstract = True

    id = Cuid2Field(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
