# Codebase Agent Roadmap

## Current Version

v2.1

---

## Completed Features

- OpenAI Compatible LLM
- Native Tool Calling
- Read File
- Write File
- List Directory
- Search Text
- Run Python
- List Python Functions
- Get Function Source
- Project Context
- Code Review
- Conversation History
- Write Confirmation

---

## Current Architecture

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
Workspace
```

---

## Sprint 1 (Current)

Repository Intelligence

Planned Features

- [ ] List Files
- [ ] List Classes
- [ ] List Imports
- [ ] Find Symbol
- [ ] Find References

---

## Sprint 2

Editing Improvements

- [ ] Backup File
- [ ] Preview Diff
- [ ] Apply Patch

---

## Sprint 3

Execution

- [ ] Run Pytest
- [ ] Run Shell Command
- [ ] Format Code

---

## Sprint 4

Memory

- [ ] Conversation Memory
- [ ] Project Memory

---

## Sprint 5

Planning

- [ ] Planning Agent
- [ ] Multi-step Reasoning
- [ ] Better Context Selection