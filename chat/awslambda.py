import os
import django

# Set the settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.awslambda_settings")

# Initialize Django
django.setup()

from chat.api.models import Message  # noqa: E402


def handler(event, context):
    result = Message.objects.all()
    messages = []
    for message in result:
        msg = {
            "role": message.role,
            "content": message.content,
            "name": message.name,
            "function_call": message.function_call,
        }
        messages.append(msg)
        print(msg)
    return {
        "statusCode": 200,
        "body": str(messages),
    }
