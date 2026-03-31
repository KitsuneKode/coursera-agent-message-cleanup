# Coursera Agent Message Cleanup

Removes the Coursera AI agent compliance/academic-integrity boilerplate text that gets pasted along with quiz questions when copying from Coursera assessment pages.

## Quick Start

```bash
# Clone and install
git clone <repo-url>
cd coursera-agent-message-cleanup
uv sync

# Run (prompts for text input, cleans, copies to clipboard)
uv run python coursera-agent-message-cleanup.py

# Or pipe from a file
uv run python coursera-agent-message-cleanup.py < questions.txt
```

## Usage

| Method | Command |
|--------|---------|
| Interactive | `uv run python coursera-agent-message-cleanup.py` (paste text, then Ctrl+D) |
| File input | `uv run python coursera-agent-message-cleanup.py < file.txt` |
| Pipe | `cat file.txt \| uv run python coursera-agent-message-cleanup.py` |

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## How It Works

1. Reads text from stdin (interactive paste or piped/file input)
2. Removes every occurrence of the Coursera AI agent boilerplate message
3. Collapses excess blank lines left behind
4. Copies the cleaned text back to clipboard
5. Prints a count of removed occurrences

## License

MIT
