#!/usr/bin/env python3
"""
Android Preview Server
Stream de screenshots do emulador Android via WebSocket
"""

import asyncio
import base64
import subprocess
import json
from typing import Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Android Preview Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado global
connected_clients: list[WebSocket] = []
streaming = False
current_device: Optional[str] = None


def get_screenshot(device_id: str) -> Optional[bytes]:
    """Captura screenshot via ADB"""
    try:
        result = subprocess.run(
            ["adb", "-s", device_id, "exec-out", "screencap", "-p"],
            capture_output=True,
            timeout=2
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
    except Exception as e:
        print(f"Erro ao capturar screenshot: {e}")
    return None


def get_devices() -> list[dict]:
    """Lista dispositivos conectados"""
    try:
        result = subprocess.run(
            ["adb", "devices", "-l"],
            capture_output=True,
            text=True,
            timeout=5
        )
        devices = []
        for line in result.stdout.strip().split("\n")[1:]:
            if line.strip() and "device" in line:
                parts = line.split()
                device_id = parts[0]
                model = "unknown"
                for part in parts:
                    if part.startswith("model:"):
                        model = part.split(":")[1]
                devices.append({"id": device_id, "model": model})
        return devices
    except Exception as e:
        print(f"Erro ao listar devices: {e}")
        return []


def send_click(device_id: str, x: int, y: int) -> bool:
    """Envia clique para o dispositivo"""
    try:
        subprocess.run(
            ["adb", "-s", device_id, "shell", "input", "tap", str(x), str(y)],
            timeout=2
        )
        return True
    except Exception:
        return False


def send_key(device_id: str, key: str) -> bool:
    """Envia tecla para o dispositivo"""
    key_codes = {
        "back": "4",
        "home": "3",
        "recent": "187",
        "volume_up": "24",
        "volume_down": "25",
        "power": "26"
    }
    try:
        code = key_codes.get(key, key)
        subprocess.run(
            ["adb", "-s", device_id, "shell", "input", "keyevent", code],
            timeout=2
        )
        return True
    except Exception:
        return False


@app.get("/")
async def root():
    return {"status": "ok", "service": "Android Preview Server"}


@app.get("/devices")
async def list_devices():
    """Lista dispositivos Android conectados"""
    return {"devices": get_devices()}


@app.get("/screenshot/{device_id}")
async def screenshot(device_id: str):
    """Captura screenshot único"""
    img = get_screenshot(device_id)
    if img:
        return {"image": base64.b64encode(img).decode("utf-8")}
    return {"error": "Failed to capture screenshot"}


@app.post("/click/{device_id}")
async def click(device_id: str, x: int, y: int):
    """Envia clique"""
    success = send_click(device_id, x, y)
    return {"success": success}


@app.post("/key/{device_id}")
async def key(device_id: str, key: str):
    """Envia tecla"""
    success = send_key(device_id, key)
    return {"success": success}


@app.websocket("/ws/{device_id}")
async def websocket_stream(websocket: WebSocket, device_id: str):
    """WebSocket para stream de screenshots"""
    await websocket.accept()
    connected_clients.append(websocket)

    print(f"Cliente conectado para device: {device_id}")

    try:
        # Loop de streaming
        fps = 10  # 10 FPS para preview
        interval = 1.0 / fps

        while True:
            # Captura screenshot
            img = get_screenshot(device_id)
            if img:
                # Envia como base64
                data = {
                    "type": "frame",
                    "image": base64.b64encode(img).decode("utf-8"),
                    "device": device_id
                }
                await websocket.send_json(data)

            # Verifica se há comandos do cliente
            try:
                msg = await asyncio.wait_for(
                    websocket.receive_json(),
                    timeout=interval
                )
                await handle_command(device_id, msg)
            except asyncio.TimeoutError:
                pass  # Timeout esperado, continua streaming

    except WebSocketDisconnect:
        print(f"Cliente desconectado: {device_id}")
    except Exception as e:
        print(f"Erro no WebSocket: {e}")
    finally:
        connected_clients.remove(websocket)


async def handle_command(device_id: str, msg: dict):
    """Processa comandos recebidos via WebSocket"""
    cmd = msg.get("command")

    if cmd == "click":
        send_click(device_id, msg.get("x", 0), msg.get("y", 0))
    elif cmd == "key":
        send_key(device_id, msg.get("key", ""))
    elif cmd == "set_fps":
        # Permite ajustar FPS dinamicamente
        pass


def main():
    """Inicia o servidor"""
    print("=" * 50)
    print("Android Preview Server")
    print("=" * 50)
    print(f"Dispositivos: {get_devices()}")
    print("Iniciando servidor em http://localhost:8765")
    print("WebSocket em ws://localhost:8765/ws/<device_id>")
    print("=" * 50)

    uvicorn.run(app, host="0.0.0.0", port=8765)


if __name__ == "__main__":
    main()
