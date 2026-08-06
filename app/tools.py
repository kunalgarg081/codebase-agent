import ast
from pathlib import Path
import subprocess
import sys
from app.config import WORKSPACE

workspace = Path(WORKSPACE)


def resolve_workspace_path(path: str) -> Path | None:
    """
    Resolve a path inside the workspace.
    Returns None if the path escapes the workspace.
    """

    resolved = (workspace / path).resolve()

    workspace_root = workspace.resolve()

    if not str(resolved).startswith(str(workspace_root)):
        return None

    return resolved


def iter_python_files():
    """
    Iterate through all Python files in the workspace.
    """
    return workspace.rglob("*.py")


def read_file(path: str) -> str:
    """
    Read a file from the workspace.
    """

    file = resolve_workspace_path(path)

    if file is None:
        return "Access denied."

    if not file.exists():
        return f"File '{path}' does not exist."

    if file.is_dir():
        return f"'{path}' is a directory."

    return file.read_text(
        encoding="utf-8",
        errors="ignore",
    )

def write_file(path: str, content: str) -> str:
    """
    Write content to a file inside the workspace.
    Creates parent directories if needed.
    """

    file = resolve_workspace_path(path)
    
    if file is None:
        return "Access denied."

    try:

        file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file.write_text(
            content,
            encoding="utf-8",
        )

        return f"Successfully wrote '{path}'."

    except Exception as e:
        return f"Failed to write '{path}': {e}"


def run_python(path: str) -> str:
    """
    Execute a Python file inside the workspace.
    """

    file = (workspace / path).resolve()

    workspace_root = workspace.resolve()

    if not str(file).startswith(str(workspace_root)):
        return "Access denied."

    if not file.exists():
        return f"File '{path}' does not exist."

    if file.suffix != ".py":
        return "Only Python files can be executed."

    try:

        result = subprocess.run(
            [sys.executable, str(file)],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=workspace,
        )

        output = [
            "Python Execution",
            "================",
            f"File: {path}",
            f"Exit Code: {result.returncode}",
        ]
        
        
        if result.stdout:
            output.append("\nSTDOUT:")
            output.append(result.stdout)
        
        if result.stderr:
            output.append("\nSTDERR:")
            output.append(result.stderr)
        
        return "\n".join(output)

    except subprocess.TimeoutExpired:

        return "Execution timed out after 10 seconds."

    except Exception as e:

        return str(e)

def list_directory(path: str = ".") -> str:
    """
    List files and folders inside a directory.
    """

    directory = resolve_workspace_path(path)
    
    if directory is None:
        return "Access denied."

    if not directory.exists():
        return f"Directory '{path}' does not exist."

    return "\n".join(
        file.name
        for file in directory.iterdir()
    )


def list_files() -> list[str]:
    """
    Recursively list all files in the workspace.
    """

    ignored_dirs = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".vscode",
    }

    files = []

    for file in workspace.rglob("*"):

        if not file.is_file():
            continue

        if any(
            part in ignored_dirs
            for part in file.parts
        ):
            continue

        files.append(
            str(file.relative_to(workspace))
        )

    files.sort()

    return files


def search_text(keyword: str) -> str:
    """
    Search every project file for a keyword.
    """

    matches = []

    for file in workspace.rglob("*"):

        if not file.is_file():
            continue

        try:

            lines = file.read_text(
                encoding="utf-8",
                errors="ignore",
            ).splitlines()

            for line_number, line in enumerate(lines, start=1):

                if keyword.lower() in line.lower():

                    matches.append(
                        f"{file.relative_to(workspace)}:{line_number}: {line.strip()}"
                    )

        except Exception:
            continue

    if not matches:
        return f"No matches found for '{keyword}'."

    return "\n".join(matches)


def list_python_functions() -> str:
    """
    List every Python function in the workspace.
    """

    results = []

    for file in iter_python_files():

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            tree = ast.parse(source)

            functions = [
                node.name
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            ]

            if functions:

                results.append(
                    f"{file.relative_to(workspace)}\n"
                    + "\n".join(
                        f"- {func}()"
                        for func in functions
                    )
                )

        except Exception:
            continue

    if not results:
        return "No Python functions found."

    return "\n\n".join(results)


