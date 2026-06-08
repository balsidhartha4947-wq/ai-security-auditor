from fastapi import APIRouter
from celery.result import AsyncResult
from app.celery_app import celery
import json

router = APIRouter()

@router.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    try:
        result = AsyncResult(task_id, app=celery)
        
        info = result.info
        
        # If info is an exception, convert to string
        if isinstance(info, Exception):
            info = {"error": str(info)}
        
        # If info is a dict, use it directly
        if isinstance(info, dict):
            details = info
        else:
            details = {"raw": str(info)} if info else {}

        return {
            "task_id": task_id,
            "status": result.status,
            "progress": details.get("progress", 0),
            "step": details.get("step", result.status),
            "results": details.get("results", None),
            "error": details.get("error", None)
        }
    except Exception as e:
        return {
            "task_id": task_id,
            "status": "ERROR",
            "progress": 0,
            "step": str(e),
            "results": None,
            "error": str(e)
        }