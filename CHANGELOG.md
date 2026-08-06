# Changelog

All notable changes to this project will be documented here.

---

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