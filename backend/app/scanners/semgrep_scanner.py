# backend/app/scanners/semgrep_scanner.py
import subprocess
import json
import os

SEMGREP_PATH = os.getenv("SEMGREP_PATH", "semgrep")


def run_semgrep(path: str, target_files: list = None) -> dict:

    abs_path = os.path.abspath(path).replace("\\", "/")
    print(f"Semgrep scanning: {abs_path}")

    if not os.path.exists(abs_path):
        print(f"Path does not exist: {abs_path}")
        return {"error": f"Repository path does not exist: {abs_path}", "results": []}

    if not os.listdir(abs_path):
        print(f"Path is empty: {abs_path}")
        return {"error": f"Repository folder is empty: {abs_path}", "results": []}

    # Incremental: scan only changed files if provided
    if target_files:
        targets = [
            os.path.abspath(os.path.join(path, f)).replace("\\", "/")
            for f in target_files
        ]
        targets = [t for t in targets if os.path.exists(t)]

        if not targets:
            print("No valid changed files found — falling back to full scan")
            scan_targets = [abs_path]
        else:
            print(f"Incremental scan: {len(targets)} file(s)")
            scan_targets = targets
    else:
        print("Full scan")
        scan_targets = [abs_path]

    command = [
        SEMGREP_PATH,
        "scan",
        "--config", "auto",
        "--json",
        "--no-git-ignore",
    ] + scan_targets

    try:
        print("Running command:", command)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300
        )

        print("Return code:", result.returncode)

        if result.stderr:
            print("Semgrep stderr:", result.stderr[:500])

        if result.stdout:
            try:
                parsed = json.loads(result.stdout)
                print(f"Findings count: {len(parsed.get('results', []))}")
                return parsed
            except json.JSONDecodeError as e:
                print("JSON parse error:", repr(e))
                print("Raw stdout preview:", result.stdout[:300])
                return {"error": "Failed to parse Semgrep output", "results": []}

        print("No stdout from Semgrep")
        return {"results": []}

    except subprocess.TimeoutExpired:
        print("Semgrep timed out after 300s")
        return {"error": "Scan timed out", "results": []}

    except FileNotFoundError:
        print("Semgrep executable not found")
        return {"error": "Semgrep not found - please install semgrep", "results": []}

    except Exception as e:
        print("SEMGREP ERROR:", repr(e))
        return {"error": str(e), "results": []}