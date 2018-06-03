from celery.decorators import task
from webpush import send_user_notification, send_group_notification
from django.contrib.auth import get_user_model

User = get_user_model()


@task(name="send_notification_to_user")
def send_notification_to_user(username, message):
    payload = {"head": "WEB PUSH to"+username, "body": message}
    user = User.objects.get(username=username)
    send_user_notification(user=user, payload=payload, ttl=1000)


@task(name="send_notification_to_group")
def send_notification_to_group(group, message):
    payload = {"head": "WEB PUSH", "body": message}
    send_group_notification(group_name=group, payload=payload, ttl=1000)
