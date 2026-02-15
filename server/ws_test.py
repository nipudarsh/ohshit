import os
import websocket

IP = os.getenv("OHSHIT_SERVER_IP", "127.0.0.1")
ws = websocket.create_connection(f"ws://{IP}:8000/ws")
print("Connected to", IP)

try:
    while True:
        msg = input("> ")
        ws.send(msg)
except KeyboardInterrupt:
    ws.close()
