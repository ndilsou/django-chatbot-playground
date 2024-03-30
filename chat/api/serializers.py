from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["url", "id", "username", "email", "groups"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "id", "name"]


class SystemPromptSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.SystemPrompt
        fields = ["url", "id", "name", "content", "owner"]


class ConversationSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    system_prompt = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Conversation
        fields = ["url", "id", "title", "system_prompt", "owner"]


class ContinueConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ["role", "content"]


class MessageSerializer(serializers.ModelSerializer):
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Message
        fields = ["url", "id", "role", "content", "name", "conversation"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ["url", "id", "label"]


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Note
        fields = ["url", "id", "title", "content", "owner", "tags"]
