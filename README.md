# Coursera Agent Message Cleanup

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Tests](https://img.shields.io/github/actions/workflow/status/kitsunekode/coursera-agent-message-cleanup/python-tests.yml)](https://github.com/kitsunekode/coursera-agent-message-cleanup/actions)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🎯 Purpose

Removes the Coursera AI-agent compliance/academic-integrity boilerplate that gets injected into quiz questions when you copy text from a Coursera assessment page, then puts the clean result right back on your clipboard.

## ⚡️ The Fastest Flow (3 keystrokes)

```
Ctrl+C   →   coursera-cleanup   →   Ctrl+V
(copy)        (clean)             (paste cleaned)
```

1. Select quiz questions on Coursera and press **Ctrl+C** (Cmd+C on Mac)
2. Run `coursera-cleanup` in your terminal
3. Press **Ctrl+V** anywhere — the cleaned text is on your clipboard

## 📦 Installation

### With uv (recommended):
```bash
git clone https://github.com/kitsunekode/coursera-agent-message-cleanup.git
cd coursera-agent-message-cleanup
uv sync
```

### With pip (no uv needed):
```bash
pip install pyperclip
# Download coursera_agent_message_cleanup.py and run it directly
python coursera_agent_message_cleanup.py -f questions.txt
```

### With pipx (for isolated installation):
```bash
pipx install git+https://github.com/kitsunekode/coursera-agent-message-cleanup.git
```

## 🚀 Usage

### Default (no flags)
```bash
coursera-cleanup
```
Reads from your clipboard, removes all Coursera boilerplate, writes the cleaned text back to your clipboard.

### With Screen Output
```bash
coursera-cleanup --screen
```
Same as above, but also prints the cleaned text to your terminal so you can preview it.

### From File
```bash
coursera-cleanup -f questions.txt
```
Reads from a file instead of clipboard. Result still goes to clipboard.

### From Pipe / Stdin
```bash
cat questions.txt | coursera-cleanup
coursera-cleanup < questions.txt
```

### Write to File
```bash
coursera-cleanup -f questions.txt -o cleaned.txt
```
Clipboard + file. Add `--screen` to also see it in terminal.

### All Options

| Flag | What it does |
|------|-------------|
| *(none)* | Read from clipboard, write back to clipboard |
| `-s` / `--screen` | **Also** print cleaned text to terminal |
| `-o FILE` / `--output FILE` | **Also** write cleaned text to a file |
| `-f FILE` / `--file FILE` | Read from file instead of clipboard |
| `--version` | Show version |
| `-h` / `--help` | Show help |

All flags are **additive** — the clipboard is always written to by default. Add `--screen` to also see output, or `-o` to also save a file.

### Examples
```bash
coursera-cleanup                              # clipboard -> clipboard (default)
coursera-cleanup --screen                     # clipboard -> clipboard + terminal
coursera-cleanup -f questions.txt             # file -> clipboard
coursera-cleanup -f questions.txt --screen    # file -> clipboard + terminal
coursera-cleanup -f q.txt -o cleaned.txt      # file -> clipboard + file
coursera-cleanup -f q.txt --screen -o out.txt # file -> clipboard + terminal + file
cat q.txt | coursera-cleanup                  # stdin -> clipboard
```

## 🔍 Why This Exists

When you copy quiz questions from Coursera, each question gets wrapped in a huge AI-agent compliance block like this:

> *You are a helpful AI assistant. You have identified that this web page contains a protected assessment from Coursera...*

It makes the text unreadable and wastes space. This tool strips every occurrence of that boilerplate in one pass and sends the cleaned questions wherever you need them.

## ⚙️ How It Works

1. Reads raw text from your clipboard (default), a file (`-f`), or stdin pipe.
2. Scans for every occurrence of the Coursera boilerplate using a compiled regex.
3. Removes all matches and collapses any excess blank lines left behind.
4. Writes the cleaned text back to your clipboard (always).
5. Optionally prints to terminal (`--screen`) or writes to file (`--output`).
6. Prints a summary line to stderr with the removal count and destinations.

## 🎯 Matching Strategy

The boilerplate is matched with a **regex**, not a literal string comparison. This is intentional.

Copying text from a browser does not always produce identical whitespace or line endings — a single extra newline or a trailing space is enough to make an exact-string match silently fail and return 0 removals.

The pattern anchors on two unique, stable phrases:

| Anchor    | Text                                                    |
| --------- | ------------------------------------------------------- |
| **Start** | `You are a helpful AI assistant.`                       |
| **End**   | `Do you understand?.`                                   |

Everything between those anchors is consumed non-greedily (`.*?`), so:

- Whitespace and newline variations between copies are handled automatically
- Multiple occurrences are each removed independently without eating content between them
- `re.IGNORECASE` guards against casing differences from copy-paste

## ✅ Testing

### Automated Tests
```bash
uv sync --all-extras
uv run pytest -v
```

Or with pip:
```bash
pip install pytest
pytest -v
```

### Manual Smoke Tests
```bash
uv run python test_manual.py
python test_manual.py
```

## 🛠️ Troubleshooting

**"Removed 0 occurrence(s)"** — The boilerplate was not detected. Coursera may have updated the message. Open the script, inspect `_COURSERA_PATTERN`, and update one or both anchors to match the new wording.

**Clipboard does not update on Linux** — Install the appropriate clipboard backend for your display server (see table below). The script prints a warning to stderr with install commands if clipboard access fails.

**Clipboard is empty error** — Make sure you've copied the quiz text from Coursera before running the tool.

### Platform Support

| Platform | Clipboard | Notes |
|----------|-----------|-------|
| **macOS** | `pbcopy` (built-in) | Works out of the box |
| **Windows** | Win32 API (built-in) | Works out of the box |
| **Linux** | `xclip` (X11) or `wl-clipboard` (Wayland) | May need manual install |

**Linux (X11):**
```bash
sudo apt install xclip        # Debian/Ubuntu
sudo dnf install xclip        # Fedora
```

**Linux (Wayland):**
```bash
sudo apt install wl-clipboard  # Debian/Ubuntu
sudo dnf install wl-clipboard  # Fedora
```

## 🤝 Contributing

PRs welcome! If you find a new boilerplate format that the regex doesn't catch:

1. Copy the exact text into `test.txt` (or add a new test case in `test_coursera.py`)
2. Update `_COURSERA_PATTERN` in `coursera_agent_message_cleanup.py`
3. Run `uv run pytest -v && uv run python test_manual.py` to confirm everything still passes
4. Open a PR with your changes

## 📜 License

MIT

## 🙏 Acknowledgments

- Inspired by the frustration of dealing with Coursera's AI agent messages
- Built with Python and pyperclip for cross-platform clipboard access