# Architecture Notes

This document explains why important design decisions were made.

---

## Why OpenAI Tool Calling?

Instead of asking the LLM to generate JSON manually, we use the native Tool Calling API.

Benefits:

- More reliable
- Structured arguments
- Easier to extend
- Less parsing code

---

## Why a Workspace Folder?

The agent should never modify files outside the selected project.

All file operations are limited to the workspace directory.

This provides a basic safety layer.

---

## Why AST?

Python's AST module understands the structure of Python code.

Using AST is much more reliable than searching text with regular expressions.

Current AST Features:

- List Functions
- Get Function Source

Future AST Features:

- List Classes
- List Imports
- Find Symbols
- Dependency Analysis

---

## Why Ask Before Writing Files?

The AI should never modify user files without permission.

Every write operation requires confirmation.

This prevents accidental changes.

---

## Design Principles

- Keep modules small and focused.
- Prefer simple code over clever code.
- Build one feature at a time.
- Test every feature before adding the next.
- Refactor only when there is a real need.