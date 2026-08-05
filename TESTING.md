# Codebase Agent Testing Guide

This document defines the testing procedure before every release.

---

# Version

Current Version: v2.1

---

# 1. Automated Tests

Run:

```bash
pytest
```

Expected Result:

- All tests should pass.

Status:

- [ ] Passed

---

# 2. File Operations

## Read Existing File

Prompt:

Read the file `hello.py`.

Expected:

- File contents are returned.

Status:

- [ ] Passed

---

## Read Missing File

Prompt:

Read `missing.py`.

Expected:

- Friendly error message.

Status:

- [ ] Passed

---

## Write File

Prompt:

Create a file named `demo.py` with:

print("Hello")

Expected:

- Confirmation is shown.
- File is created.

Status:

- [ ] Passed

---

## Write Outside Workspace

Attempt to write outside the workspace.

Expected:

- Operation denied.

Status:

- [ ] Passed

---

# 3. Directory Operations

Prompt:

List the project directory.

Expected:

- Files are listed correctly.

Status:

- [ ] Passed

---

# 4. Search

Search for text that exists.

Status:

- [ ] Passed

Search for text that does not exist.

Status:

- [ ] Passed

---

# 5. Python AST

List Python functions.

Status:

- [ ] Passed

---

Get function source.

Status:

- [ ] Passed

---

# 6. Python Execution

Run a valid Python file.

Status:

- [ ] Passed

---

Run a Python file with an error.

Status:

- [ ] Passed

---

# 7. Project Context

Ask:

Describe this project.

Expected:

- Agent uses project context correctly.

Status:

- [ ] Passed

---

# 8. Code Review

Ask for a code review of a workspace file.

Status:

- [ ] Passed

---

# 9. Multi-Step Reasoning

Ask a question that requires multiple tool calls.

Expected:

- Agent completes all required steps.

Status:

- [ ] Passed

---

# 10. Conversation

Ask a follow-up question.

Expected:

- Previous conversation is remembered.

Status:

- [ ] Passed

---

# Release Decision

Ready to Release

- [ ] Yes
- [ ] No

Notes

__________________________