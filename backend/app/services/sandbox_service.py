import subprocess


def run_sandboxed_scan():

    subprocess.run([
        \"docker\",
        \"run\",
        \"--memory=512m\",
        \"--cpus=1\",
        \"--network=none\",
        \"--read-only\",
        \"security-scanner\"
    ])