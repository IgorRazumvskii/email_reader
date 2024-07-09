import json
from channels.generic.websocket import AsyncWebsocketConsumer


class EmailFetchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('email_fetch_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('email_fetch_group', self.channel_name)

    async def update_progress(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
