import os

DANGEROUS_EXTENSIONS = [
    \".exe\",
    \".dll\",
    \".bin\",
    \".so\"
]


def contains_dangerous_files(path):

    for root, dirs, files in os.walk(path):

        for file in files:

            for ext in DANGEROUS_EXTENSIONS:

                if file.endswith(ext):

                    return True

    return False