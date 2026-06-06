from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/webhook/github")

async def github_webhook(
    request: Request
):

    payload = await request.json()

    repository = payload.get(
        "repository",
        {}
    ).get("clone_url")

    return {
        "message": "Webhook received",
        "repository": repository
    }