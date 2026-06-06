from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from celery.result import AsyncResult

from app.services.websocket_manager import manager

router = APIRouter()


@router.websocket("/ws/{task_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    task_id: str
):
    await manager.connect(task_id, websocket)

    try:
        await websocket.send_json({
            "progress": 0,
            "step": f"Connected to task {task_id}"
        })

        while True:
            await asyncio.sleep(2)

            result = AsyncResult(task_id)

            if result.state == "PROGRESS":
                meta = result.info or {}
                await websocket.send_json({
                    "progress": meta.get("progress", 0),
                    "step": meta.get("step", "Processing...")
                })

            elif result.state == "SUCCESS":
                await websocket.send_json({
                    "progress": 100,
                    "step": "Completed",
                    "results": result.result
                })
                break  # ← exit loop cleanly

            elif result.state == "FAILURE":
                await websocket.send_json({
                    "progress": 0,
                    "step": "Failed",
                    "error": str(result.result)
                })
                break

            else:
                # PENDING or STARTED
                await websocket.send_json({
                    "progress": 0,
                    "step": "Waiting for task to start..."
                })

    except WebSocketDisconnect:
        manager.disconnect(task_id, websocket)

    finally:
        manager.disconnect(task_id, websocket)  # cleanup on any exit