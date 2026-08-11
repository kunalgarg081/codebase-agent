# Changelog

All notable changes to this project will be documented here.

---

## v0.5.0 - Repository Intelligence

### Added

- Added `find_symbol_references()` using Python AST.
- Added detection of symbol definitions.
- Added detection of function and class calls.
- Added detection of imports.
- Added `find_module_dependencies()` for project-local Python dependencies.
- Standard-library imports are excluded from project dependency results.
- Added `find_module_dependents()` to identify project files that depend on a Python module.
- Added reverse dependency analysis for project-local Python modules.
- Added `analyze_project()` for high-level project structure and dependency analysis.
- Added project overview analysis covering files, classes, functions, dependencies, and dependents.

### Testing

- Automated test suite expanded from 22 to 25 tests.
- All 25 tests pass.
- Manually verified symbol reference queries for:
  - `greet`
  - `Calculator`
  - `divide`
- Manually verified module dependency analysis for `imports_demo.py`.

### Integration

- Added both tools to the agent tool registry.
- Verified that the LLM selects the new tools correctly.


## v2.1

### Added

- OpenAI compatible LLM support
- Native Tool Calling
- File reading
- File writing
- Python execution
- Directory listing
- Project search
- Function listing using AST
- Function source extraction
- Project context builder
- Code review tool
- Conversation history
- User confirmation before file modification

---

## [v2.1.1] - 2026-08-06

### Added

- Added `/code` mode for multiline prompts.
- Added `TEST_RESULTS.md` to record certification results.
- Added `list_classes()` tool for discovering Python classes using the AST.
- Added `list_imports()` tool for discovering Python imports using the AST.

### Changed

- Normal prompts now use single-line input.
- Multiline prompts are entered through `/code`.
- Improved CLI user experience.

### Testing

- Started v2.1 certification.
- Verified:
  - Read File
  - Write File
  - List Directory
  - Run Python
  - List Python Functions
  - Get Function Source

### Known Improvements

- `search_text()` should return matching lines to reduce unnecessary follow-up tool calls.

---

## Upcoming

v2.2

- Repository Intelligence
- List Files
- List Classes
- Find Symbols