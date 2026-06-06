# backend/app/services/repository_service.py
import os
import shutil
from git import Repo

BASE_DIR = os.path.abspath("repositories")
os.makedirs(BASE_DIR, exist_ok=True)


def get_repo_path(repo_url: str) -> str:
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    return os.path.abspath(os.path.join(BASE_DIR, repo_name))


def get_latest_commit_hash(repo_url: str) -> str:
    """Get HEAD commit hash without cloning (fast, uses ls-remote)."""
    import subprocess
    result = subprocess.run(
        ["git", "ls-remote", repo_url, "HEAD"],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode == 0 and result.stdout:
        return result.stdout.split()[0]
    return None


def get_local_commit_hash(repo_path: str) -> str:
    """Get HEAD commit hash of an already-cloned repo."""
    try:
        repo = Repo(repo_path)
        return repo.head.commit.hexsha
    except Exception:
        return None


def get_changed_files(repo_path: str, old_hash: str, new_hash: str) -> list[str]:
    """Return list of files changed between two commits."""
    try:
        repo = Repo(repo_path)
        old_commit = repo.commit(old_hash)
        new_commit = repo.commit(new_hash)
        diff = old_commit.diff(new_commit)
        return [d.b_path for d in diff if d.b_path]
    except Exception:
        return []


def clone_repository(repo_url: str) -> str:
    target_path = get_repo_path(repo_url)

    # Remove empty/broken clone
    if os.path.exists(target_path) and not os.listdir(target_path):
        print(f"Removing empty/broken clone: {target_path}")
        shutil.rmtree(target_path)

    if not os.path.exists(target_path):
        print(f"Cloning {repo_url} into {target_path}")
        Repo.clone_from(repo_url, target_path)
    else:
        # Pull latest changes if repo already exists
        print(f"Pulling latest changes for {target_path}")
        repo = Repo(target_path)
        repo.remotes.origin.pull()

    print(f"Repo ready at: {target_path}")
    return target_path