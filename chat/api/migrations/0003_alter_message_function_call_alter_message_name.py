# Generated by Django 5.0.3 on 2024-03-30 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_remove_messages_conversation_remove_notes_tags_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="function_call",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="message",
            name="name",
            field=models.CharField(max_length=400, null=True),
        ),
    ]
