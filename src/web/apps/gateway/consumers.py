import logging
import json
from channels.layers import get_channel_layer
from django.utils import timezone
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from web.redis_client import redis_client

logger = logging.getLogger(__name__)

class PingConsumer(AsyncJsonWebsocketConsumer):
    group_name = "ping_group"

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

      
        self.connection_key = f"ws:connected:{self.channel_name}"
        
        data = {
            "channel_name": self.channel_name,
            "user_id": self.scope["user"].id if self.scope.get("user") and self.scope["user"].is_authenticated else None,
            "ip": self.scope.get("client")[0] if self.scope.get("client") else None,
            "path": self.scope.get("path"),
            "connected_at": timezone.now().isoformat(),
        }

        await redis_client.set(self.connection_key, json.dumps(data), ex=360)  # Expire in 6 minutes


    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await redis_client.delete(self.connection_key)


    async def receive_json(self, content, **kwargs):
        # Log
        logger.info(f"{self.__class__.__name__} received message", extra={
            "path": self.scope.get("path"),
            "client": self.scope.get("client"),
            "payload_keys": list(content.keys()),
        })

        # Broadcast to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast_message",
                "content": content,
            }
        )

    async def broadcast_message(self, event):
        await self.send_json({
            "broadcast": event["content"]
        })
