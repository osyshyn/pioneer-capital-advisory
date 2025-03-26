from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Set, List
import json
from pydantic import BaseModel
from dishka import Provider, Scope, provide, make_async_container
from dishka.integrations.fastapi import FromDishka, setup_dishka


class WebsocketService:
    def __init__(self):
        self._user_connections: Dict[str, WebSocket] = {}
        self._chat_rooms: Dict[str, List[str]] = {}
        self._admins: Set[str] = set()

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self._user_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self._user_connections:
            del self._user_connections[user_id]
            for chat_room_id in list(self._chat_rooms.keys()):
                if user_id in self._chat_rooms[chat_room_id]:
                    self._chat_rooms[chat_room_id].remove(user_id)
                    if not self._chat_rooms[chat_room_id]:
                        del self._chat_rooms[chat_room_id]

    async def send_chat_message(self, chat_room_id: str, message: str):
        if chat_room_id not in self._chat_rooms:
            return
        for user_id in self._chat_rooms[chat_room_id]:
            if user_id in self._user_connections:
                await self._user_connections[user_id].send_json({
                    "type": "chat_message",
                    "chat_room_id": chat_room_id,
                    "message": message
                })

    async def send_notification(self, user_id: str, application_id: str, new_status: str):
        if user_id in self._user_connections:
            await self._user_connections[user_id].send_json({
                "type": "notification",
                "application_id": application_id,
                "status": new_status
            })

    async def send_admin_message(self, message: str):
        for admin_id in self._admins:
            if admin_id in self._user_connections:
                await self._user_connections[admin_id].send_json({
                    "type": "admin_message",
                    "message": message
                })

    def join_chat_room(self, user_id: str, chat_room_id: str):
        if chat_room_id not in self._chat_rooms:
            self._chat_rooms[chat_room_id] = []
        if user_id not in self._chat_rooms[chat_room_id]:
            self._chat_rooms[chat_room_id].append(user_id)

    def leave_chat_room(self, user_id: str, chat_room_id: str):
        if chat_room_id in self._chat_rooms and user_id in self._chat_rooms[chat_room_id]:
            self._chat_rooms[chat_room_id].remove(user_id)
            if not self._chat_rooms[chat_room_id]:
                del self._chat_rooms[chat_room_id]

    def add_admin(self, user_id: str):
        self._admins.add(user_id)

    def remove_admin(self, user_id: str):
        self._admins.discard(user_id)

    def get_admins(self) -> List[int]:
        return list(map(lambda i: int(i), self._admins))
