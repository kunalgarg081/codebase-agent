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


def analyze_project() -> str:
    """
    Generate a high-level overview of the Python project.

    Includes:
    - Python files
    - Classes
    - Functions
    - Project dependencies
    - Project dependents
    """

    sections = []

    # ---------------------------------------------------------
    # Files
    # ---------------------------------------------------------

    files = []

    for file in iter_python_files():
        try:
            files.append(
                str(file.relative_to(workspace))
            )
        except ValueError:
            continue

    files = sorted(files)

    if files:
        sections.append(
            "Files\n"
            "-----\n"
            + "\n".join(
                f"- {file}"
                for file in files
            )
        )
    else:
        sections.append(
            "Files\n"
            "-----\n"
            "No Python files found."
        )

    # ---------------------------------------------------------
    # Classes
    # ---------------------------------------------------------

    classes = list_classes()

    if classes:

        class_lines = []

        for item in classes:
            class_lines.append(
                f"- {item['file']}: {item['class']}"
            )

        sections.append(
            "Classes\n"
            "-------\n"
            + "\n".join(class_lines)
        )

    else:
        sections.append(
            "Classes\n"
            "-------\n"
            "No Python classes found."
        )

    # ---------------------------------------------------------
    # Functions
    # ---------------------------------------------------------

    functions = list_python_functions()

    sections.append(
        "Functions\n"
        "---------\n"
        + functions
    )

    # ---------------------------------------------------------
    # Dependencies
    # ---------------------------------------------------------

    dependency_lines = []

    for file in files:

        result = find_module_dependencies(file)

        if result.startswith(
            "No project dependencies found"
        ):
            continue

        if result.startswith(
            "Access denied."
        ):
            continue

        if result.startswith(
            "File "
        ):
            continue

        if result.startswith(
            "Could not parse"
        ):
            continue

        for dependency in result.splitlines():

            dependency_lines.append(
                f"- {file} -> {dependency}"
            )

    sections.append(
        "Project Dependencies\n"
        "--------------------\n"
        + (
            "\n".join(dependency_lines)
            if dependency_lines
            else "No project dependencies found."
        )
    )

    # ---------------------------------------------------------
    # Dependents
    # ---------------------------------------------------------

    dependent_lines = []

    for file in files:

        result = find_module_dependents(file)

        if result.startswith(
            "No project dependents found"
        ):
            continue

        if result.startswith(
            "Access denied."
        ):
            continue

        if result.startswith(
            "File "
        ):
            continue

        if result.startswith(
            "Could not parse"
        ):
            continue

        for dependent in result.splitlines():

            dependent_lines.append(
                f"- {file} <- {dependent}"
            )

    sections.append(
        "Project Dependents\n"
        "------------------\n"
        + (
            "\n".join(dependent_lines)
            if dependent_lines
            else "No project dependents found."
        )
    )

    return (
        "Project Overview\n"
        "================\n\n"
        + "\n\n".join(sections)
    )


def build_dependency_graph() -> str:
    """
    Build a project-level dependency graph for Python modules.

    Returns a readable list of project-local dependencies.
    Standard-library and third-party imports are ignored.
    """

    files = []

    for file in iter_python_files():
        try:
            files.append(
                str(file.relative_to(workspace))
            )
        except ValueError:
            continue

    files = sorted(files)

    if not files:
        return (
            "Project Dependency Graph\n"
            "========================\n\n"
            "No Python files found."
        )

    graph_lines = []

    for file in files:

        result = find_module_dependencies(file)

        if result.startswith(
            "No project dependencies found"
        ):
            graph_lines.append(
                f"{file}\n"
                "    -> none"
            )
            continue

        if result.startswith(
            "Access denied."
        ):
            continue

        if result.startswith(
            "File "
        ):
            continue

        if result.startswith(
            "Could not parse"
        ):
            continue

        dependencies = result.splitlines()

        graph_lines.append(file)

        for dependency in dependencies:
            graph_lines.append(
                f"    -> {dependency}"
            )

    return (
        "Project Dependency Graph\n"
        "========================\n\n"
        + "\n".join(graph_lines)
    )

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


