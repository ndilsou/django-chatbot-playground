# Generated by Django 5.0.3 on 2024-03-30 00:22

import chat.commons.cuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="messages",
            name="conversation",
        ),
        migrations.RemoveField(
            model_name="notes",
            name="tags",
        ),
        migrations.RemoveField(
            model_name="notes",
            name="user",
        ),
        migrations.RemoveField(
            model_name="tags",
            name="user",
        ),
        migrations.AlterField(
            model_name="systemprompt",
            name="id",
            field=chat.commons.cuid.Cuid2Field(
                default=chat.commons.cuid.create_id,
                editable=False,
                max_length=24,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.CreateModel(
            name="Conversation",
            fields=[
                (
                    "id",
                    chat.commons.cuid.Cuid2Field(
                        default=chat.commons.cuid.create_id,
                        editable=False,
                        max_length=24,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(default="Untitled", max_length=400)),
                (
                    "system_prompt",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.systemprompt",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    chat.commons.cuid.Cuid2Field(
                        default=chat.commons.cuid.create_id,
                        editable=False,
                        max_length=24,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("user", "User"),
                            ("system", "System"),
                            ("assistant", "Assistant"),
                            ("function", "Function"),
                        ],
                        max_length=10,
                    ),
                ),
                ("content", models.TextField()),
                ("name", models.CharField(max_length=400)),
                ("function_call", models.JSONField()),
                (
                    "conversation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.conversation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    chat.commons.cuid.Cuid2Field(
                        default=chat.commons.cuid.create_id,
                        editable=False,
                        max_length=24,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("label", models.CharField(max_length=400)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Note",
            fields=[
                (
                    "id",
                    chat.commons.cuid.Cuid2Field(
                        default=chat.commons.cuid.create_id,
                        editable=False,
                        max_length=24,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(default="Untitled", max_length=400)),
                ("content", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("tags", models.ManyToManyField(to="api.tag")),
            ],
        ),
        migrations.DeleteModel(
            name="Conversations",
        ),
        migrations.DeleteModel(
            name="Messages",
        ),
        migrations.DeleteModel(
            name="Notes",
        ),
        migrations.DeleteModel(
            name="Tags",
        ),
        migrations.AddIndex(
            model_name="tag",
            index=models.Index(fields=["label"], name="api_tag_label_26ebbe_idx"),
        ),
        migrations.AddIndex(
            model_name="note",
            index=models.Index(fields=["title"], name="api_note_title_4e44df_idx"),
        ),
    ]
