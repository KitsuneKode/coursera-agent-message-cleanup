# AGENTS.md

## Project Overview

Coursera Agent Message Cleanup — a CLI tool that removes the Coursera AI agent
compliance/academic-integrity boilerplate text from copied quiz questions and
puts the cleaned result on the clipboard.

## Structure

```
coursera-agent-message-cleanup/
├── coursera-agent-message-cleanup.py  # Main script
├── pyproject.toml                     # Project config + deps
├── test.txt                           # Sample input for manual testing
├── .gitignore
├── AGENTS.md
└── README.md
```

## Dependencies

- Python 3.10+
- `pyperclip` — clipboard access (managed via uv)

## Setup

```bash
uv sync
```

## Running

```bash
uv run python coursera-agent-message-cleanup.py          # interactive (paste + Ctrl+D)
uv run python coursera-agent-message-cleanup.py < file   # from file/pipe
cat file.txt | uv run python coursera-agent-message-cleanup.py
```

## Matching Strategy

The boilerplate is matched via the compiled regex `_COURSERA_PATTERN` at the
top of the script — **not** a literal string constant. Key decisions:

| Property         | Value                              | Reason                                                                                             |
| ---------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------- |
| Start anchor     | `You are a helpful AI assistant\.` | First sentence; never appears in quiz content                                                      |
| End anchor       | `Do you understand\?\.`            | Last sentence; unique enough to be safe                                                            |
| `re.DOTALL`      | enabled                            | Allows `.` to match newlines across the multi-line blob                                            |
| `re.IGNORECASE`  | enabled                            | Guards against copy-paste casing inconsistencies                                                   |
| Non-greedy `.*?` | used between anchors               | Ensures each occurrence is removed independently without consuming content between multiple blocks |

Removal is done with `re.subn()` in a single pass, which returns both the
cleaned string and the substitution count — avoiding a redundant `findall`
scan to count matches.

## Conventions

- No external network calls
- Keep the script self-contained — single file, no submodules
- Boilerplate detection lives in `_COURSERA_PATTERN` (compiled `re.Pattern`)
- Prefer `re.subn()` over separate `findall()` + `sub()` when both the result
  and the count are needed
- Add inline comments only where the regex flags or non-obvious decisions need
  explaining; avoid noise comments elsewhere
