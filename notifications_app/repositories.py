import asyncio

import requests
from django.contrib.auth.models import User
from notifications_app.models import NotificationModel, TgAccounts
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class NotificationRepository:

    def __init__(self, user=None):
        if user is not None:
            self.user = user

    def create_notification(self, message):
        notification = NotificationModel.objects.create(
            user=self.user,
            message=message
        )
        unread_count = self.get_unread_count()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f"user_{1}", {
            "type": "send_data",
            "data": {
                "func": "notification",
                'id': notification.id,
                'message': notification.message,
                'timestamp': int(notification.date_created.timestamp()),
                'unread_count': unread_count,
            },
        })

    @staticmethod
    def create_notifications_for_all_users(message):
        for user in User.objects.all():
            NotificationRepository(user).create_notification(message)

    def get_all(self, **kwargs):
        offset = kwargs.get('offset', 0)
        step = kwargs.get('step', 50)
        notifications = NotificationModel.objects.filter(user=self.user).order_by('-date_created')[offset:offset+step]
        NotificationModel.objects.filter(id__in=[n.id for n in notifications]).update(has_seen=True)
        return notifications

    def read(self, pk):
        try:
            notification = NotificationModel.objects.get(user=self.user, pk=pk)
            notification.has_seen = True
            notification.save()
            return True
        except Exception as e:
            print(e)
            return False

    def get_some(self, count, **kwargs):
        offset = kwargs.get('offset', 0)
        return NotificationModel.objects.filter(user=self.user).order_by('-date_created')[offset:offset+count]

    def get_unread_count(self):
        return NotificationModel.objects.filter(user=self.user, has_seen=False).count()


class TgNotificationsRepository:

    url = 'https://api.telegram.org/bot'
    token = "8208541014:AAEJdxKg6FEFciTC7_CZnPE_WwE8NqJrURs"

    def __init__(self, user=None, **kwargs):
        if user is not None:
            self.user = user
        elif kwargs.get('user', None) is not None:
            self.user = kwargs.get('user')

    async def send_message(self, tg_user_id, message):
        params = {
            'chat_id': tg_user_id,
            'parse_mode': 'html',
            'text': message
        }
        try:
            requests.get(f"{self.url}{self.token}/sendMessage", params=params)
            return True
        except Exception as e:
            print(e)
            return False

    async def send_message_all(self, message):
        async for tg_user in TgAccounts.objects.filter(user=self.user):
            asyncio.create_task(self.send_message(tg_user.tg_id, message))

    def get_list(self):
        return TgAccounts.objects.filter(user=self.user)

    def add_user(self, tg_id):
        if TgAccounts.objects.create(user=self.user, tg_id=tg_id):
            return True
        return False

    def remove_user(self, pk):
        try:
            TgAccounts.objects.get(user=self.user, pk=pk).delete()
        except Exception as e:
            print(e)

    def command_start(self, data):
        pass
