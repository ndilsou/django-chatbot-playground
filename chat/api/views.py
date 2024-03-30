from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.decorators import action
import structlog

from chat.api.serializers import GroupSerializer, UserSerializer
from chat.api import serializers as serde
from . import models
from . import permissions


logger = structlog.get_logger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class SystemPromptViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows system prompts to be viewed or edited.
    """

    queryset = models.SystemPrompt.objects.all()
    serializer_class = serde.SystemPromptSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Protect the view to only show notes owned by the logged in user.
        """
        return self.queryset.filter(owner=self.request.user)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or edited.
    """

    queryset = models.Conversation.objects.all()
    serializer_class = serde.ConversationSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwner]

    @action(detail=True, url_path="continue", methods=["post"])
    def continue_conversation(self, request, pk=None):
        serializer = serde.ContinueConversationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_message = serializer.validated_data

        conversation: models.Conversation = self.get_object()
        logger.info("new message", new_message=new_message)
        message = conversation.reply(new_message)
        serializer = serde.MessageSerializer(message, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        system_prompt = models.SystemPrompt.objects.get(
            owner=self.request.user, name="Default"
        )
        serializer.save(owner=self.request.user, system_prompt=system_prompt)

    def get_queryset(self):
        """
        Protect the view to only show notes owned by the logged in user.
        """
        return self.queryset.filter(owner=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """

    queryset = models.Message.objects.all()
    serializer_class = serde.MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        logger.info("kwargs", kwargss=self.kwargs)
        if conversation_id := self.kwargs.get("conversation_pk"):
            return self.queryset.filter(
                conversation_id=conversation_id, conversation__owner=self.request.user
            )
        return self.queryset.filter(conversation__owner=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """

    queryset = models.Tag.objects.all()
    serializer_class = serde.TagSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Protect the view to only show notes owned by the logged in user.
        """
        return self.queryset.filter(owner=self.request.user)


class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows notes to be viewed or edited.
    """

    queryset = models.Note.objects.all()
    serializer_class = serde.NoteSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Protect the view to only show notes owned by the logged in user.
        """
        return self.queryset.filter(owner=self.request.user)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/api/dj-rest-auth/google/callback/"
    client_class = OAuth2Client


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://localhost:8000/api/dj-rest-auth/github/callback/"
    client_class = OAuth2Client
