import asyncio
from fastapi import WebSocket
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK


class ConnectionManager:

    def __init__(self):
        self.connections: dict[str, list[WebSocket]] = {}

    async def connect(self, task_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections.setdefault(task_id, []).append(websocket)

    def disconnect(self, task_id: str, websocket: WebSocket):
        if task_id not in self.connections:
            return

        self.connections[task_id].discard(websocket) \
            if hasattr(self.connections[task_id], "discard") \
            else self.connections[task_id].remove(websocket)

        # Clean up empty task entries
        if not self.connections[task_id]:
            del self.connections[task_id]

    async def send_task_update(self, task_id: str, message: dict):
        if task_id not in self.connections:
            return

        dead = []

        for ws in self.connections[task_id]:
            try:
                await ws.send_json(message)
            except (ConnectionClosedError, ConnectionClosedOK, RuntimeError):
                dead.append(ws)

        for ws in dead:
            self.disconnect(task_id, ws)


manager = ConnectionManager()