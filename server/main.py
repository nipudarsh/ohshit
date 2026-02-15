from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# Very small "connection manager" for MVP
class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, message: str):
        for ws in list(self.active):
            await ws.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            msg = await ws.receive_text()
            await manager.broadcast(msg)
    except WebSocketDisconnect:
        manager.disconnect(ws)

