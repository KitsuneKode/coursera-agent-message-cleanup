# AGENTS.md

## Project Overview

Coursera Agent Message Cleanup — a CLI tool that removes the Coursera AI agent compliance/academic-integrity boilerplate text from copied quiz questions and puts the cleaned result on the clipboard.

## Structure

```
coursera-agent-message-cleanup/
├── coursera-agent-message-cleanup.py  # Main script
├── pyproject.toml                     # Project config + deps
├── .gitignore
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
```

## Conventions

- No external network calls
- No comments unless asked
- Keep the script self-contained — single file, no submodules
- The boilerplate string to remove lives in `COURSERA_MESSAGE` constant at the top of the script
