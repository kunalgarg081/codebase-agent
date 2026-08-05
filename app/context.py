from app.tools import read_file

IMPORTANT_FILES = [
    "README.md",
    "main.py",
    "requirements.txt",
]


def build_project_context() -> str:
    """
    Collect important project files.
    """

    parts = []

    for file in IMPORTANT_FILES:

        content = read_file(file)

        if "does not exist" in content:
            continue

        parts.append(
            f"""
====================
{file}
====================

{content}
"""
        )

    return "\n".join(parts)
