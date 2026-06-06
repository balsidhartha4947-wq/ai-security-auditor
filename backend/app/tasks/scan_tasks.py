# backend/app/tasks/scan_tasks.py
import time
from app.celery_app import celery
from app.services.repository_service import (
    clone_repository,
    get_local_commit_hash,
    get_changed_files,
    get_repo_path,
)
from app.scanners.semgrep_scanner import run_semgrep
from app.database.database import SessionLocal
from app.models.repository import Repository
from app.models.scan import Scan


@celery.task(bind=True)
def run_security_scan(self, repo_url: str, repo_id: int = None, new_hash: str = None):
    print("SCAN STARTED")
    total = time.time()
    db = SessionLocal()

    try:
        # Step 1: Clone / pull
        self.update_state(state="PROGRESS", meta={"progress": 10, "step": "Cloning repository"})
        t = time.time()
        repo_path = clone_repository(repo_url)
        print(f"Clone/pull took: {time.time() - t:.2f}s")

        # Step 2: Determine if incremental scan is possible
        db_repo = db.query(Repository).filter(Repository.id == repo_id).first() if repo_id else None
        old_hash = db_repo.last_commit_hash if db_repo else None
        current_hash = get_local_commit_hash(repo_path)

        changed_files = []
        if old_hash and current_hash and old_hash != current_hash:
            changed_files = get_changed_files(repo_path, old_hash, current_hash)
            print(f"Incremental scan: {len(changed_files)} changed files")

        # Step 3: Run Semgrep (full or incremental)
        self.update_state(state="PROGRESS", meta={"progress": 40, "step": "Running Semgrep"})
        t = time.time()

        if changed_files:
            # Only scan changed files — massive speedup for large repos
            results = run_semgrep(repo_path, target_files=changed_files)
        else:
            # First scan or no diff available — full scan
            results = run_semgrep(repo_path)

        print(f"Semgrep took: {time.time() - t:.2f}s")
        print(f"Total scan time: {time.time() - total:.2f}s")

        if "error" in results and "results" not in results:
            raise Exception(results["error"])

        total_findings = len(results.get("results", []))
        print(f"Total findings: {total_findings}")

        # Step 4: Persist scan record + update commit hash
        if db_repo:
            db_repo.last_commit_hash = current_hash
            scan_record = Scan(
                repository_id=repo_id,
                status="completed",
                total_findings=total_findings,
            )
            db.add(scan_record)
            db.commit()

        return {
            "progress": 100,
            "step": "Completed",
            "results": results,
            "total_findings": total_findings,
        }

    except Exception as e:
        print(f"SCAN ERROR: {repr(e)}")
        self.update_state(state="FAILURE", meta={"progress": 0, "step": "Failed", "error": str(e)})
        raise

    finally:
        db.close()