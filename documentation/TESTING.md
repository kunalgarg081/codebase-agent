# Codebase Agent Testing Guide

This document describes how every release should be tested before it is considered stable.

---

# Testing Levels

## Level 1 – Unit Tests

Run:

```bash
pytest -v
```

Expected:

* All tests pass.
* Current test suite: **32 tests**.

---

## Level 2 – Integration Tests

Verify that the Agent, LLM, Tool Executor, and tools work together correctly.

Examples:

* Read file
* Write file
* Run Python
* Search
* AST tools
* Symbol reference analysis
* Module dependency analysis
* Module dependent analysis
* Project analysis

---

## Level 3 – User Scenarios

Test realistic workflows.

Examples:

* Explain a file.
* Review code.
* Create a new file.
* Modify existing code.
* Execute Python.
* Search the project.
* Get a project overview.
* Analyze project file connections.

---

# Certification Checklist

## File Operations

* [ ] Read existing file
* [ ] Read missing file
* [ ] Write file
* [ ] Prevent writing outside workspace

---

## Directory Operations

* [x] List workspace
* [x] List all files recursively

---

## Search

* [ ] Search existing text
* [ ] Search missing text

---

## Python Execution

* [ ] Execute valid Python file
* [ ] Execute file with runtime error

---

## AST

* [ ] List Python functions
* [ ] Get function source
* [x] Find symbol references
* [x] Find module dependencies
* [x] Find module dependents
* [x] Analyze project
* [x] Build dependency graph
- [x] Find module impact

---

## Agent

* [ ] Project context
* [ ] Code review
* [ ] Multi-step reasoning
* [ ] Conversation memory
* [x] Project overview
* [x] Project file connections
- [x] Module impact analysis
- [x] Find symbol impact

---

# CLI Testing

## Normal Mode

Verify:

* Single-line commands are executed immediately.

Examples:

* Read hello.py
* Run greet.py
* Explain calculator.py
* Get a project overview
* Analyze project file connections

---

## Code Mode

Enter:

```text
/code
```

Verify:

* Multiline prompt is accepted.
* Code formatting is preserved.
* `END` sends the prompt.
* CLI returns to normal mode after execution.

---

# Release Decision

A version is ready for release when:

* Unit tests pass.
* Manual certification passes.
* No critical bugs remain.
* Documentation is updated.
