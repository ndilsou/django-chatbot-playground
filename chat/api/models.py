from django.db import models
import structlog
from chat import settings
from chat import commons
from chat.commons import Cuid2Field
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from litellm import completion

logger = structlog.get_logger(__name__)


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = ["username"]

    id = Cuid2Field(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(_("email address"), unique=True)

    class Meta:
        ordering = ["email"]


class SystemPrompt(commons.BaseModel):
    name = models.CharField(max_length=400, default="Untitled")
    content = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class Conversation(commons.BaseModel):
    title = models.CharField(max_length=400, default="Untitled")
    system_prompt = models.ForeignKey(
        SystemPrompt,
        on_delete=models.SET_NULL,
        null=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def reply(self, new_input_message: dict) -> dict:
        next_message = Message(**new_input_message, conversation=self)
        next_message.save()
        messages_q = Message.objects.filter(conversation_id=self.id).order_by(
            "created_at"
        )

        messages = [
            dict(
                role=m.role,
                content=m.content,
                name=m.name,
                function_call=m.function_call,
            )
            for m in messages_q
        ]
        # messages.append(
        #     dict(
        #         role=next_message.role,
        #         content=next_message.content,
        #         name=next_message.name,
        #         function_call=next_message.function_call,
        #     )
        # )
        response = completion(
            model="claude-3-sonnet-20240229",
            messages=messages,
        )
        content = response.choices[0].message.content
        reply_message = Message(
            role=Message.RoleType.ASSISTANT,
            content=content,
            conversation=self,
        )
        reply_message.save()

        logger.info(
            "data",
            messages=messages,
        )
        return reply_message


class Message(commons.BaseModel):
    class RoleType(models.TextChoices):
        USER = "user"
        SYSTEM = "system"
        ASSISTANT = "assistant"
        FUNCTION = "function"

    role = models.CharField(max_length=10, choices=RoleType.choices)
    content = models.TextField()
    name = models.CharField(max_length=400, null=True)
    function_call = models.JSONField(null=True)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
    )


class Tag(commons.BaseModel):
    class Meta:
        indexes = [
            models.Index(fields=["label"]),
        ]

    label = models.CharField(max_length=400)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class Note(commons.BaseModel):
    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]

    # id = Cuid2Field(primary_key=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=400, default="Untitled")
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
