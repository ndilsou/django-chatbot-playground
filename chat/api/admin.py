from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from . import models


class UserAdmin(DjangoUserAdmin):
    ordering = ("email",)


admin.site.register(models.User, UserAdmin)


class SystemPromptAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at", "content")


admin.site.register(models.SystemPrompt, SystemPromptAdmin)


class ConversationsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at", "system_prompt", "owner")


admin.site.register(models.Conversation, ConversationsAdmin)


class MessagesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "role",
        "content",
        "name",
        "created_at",
        "updated_at",
        "conversation",
    )


admin.site.register(models.Message, MessagesAdmin)


class TagsAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "created_at", "updated_at", "owner")


admin.site.register(models.Tag, TagsAdmin)


class NotesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content", "created_at", "updated_at", "owner")
    filter_horizontal = ("tags",)


admin.site.register(models.Note, NotesAdmin)
