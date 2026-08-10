from pathlib import Path

from app.tools import (
    read_file,
    write_file,
    list_directory,
    list_files,
    search_text,
    list_python_functions,
    get_function_source,
    run_python,
    workspace,
    list_classes,
    list_imports,
    find_symbol_references,
)


def test_read_existing_file():
    result = read_file("hello.py")
    assert "Hello Python" in result


def test_read_missing_file():
    result = read_file("missing.py")
    assert "does not exist" in result


def test_path_traversal():
    result = read_file("../../secret.txt")
    assert result == "Access denied."


def test_write_file():
    result = write_file(
        "pytest_test.py",
        'print("pytest")'
    )

    assert "Successfully wrote" in result

    content = read_file("pytest_test.py")

    assert "pytest" in content


def test_list_directory():

    result = list_directory()

    assert "hello.py" in result


def test_search_text():

    result = search_text("Hello Python")

    assert "hello.py" in result


def test_find_symbol_references_function():

    result = find_symbol_references("greet")

    assert any(
        item["file"] == "greet.py"
        and item["kind"] == "definition"
        for item in result
    )

    assert any(
        item["file"] == "greet.py"
        and item["kind"] == "call"
        for item in result
    )


def test_find_symbol_references_import():

    result = find_symbol_references("greet")

    assert any(
        item["file"] == "imports_demo.py"
        and item["kind"] == "import"
        for item in result
    )


def test_find_symbol_references_class():

    result = find_symbol_references("Calculator")

    assert any(
        item["file"] == "classes_demo.py"
        and item["kind"] == "definition"
        for item in result
    )


def test_find_symbol_references_no_match():

    result = find_symbol_references("DefinitelyNotARealSymbol")

    assert result == []
def test_list_python_functions():

    result = list_python_functions()

    assert "greet" in result


def test_get_function_source():

    result = get_function_source("greet")

    assert "def greet" in result


def test_run_python():

    result = run_python("hello.py")

    assert "Exit Code: 0" in result

    assert "Hello Python" in result


def test_list_files():

    result = list_files()

    assert "hello.py" in result
    assert "greet.py" in result


def test_list_files_returns_relative_paths():

    result = list_files()

    for path in result:
        assert not Path(path).is_absolute()


def test_list_files_ignores_hidden_directories():

    hidden = workspace / ".git"
    hidden.mkdir(exist_ok=True)

    secret = hidden / "secret.py"
    secret.write_text("print('secret')")

    result = list_files()

    assert ".git/secret.py" not in result

    secret.unlink()


def test_list_classes():

    result = list_classes()

    class_names = [
        item["class"]
        for item in result
    ]

    assert "Calculator" in class_names
    assert "User" in class_names

def test_list_classes_returns_file():

    result = list_classes()

    files = {
        item["file"]
        for item in result
    }

    assert "classes_demo.py" in files


def test_list_classes_relative_paths():

    result = list_classes()

    for item in result:

        assert not Path(item["file"]).is_absolute()


def test_list_imports():

    result = list_imports()

    modules = [
        item["module"]
        for item in result
    ]

    assert "math" in modules
    assert "os" in modules
    assert "pathlib" in modules
    assert "greet" in modules


def test_list_imports_returns_relative_paths():

    result = list_imports()

    for item in result:

        assert not Path(item["file"]).is_absolute()


def test_list_imports_from_import():

    result = list_imports()

    pathlib_import = next(
        item
        for item in result
        if item["module"] == "pathlib"
    )

    assert "Path" in pathlib_import["imports"]
