from django.db.models.signals import post_save
from django.dispatch import receiver

from .ai import DEFAULT_SYSTEM_PROMPT
from .models import User, SystemPrompt


@receiver(post_save, sender=User, dispatch_uid="create_system_prompt_for_new_user")
def create_system_prompt_for_new_user(sender, instance, created, **kwargs):
    if created:
        SystemPrompt.objects.create(
            name="Default", content=DEFAULT_SYSTEM_PROMPT, user=instance
        )
