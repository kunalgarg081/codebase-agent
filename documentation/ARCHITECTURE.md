# Codebase Agent Architecture

This document explains the design decisions, architecture, and development philosophy of the Codebase Agent.

---

# Project Goal

The purpose of this project is not only to build an AI-powered Codebase Agent, but also to understand how modern AI agents are designed and implemented from scratch.

The project intentionally avoids large agent frameworks such as LangGraph, CrewAI, AutoGen, and similar libraries.

Every component should be:

- Simple
- Modular
- Easy to understand
- Easy to extend
- Easy to test

The goal is to learn software engineering by building a production-style project step by step.

---

# Development Philosophy

We follow a few simple principles throughout the project.

- Build one feature at a time.
- Keep the architecture simple.
- Test every feature before moving to the next.
- Refactor only when there is a real need.
- Prefer readable code over clever code.
- Small improvements consistently are better than large rewrites.

---

# Architecture Overview

```
User
    │
    ▼
CLI (main.py)
    │
    ▼
Agent
    │
    ▼
LLM
    │
    ▼
Tool Executor
    │
    ▼
Workspace Tools
    │
    ▼
Workspace
```

The Agent is responsible for orchestrating the conversation.

The LLM is responsible for reasoning.

The tools interact with the project files.

---

# Command Line Interface (CLI)

The application provides two input modes.

## Normal Mode

Used for everyday interactions.

Examples:

- Read hello.py
- Run greet.py
- Explain calculator.py

Press **Enter** to send the command.

---

## Code Mode

Enter:

```
/code
```

The CLI switches to multiline mode.

The user can paste long prompts or source code.

Typing:

```
END
```

on a new line submits the entire prompt and returns the CLI to normal mode.

This approach keeps normal interactions fast while providing a reliable way to submit multiline code without terminal input limitations.

---

# Folder Responsibilities

## app/

Contains the implementation of the Codebase Agent.

Current modules include:

- agent.py
- llm.py
- tools.py
- tool_executor.py
- context.py
- state.py
- config.py
- prompts.py
- tool_result.py

---

## workspace/

Contains the project that the agent is allowed to inspect, execute, and modify.

The agent should never access files outside this directory.

---

## tests/

Contains automated tests for the project.

Every major feature should eventually have corresponding tests.

---

# Why OpenAI Tool Calling?

Instead of asking the LLM to manually generate JSON, the project uses the native Tool Calling API.

Benefits:

- Structured arguments
- Better reliability
- Less parsing code
- Easier to extend
- Better error handling

---

# Why a Workspace?

The workspace acts as a safety boundary.

All file operations are limited to the configured workspace directory.

This prevents accidental modification of unrelated files.

---

# Why Python AST?

Python's AST module understands Python syntax.

Compared to searching raw text, AST is:

- More accurate
- Less error-prone
- Easier to extend

Current AST Features:

- List Python Functions
- Get Function Source
- List Classes
- List Imports
- Find Symbol References
- Find Module Dependencies
- Find Module Dependents
- Analyze Project
- Build Dependency Graph
- Find Module Impact
- Find Symbol Impact

## Symbol Reference Analysis

The `find_symbol_references()` tool uses Python's AST to locate:

- Symbol definitions
- Function and class calls
- Imports
- Project-local references

For example, it can distinguish a real function call from ordinary text containing the same word.

## Module Dependency Analysis

The `find_module_dependencies()` tool analyzes Python imports and identifies project-local Python modules used by a file.

Standard-library imports such as `math`, `os`, and `pathlib` are not reported as project dependencies.

Example:

```text
imports_demo.py
    ↓
greet.py
```

---

# Why Ask Before Writing Files?

The AI should never modify user files without permission.

Before calling the write tool, the user must explicitly approve the operation.

This provides an additional safety layer.

---

# Git Workflow

Every feature follows the same workflow.

```
Requirement
        ↓
Design
        ↓
Implementation
        ↓
Testing
        ↓
Documentation
        ↓
Commit
```

Each feature should have its own Git commit.

This keeps the project history clean and easy to understand.

---

# Coding Guidelines

Whenever possible:

- Keep functions small.
- Keep modules focused.
- Avoid duplicate code.
- Prefer composition over complexity.
- Write descriptive function names.
- Add tests for new functionality.
- Document important design decisions.

---

# Future Architecture

As the project grows, new capabilities will be added.

Examples include:

- Repository indexing
- Symbol lookup
- Class discovery
- Import analysis
- Dependency graph
- Git integration
- Patch generation
- Planning Agent
- Long-term Memory

These should be added only when they solve a real problem.

Avoid premature optimization.

---

# Design Principles

The project follows several architectural principles.

## Tools return data

Tools should return structured Python data whenever possible.

The LLM is responsible for converting that data into natural language for the user.

Keeping these responsibilities separate makes tools easier to test and reuse.

---

## Keep Version 1 Simple

New features should solve one problem well.

Additional options and flexibility should only be introduced after a real need is identified through testing.

---

## Test Before Expanding

Every feature follows the same lifecycle:

Requirement

↓

Design

↓

Implementation

↓

Manual Testing

↓

Unit Tests

↓

Documentation

↓

Git Commit

Only after a feature completes this cycle should the next feature begin.

---
# Learning Goal

This project is a learning project.

The objective is not only to build a capable Codebase Agent but also to understand:

- Python architecture
- Agent design
- Tool calling
- Clean code
- Software engineering
- Git workflows
- Testing
- Project organization

Every feature should be implemented in a way that explains both **how** it works and **why** it was designed that way.

The journey of building the agent is as important as the final product.

# Repository Intelligence

Repository Intelligence is the next stage of the project.

Instead of operating on individual files only, the agent gradually learns the structure of the entire repository.

Current repository tools:

- list_directory()
- list_files()
- list_python_functions()
- list_classes()
- list_imports()

Design decisions:

- Search recursively through the workspace.
- Return relative paths instead of absolute paths.
- Ignore implementation directories such as `.git`, `__pycache__`, `.pytest_cache`, and `.vscode`.
- Return structured data (`list[str]`) instead of formatted text.
- Keep Version 1 simple. Filtering by extension or directory can be added later if required.

This design allows future tools such as:

- list_classes()
- list_imports()
- find_symbol()
- find_references()

to reuse the same repository understanding.

