import os


SUSPICIOUS_PATTERNS = [
    \"eval(\",
    \"exec(\",
    \"pickle.loads\",
    \"subprocess\",
    \"os.system\"
]


def scan_repository_structure(
    repo_path: str
):

    findings = []

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if file.endswith((
                \".py\",
                \".js\",
                \".ts\"
            )):

                full_path = os.path.join(
                    root,
                    file
                )

                try:

                    with open(
                        full_path,
                        \"r\",
                        encoding=\"utf-8\"
                    ) as f:

                        content = f.read()

                        for pattern in (
                            SUSPICIOUS_PATTERNS
                        ):

                            if pattern in content:

                                findings.append({
                                    \"file\": full_path,
                                    \"pattern\": pattern
                                })

                except Exception:
                    pass

    return findings