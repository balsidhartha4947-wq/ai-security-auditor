# backend/app/api/scan.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.repository import Repository
from app.models.scan import Scan
from app.tasks.scan_tasks import run_security_scan
from app.services.repository_service import get_latest_commit_hash, get_repo_path

router = APIRouter()


@router.post("/scan")
def start_scan(repo_url: str, db: Session = Depends(get_db)):
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")

    # Fetch or create repository record
    db_repo = db.query(Repository).filter(Repository.url == repo_url).first()
    if not db_repo:
        db_repo = Repository(name=repo_name, url=repo_url)
        db.add(db_repo)
        db.commit()
        db.refresh(db_repo)

    # Check latest commit hash (fast, no clone needed)
    latest_hash = get_latest_commit_hash(repo_url)

    if latest_hash and db_repo.last_commit_hash == latest_hash:
        # Repo unchanged — find the last completed scan and return it
        last_scan = (
            db.query(Scan)
            .filter(Scan.repository_id == db_repo.id, Scan.status == "completed")
            .order_by(Scan.created_at.desc())
            .first()
        )
        if last_scan:
            return {
                "task_id": None,
                "status": "cached",
                "message": "No changes since last scan. Returning cached results.",
                "scan_id": last_scan.id,
                "total_findings": last_scan.total_findings,
            }

    # Repo changed (or first scan) — queue a new scan
    task = run_security_scan.delay(repo_url, db_repo.id, latest_hash)

    return {
        "task_id": task.id,
        "status": "queued"
    }