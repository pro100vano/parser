import json

from channels.generic.websocket import AsyncWebsocketConsumer


class Consumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(f"{self.scope['url_route']['kwargs']['room_name']}", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        self.channel_layer.group_discard(f"{self.scope['url_route']['kwargs']['room_name']}", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # await self.send(text_data=text_data)
        pass

    async def send_data(self, data):
        await self.send(text_data=json.dumps(data.get('data')))
