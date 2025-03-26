import json
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, Form, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
from loan_advisory_service.services.web_socket_service import WebsocketService
import logging
web_socket_router = APIRouter(prefix="/ws", route_class=DishkaRoute)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@web_socket_router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    container = websocket.app.state.dishka_container
    manager = await container.get(WebsocketService)
    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "join_chat_room":
                manager.join_chat_room(user_id, message["chat_room_id"])
                await websocket.send_json({
                    "type": "response",
                    "message": f"Joined chat room {message['chat_room_id']}"
                })
            elif message["type"] == "leave_chat_room":
                manager.leave_chat_room(user_id, message["chat_room_id"])
                await websocket.send_json({
                    "type": "response",
                    "message": f"Left chat room {message['chat_room_id']}"
                })
            elif message["type"] == "chat_message":
                await manager.send_chat_message(message["chat_room_id"], message["message"])
            elif message["type"] == "add_admin":
                manager.add_admin(user_id)
                await websocket.send_json({
                    "type": "response",
                    "message": "You are now an admin"
                })
            elif message["type"] == "remove_admin":
                manager.remove_admin(user_id)
                await websocket.send_json({
                    "type": "response",
                    "message": "You are no longer an admin"
                })

    except WebSocketDisconnect:
        manager.disconnect(user_id)
        print(f"User {user_id} disconnected")

