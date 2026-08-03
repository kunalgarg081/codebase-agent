import ast
from pathlib import Path
from app.config import WORKSPACE

workspace = Path(WORKSPACE)


def search_text(keyword: str):

    matches = []

    for file in workspace.rglob("*"):

        if not file.is_file():
            continue

        try:
            lines = file.read_text(encoding="utf-8").splitlines()

            for line_number, line in enumerate(lines, start=1):

                if keyword.lower() in line.lower():

                    matches.append(
                        f"{file.relative_to(workspace)}:{line_number}: {line.strip()}"
                    )

        except Exception:
            pass

    if not matches:
        return f"No matches found for '{keyword}'."

    return "\n".join(matches)

def list_python_functions():
    """
    Find every Python function inside the workspace.
    """

    results = []

    for file in workspace.rglob("*.py"):

        try:

            source = file.read_text(encoding="utf-8")

            tree = ast.parse(source)

            functions = [
                node.name
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            ]

            if functions:

                results.append(
                    f"{file.relative_to(workspace)}\n"
                    + "\n".join(f"- {func}()" for func in functions)
                )

        except Exception:
            pass

    if not results:
        return "No Python functions found."

    return "\n\n".join(results)

def read_file(path: str):
    file = workspace / path

    if not file.exists():
        return f"File '{path}' does not exist."

    if file.is_dir():
        return f"'{path}' is a directory."

    return file.read_text(encoding="utf-8")


def list_directory(path="."):
    directory = workspace / path

    if not directory.exists():
        return f"Directory '{path}' does not exist."

    return "\n".join(
        file.name
        for file in directory.iterdir()
    )

def get_function_source(function_name: str):
    """
    Returns the source code of a Python function.
    """

    for file in workspace.rglob("*.py"):

        try:

            source = file.read_text(encoding="utf-8")

            tree = ast.parse(source)

            for node in tree.body:

                if isinstance(node, ast.FunctionDef):

                    if node.name == function_name:

                        return ast.get_source_segment(source, node)

        except Exception:
            pass

    return f"Function '{function_name}' not found."

def get_project_context():
    """
    Returns the important files of the project.
    """

    context = []

    for file in workspace.rglob("*"):

        if not file.is_file():
            continue

        # Ignore cache files
        if "__pycache__" in str(file):
            continue

        try:

            relative = file.relative_to(workspace)

            content = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            # Prevent huge prompts
            content = content[:1500]

            context.append(
                f"""
=========================
File: {relative}
=========================

{content}
"""
            )

        except Exception:
            pass

    return "\n".join(context)

def review_file(path: str):
    """
    Returns the contents of a file for AI review.
    """

    return read_file(path)







TOOLS = {
    "read_file": read_file,
    "list_directory": list_directory,
    "search_text": search_text,
    "list_python_functions": list_python_functions,
    "get_function_source": get_function_source,
    "get_project_context": get_project_context,
    "review_file": review_file,
}