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

- All tests pass.

---

## Level 2 – Integration Tests

Verify that the Agent, LLM, Tool Executor, and tools work together correctly.

Examples:

- Read file
- Write file
- Run Python
- Search
- AST tools

---

## Level 3 – User Scenarios

Test realistic workflows.

Examples:

- Explain a file.
- Review code.
- Create a new file.
- Modify existing code.
- Execute Python.
- Search the project.

---

# Certification Checklist

## File Operations

- [ ] Read existing file
- [ ] Read missing file
- [ ] Write file
- [ ] Prevent writing outside workspace

---

## Directory Operations

- [ ] List workspace

---

## Search

- [ ] Search existing text
- [ ] Search missing text

---

## Python Execution

- [ ] Execute valid Python file
- [ ] Execute file with runtime error

---

## AST

- [ ] List Python functions
- [ ] Get function source

---

## Agent

- [ ] Project context
- [ ] Code review
- [ ] Multi-step reasoning
- [ ] Conversation memory

---

# CLI Testing

## Normal Mode

Verify:

- Single-line commands are executed immediately.

Examples:

- Read hello.py
- Run greet.py
- Explain calculator.py

---

## Code Mode

Enter:

```
/code
```

Verify:

- Multiline prompt is accepted.
- Code formatting is preserved.
- `END` sends the prompt.
- CLI returns to normal mode after execution.

---

# Release Decision

A version is ready for release when:

- Unit tests pass.
- Manual certification passes.
- No critical bugs remain.
- Documentation is updated.