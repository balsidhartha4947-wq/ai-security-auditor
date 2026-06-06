from fastapi import APIRouter

from celery.result import AsyncResult

from app.celery_app import celery

router = APIRouter()


@router.get("/task-status/{task_id}")

def get_task_status(task_id: str):

    result = AsyncResult(
        task_id,
        app=celery
    )

    response = {
        "task_id": task_id,
        "status": result.status
    }

    if result.info:

        response["details"] = str(result.info)

    return response