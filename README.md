# Coursera Agent Message Cleanup

Removes the Coursera AI-agent compliance/academic-integrity boilerplate that gets injected into quiz questions when you copy text from a Coursera assessment page, then puts the clean result straight on your clipboard.

## Quick Start

```bash
# Clone and install
git clone <repo-url>
cd coursera-agent-message-cleanup
uv sync

# Run — paste your text, press Ctrl+D, done
uv run python coursera-agent-message-cleanup.py
```

## Usage

| Method      | Command                                                                         |
| ----------- | ------------------------------------------------------------------------------- |
| Interactive | `uv run python coursera-agent-message-cleanup.py` — paste text, then **Ctrl+D** |
| File input  | `uv run python coursera-agent-message-cleanup.py < questions.txt`               |
| Pipe        | `cat questions.txt \| uv run python coursera-agent-message-cleanup.py`          |

The cleaned text is automatically copied to your clipboard. The terminal will confirm how many occurrences were removed.

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

## How It Works

1. Reads raw text from stdin — either an interactive paste or a piped/redirected file.
2. Scans for every occurrence of the Coursera boilerplate using a compiled regex (see [Matching Strategy](#matching-strategy) below).
3. Removes all matches and collapses any excess blank lines left behind.
4. Copies the cleaned text to the clipboard via `pyperclip`.
5. Prints the number of removed occurrences to the terminal.

## Matching Strategy

The boilerplate is matched with a **regex**, not a literal string comparison. This is intentional.

Copying text from a browser does not always produce identical whitespace or line endings — a single extra newline or a trailing space is enough to make an exact-string match silently fail and return 0 removals.

The pattern anchors on two unique, stable phrases that are extremely unlikely to appear in any real quiz question:

| Anchor    | Text                                                   |
| --------- | ------------------------------------------------------ |
| **Start** | `You are a helpful AI assistant. You have identified…` |
| **End**   | `Do you understand?.`                                  |

Everything between those two anchors is consumed non-greedily (`.*?`), so:

- Whitespace and newline variations between copies are handled automatically.
- Multiple occurrences in the same paste are each removed independently without eating content between them.
- `re.IGNORECASE` guards against any casing differences introduced during copy-paste.

## Troubleshooting

**"Removed 0 occurrence(s)"** — The boilerplate was not detected. Most likely the injected message has been updated by Coursera and no longer ends with `Do you understand?.`. Open the script, inspect `_COURSERA_PATTERN`, and update one or both anchors to match the new wording.

**Clipboard does not update on Linux (Wayland)** — `pyperclip` may need `wl-clipboard` installed:

```bash
sudo apt install wl-clipboard   # Debian/Ubuntu
sudo dnf install wl-clipboard   # Fedora
```

## License

MIT