def list_classes() -> list[dict]:
    """
    List all Python classes in the workspace.
    """

    results = []

    for file in iter_python_files():

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            tree = ast.parse(source)

            for node in ast.walk(tree):

                if isinstance(node, ast.ClassDef):

                    results.append(
                        {
                            "file": str(file.relative_to(workspace)),
                            "class": node.name,
                        }
                    )

        except Exception:
            continue

    return sorted(
        results,
        key=lambda item: (item["file"], item["class"])
    )


def list_imports() -> list[dict]:
    """
    List all imports in the workspace.
    """

    results = []

    for file in iter_python_files():

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            tree = ast.parse(source)

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        results.append(
                            {
                                "file": str(file.relative_to(workspace)),
                                "module": alias.name,
                                "alias": alias.asname,
                            }
                        )

                elif isinstance(node, ast.ImportFrom):

                    results.append(
                        {
                            "file": str(file.relative_to(workspace)),
                            "module": node.module,
                            "imports": [
                                alias.name
                                for alias in node.names
                            ],
                        }
                    )

        except Exception:
            continue         

    return sorted(
        results,
        key=lambda item: (
            item["file"],
            item["module"] or "",
        ),
    )

def get_function_source(function_name: str) -> str:
    """
    Return the complete source code of a function.
    """

    for file in iter_python_files():

        try:

            source = file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            tree = ast.parse(source)

            for node in tree.body:

                if (
                    isinstance(node, ast.FunctionDef)
                    and node.name == function_name
                ):
                    return ast.get_source_segment(
                        source,
                        node,
                    )

        except Exception:
            continue

    return f"Function '{function_name}' not found."


def get_project_context() -> str:
    """
    Read important project files and return
    their contents for summarization.
    """

    context = []

    important_files = []

    for name in [
        "README.md",
        "main.py",
        "requirements.txt",
    ]:
        file = workspace / name
        if file.exists():
            important_files.append(file)

    important_files.extend(workspace.rglob("*.py"))

    for file in important_files:

        if not file.is_file():
            continue

        if "__pycache__" in str(file):
            continue

        try:

            relative = file.relative_to(workspace)

            content = file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            context.append(
                f"""
=========================
File: {relative}
=========================

{content[:1500]}
"""
            )

        except Exception:
            continue

    return "\n".join(context)


def review_file(path: str) -> str:
    """
    Read a file for AI code review.
    """

    return read_file(path)


TOOLS = {
    "read_file": {
        "function": read_file,
        "description": "Read the contents of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the file."
                }
            },
            "required": ["path"]
        }
    },

    "list_directory": {
        "function": list_directory,
        "description": "List files and folders inside a directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory relative to the workspace."
                }
            }
        }
    },

    "search_text": {
        "function": search_text,
        "description": "Search every project file for a keyword.",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "Keyword to search for."
                }
            },
            "required": ["keyword"]
        }
    },

    "list_python_functions": {
        "function": list_python_functions,
        "description": "List all Python functions in the workspace.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },

    "get_function_source": {
        "function": get_function_source,
        "description": "Return the source code of a Python function.",
        "parameters": {
            "type": "object",
            "properties": {
                "function_name": {
                    "type": "string",
                    "description": "Name of the function."
                }
            },
            "required": ["function_name"]
        }
    },

    "get_project_context": {
        "function": get_project_context,
        "description": "Collect important project files for summarization.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },

    "review_file": {
        "function": review_file,
        "description": "Read a file for AI code review.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the file."
                }
            },
            "required": ["path"]
        }
    },
    "write_file": {
        "function": write_file,
        "description": "Create or overwrite a file inside the workspace.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path of the file."
                },
                "content": {
                    "type": "string",
                    "description": "Content to write into the file."
                }
            },
            "required": [
                "path",
                "content"
            ]
        }
    },
    "run_python": {
        "function": run_python,
        "description": "Execute a Python file inside the workspace.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to a Python file."
                }
            },
            "required": ["path"]
        }
    },
    "list_files": {
        "function": list_files,
        "description": "Recursively list all files in the workspace.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    "list_classes": {
        "function": list_classes,
        "description": "List all Python classes in the workspace.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    "list_imports": {
        "function": list_imports,
        "description": "List all imports in the workspace.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": name,
            "description": tool["description"],
            "parameters": tool["parameters"],
        },
    }
    for name, tool in TOOLS.items()
]