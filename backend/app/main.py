from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.api.scan import router as scan_router
from app.api.search import router as search_router
from app.api.tasks import router as task_router
from app.api.webhook import router as webhook_router
from app.api.ws import router as ws_router

app = FastAPI(title="AI Security Auditor")

# CORS must be registered before routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan_router)
app.include_router(search_router)
app.include_router(task_router)
app.include_router(webhook_router)
app.include_router(ws_router)


@app.get("/")
def home():
    return {"status": "running"}