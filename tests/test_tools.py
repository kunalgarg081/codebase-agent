from app.tools import (
    read_file,
    write_file,
    list_directory,
    search_text,
    list_python_functions,
    get_function_source,
    run_python,
)


def test_read_existing_file():
    result = read_file("hello.py")
    assert "Hello World" in result


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

    result = search_text("Hello World")

    assert "hello.py" in result


def test_list_python_functions():

    result = list_python_functions()

    assert "greet" in result


def test_get_function_source():

    result = get_function_source("greet")

    assert "def greet" in result


def test_run_python():

    result = run_python("hello.py")

    assert "Exit Code: 0" in result

    assert "Hello World" in result