def find_symbol_references(symbol: str):
    """
    Find AST-level definitions, calls, imports, and references
    to a symbol across Python files in the workspace.
    """

    results = []

    workspace = Path(WORKSPACE)

    for path in workspace.rglob("*.py"):

        # Ignore hidden directories
        relative_path = path.relative_to(workspace)

        if any(
            part.startswith(".")
            for part in relative_path.parts
        ):
            continue

        try:
            source = path.read_text(
                encoding="utf-8",
                errors="replace",
            )

            tree = ast.parse(source)

        except (OSError, SyntaxError):
            continue

        relative_file = relative_path.as_posix()

        for node in ast.walk(tree):

            # Function definition
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):
                if node.name == symbol:
                    results.append({
                        "file": relative_file,
                        "line": node.lineno,
                        "kind": "definition",
                    })

            # Class definition
            elif isinstance(node, ast.ClassDef):
                if node.name == symbol:
                    results.append({
                        "file": relative_file,
                        "line": node.lineno,
                        "kind": "definition",
                    })

            # Function/class call
            elif isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):

                    if node.func.id == symbol:
                        results.append({
                            "file": relative_file,
                            "line": node.lineno,
                            "kind": "call",
                        })

                elif isinstance(node.func, ast.Attribute):

                    if node.func.attr == symbol:
                        results.append({
                            "file": relative_file,
                            "line": node.lineno,
                            "kind": "call",
                        })

            # import foo
            elif isinstance(node, ast.Import):

                for alias in node.names:

                    imported_name = (
                        alias.asname
                        or alias.name.split(".")[0]
                    )

                    if imported_name == symbol:
                        results.append({
                            "file": relative_file,
                            "line": node.lineno,
                            "kind": "import",
                        })

            # from module import symbol
            elif isinstance(node, ast.ImportFrom):

                for alias in node.names:

                    imported_name = (
                        alias.asname
                        or alias.name
                    )

                    if imported_name == symbol:
                        results.append({
                            "file": relative_file,
                            "line": node.lineno,
                            "kind": "import",
                        })

    return results


def find_module_dependencies(path: str):
    """
    Find project Python modules imported by a Python file.

    Returns project-local dependencies only.
    Standard-library and third-party imports are ignored.
    """

    file = resolve_workspace_path(path)

    if file is None:
        return "Access denied."

    if not file.exists():
        return f"File '{path}' does not exist."

    if not file.is_file():
        return f"'{path}' is not a file."

    if file.suffix != ".py":
        return "Only Python files can be analyzed."

    try:
        source = file.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        tree = ast.parse(source)

    except SyntaxError as e:
        return f"Could not parse '{path}': {e}"

    dependencies = set()

    for node in ast.walk(tree):

        # import greet
        if isinstance(node, ast.Import):

            for alias in node.names:

                module = alias.name.split(".")[0]

                candidate = workspace / f"{module}.py"

                if candidate.exists():
                    dependencies.add(
                        candidate.relative_to(workspace).as_posix()
                    )

        # from greet import greet
        elif isinstance(node, ast.ImportFrom):

            if not node.module:
                continue

            module = node.module.split(".")[0]

            candidate = workspace / f"{module}.py"

            if candidate.exists():
                dependencies.add(
                    candidate.relative_to(workspace).as_posix()
                )

    if not dependencies:
        return f"No project dependencies found for '{path}'."

    return "\n".join(sorted(dependencies))


def find_module_dependents(path: str):
    """
    Find project Python files that import the given Python module.

    Returns project files that depend on the specified module.
    Standard-library and third-party modules are ignored.
    """

    file = resolve_workspace_path(path)

    if file is None:
        return "Access denied."

    if not file.exists():
        return f"File '{path}' does not exist."

    if not file.is_file():
        return f"'{path}' is not a file."

    if file.suffix != ".py":
        return "Only Python files can be analyzed."

    target_module = file.stem

    dependents = set()

    for candidate in workspace.rglob("*.py"):

        try:
            source = candidate.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            tree = ast.parse(source)

        except (OSError, SyntaxError):
            continue

        for node in ast.walk(tree):

            # import greet
            # import greet as something
            if isinstance(node, ast.Import):

                for alias in node.names:

                    module = alias.name.split(".")[0]

                    if module == target_module:
                        dependents.add(
                            candidate.relative_to(workspace).as_posix()
                        )

            # from greet import greet
            elif isinstance(node, ast.ImportFrom):

                if not node.module:
                    continue

                module = node.module.split(".")[0]

                if module == target_module:
                    dependents.add(
                        candidate.relative_to(workspace).as_posix()
                    )

    if not dependents:
        return f"No project dependents found for '{path}'."

    return "\n".join(sorted(dependents))


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
    "find_symbol_references": {
        "function": find_symbol_references,
        "description": (
            "Find where a Python symbol is defined, called, "
            "or imported across the workspace."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Name of the Python symbol to find."
                }
            },
            "required": ["symbol"]
        }
    },
    "find_module_dependencies": {
        "function": find_module_dependencies,
        "description": (
            "Find project Python modules imported by a Python file."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "Relative path to the Python file "
                        "to analyze."
                    )
                }
            },
            "required": ["path"]
        }
    },
    "find_module_dependents": {
        "function": find_module_dependents,
        "description": (
            "Find project Python files that import or depend "
            "on a given Python module."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "Relative path to the Python module "
                        "to find dependents for."
                    )
                }
            },
            "required": ["path"]
        }
    },
    "analyze_project": {
        "function": analyze_project,
        "description": (
            "Generate a high-level overview of the Python project "
            "including files, classes, functions, dependencies, "
            "and dependents."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    "build_dependency_graph": {
        "function": build_dependency_graph,
        "description": (
            "Build a project-level dependency graph showing "
            "which Python files depend on other project files."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
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