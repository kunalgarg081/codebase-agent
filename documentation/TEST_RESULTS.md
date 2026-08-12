# Codebase Agent Certification

---

# Version

v0.5.0

Certification Date: 2026-08-10

Status: 🟢 Active Certification

---

# Automated Tests

| Test | Result |
|------|--------|
| pytest | ✅ PASS (25/25) |

---

# Manual Tests

| Feature | Result | Notes |
|---------|--------|-------|
| Read Existing File | ✅ PASS | Correct tool selected and file returned. |
| Read Missing File | ✅ PASS | Friendly error message displayed. |
| Write File | ✅ PASS | Confirmation shown before writing. |
| Write Confirmation | ✅ PASS | File successfully created after approval. |
| List Directory | ✅ PASS | Correct files listed. |
| Search Text | 🟡 PASS | Works correctly but performs unnecessary follow-up reads. |
| Run Python | ✅ PASS | Executed successfully with correct output and exit code. |
| List Python Functions | ✅ PASS | AST tool returned all functions correctly. |
| Get Function Source | ✅ PASS | Returned exact function source. |

---
## 2026-08-07

### Investigation: Random 401 Unauthorized

Symptoms:
- All requests failed immediately with HTTP 401.
- Failure occurred on the first prompt.

Root Cause:
- Selected model (`north-mini-code-free`) was no longer usable with the provider.

Resolution:
- Switched to another supported model.
- No code changes were required.

Status:
- Resolved.
---

# v2.2 Feature Certification

| Feature | Result | Notes |
|---------|--------|-------|
| list_files() | ✅ PASS | Recursive listing works correctly. |
| Relative Paths | ✅ PASS | Returns workspace-relative paths only. |
| Hidden Directory Filtering | ✅ PASS | Ignores `.git`, `__pycache__`, `.pytest_cache`, and `.vscode`. |
| list_classes() | ✅ PASS | Correctly discovers Python classes using AST. |
| Relative Paths | ✅ PASS | Returns workspace-relative file paths. |
| File Mapping | ✅ PASS | Correctly associates each class with its source file. |
| list_imports() | ✅ PASS | Detects both `import` and `from ... import ...` statements. |

---

# Observations

## Improvements

- `search_text()` should return matching lines instead of only filenames.
- Reduce unnecessary follow-up tool calls.
- Add configurable debug levels.

---

# Remaining Tests

- [ ] Project Context
- [ ] Code Review
- [ ] Conversation Memory
- [ ] Invalid Tool Handling

---

# Overall Status

Current Result:

- No critical bugs found.
- Core tools are working correctly.
- Project is considered stable for continued development.

Certification Status:

🟡 In Progress

---

# v0.5.0 Certification

## Automated Tests

| Result | Status |
|---|---|
| Pytest | ✅ 41/41 passed |

## Repository Intelligence

| Feature | Result | Notes |
|---|---|---|
| `find_symbol_references()` | ✅ PASS | AST-based definitions, calls, and imports |
| `find_module_dependencies()` | ✅ PASS | Identifies project-local Python dependencies |
| `find_module_dependents()` | ✅ PASS | Identifies project files that depend on a Python module |
| `analyze_project()` | ✅ PASS | Generates a high-level project overview |
| `build_dependency_graph()` | ✅ PASS | Builds a project-level dependency graph |
| `find_module_impact()` | ✅ PASS | Identifies files directly affected by a module change |
| `find_symbol_impact()` | ✅ PASS | Analyzes project references to a Python symbol |

## Manual Tests

| Query | Result |
|---|---|
| Where is greet used? | ✅ PASS |
| Where is Calculator used? | ✅ PASS |
| Where is divide used? | ✅ PASS |
| What does imports_demo.py depend on? | ✅ PASS |
| Which project files does imports_demo.py import? | ✅ PASS |
| Who depends on greet.py? | ✅ PASS |
| Which files import calculator.py? | ✅ PASS |
| Give me an overview of this project. | ✅ PASS |
| How are the project files connected? | ✅ PASS |
| Show me the dependency graph. | ✅ PASS |
| What depends on greet.py? | ✅ PASS |
| What would be affected if I change greet.py? | ✅ PASS |
| What would be affected if I change calculator.py? | ✅ PASS |
| What would be affected if I change greet? | ✅ PASS |
| What would be affected if I change Calculator? | ✅ PASS |

## Certification Status

🟢 v0.5.0 repository intelligence milestone verified.