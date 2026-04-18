# AGENTS.md

## Project Overview

Coursera Agent Message Cleanup — a CLI tool that removes the Coursera AI agent
compliance/academic-integrity boilerplate text from copied quiz questions and
outputs the cleaned result to any combination of: terminal screen, clipboard, or file.

## Structure

```
coursera-agent-message-cleanup/
├── coursera_agent_message_cleanup.py    # Main script (valid Python module name)
├── pyproject.toml                       # Project config + deps + entry point
├── test_coursera.py                     # Automated pytest unit tests
├── test_manual.py                       # Manual smoke-test runner
├── test.txt                             # Sample input for testing
├── LICENSE                              # MIT
├── .gitignore
├── AGENTS.md
└── README.md
```

## Dependencies

- Python 3.10+
- `pyperclip` — clipboard access

### Install (uv recommended)

```bash
uv sync
```

### Install (pip — no uv needed)

```bash
pip install pyperclip
```

## Running

```bash
# Default: clipboard -> clipboard
uv run python coursera_agent_message_cleanup.py            # from clipboard
uv run python coursera_agent_message_cleanup.py -f file    # from file
uv run python coursera_agent_message_cleanup.py < file     # stdin redirect
cat file.txt | uv run python coursera_agent_message_cleanup.py  # pipe

# Add screen output
uv run python coursera_agent_message_cleanup.py -f q.txt --screen

# Add file output
uv run python coursera_agent_message_cleanup.py -f q.txt -o out.txt

# With pip (no uv):
python coursera_agent_message_cleanup.py -f questions.txt
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

## Output Model

Clipboard is always written to by default. `--screen` and `--output` are additive flags that add extra destinations.

Input priority: `-f FILE` > stdin pipe > clipboard (default).

Summary output goes to stderr; cleaned text goes to stdout (when `--screen` is set).

## Conventions

- No external network calls
- Keep the script self-contained — single file, no submodules
- Boilerplate detection lives in `_COURSERA_PATTERN` (compiled `re.Pattern`)
- Prefer `re.subn()` over separate `findall()` + `sub()` when both the result
  and the count are needed
- Add inline comments only where the regex flags or non-obvious decisions need
  explaining; avoid noise comments elsewhere
- All status/summary output goes to stderr; cleaned text goes to stdout

## Testing

```bash
uv run pytest -v          # 8 unit tests
uv run python test_manual.py  # 7 smoke tests
```
