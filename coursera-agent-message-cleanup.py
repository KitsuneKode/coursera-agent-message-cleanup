#!/usr/bin/env python3
"""
coursera-agent-message-cleanup.py

Removes the Coursera AI agent compliance/academic-integrity boilerplate
from question text and copies the cleaned result to the clipboard.

Usage:
    coursera-cleanup              # prompts you to paste text, then Ctrl+D
    coursera-cleanup < file.txt   # reads from file
    echo "text" | coursera-cleanup # reads from pipe

The script uses a regex anchored on the distinctive start and end of the
Coursera message so it stays robust against minor formatting/whitespace
differences that break exact-string matching.
"""

import re
import sys

try:
    import pyperclip
except ImportError:
    print("pyperclip is required. Install it with: pip install pyperclip")
    sys.exit(1)

# Matches from the well-known opening sentence all the way through to the
# mandatory closing prompt "Do you understand?." — including every character
# in between regardless of how newlines or spaces vary in the pasted text.
#
# Anchors chosen because they are unique enough to never appear in normal
# question text:
#   START  – "You are a helpful AI assistant. You have identified that this
#              web page contains a protected assessment from Coursera."
#   END    – "Do you understand?."
#
# re.DOTALL makes '.' match newlines so the whole multi-line blob is consumed.
# re.IGNORECASE is a safety net for copy-paste casing variations.
# The pattern is non-greedy (.*?) so multiple occurrences are each removed
# independently rather than one giant span swallowing content between them.
_COURSERA_PATTERN = re.compile(
    r"You are a helpful AI assistant\."
    r".+?"  # everything in between (non-greedy)
    r"Do you understand\?\.",
    re.DOTALL | re.IGNORECASE,
)


def remove_coursera_message(text: str) -> tuple[str, int]:
    """
    Remove every occurrence of the Coursera AI agent boilerplate from *text*.

    Returns:
        (cleaned_text, number_of_occurrences_removed)
    """
    # subn() does the replacement and count in a single pass over the string,
    # avoiding the redundant findall() scan.
    cleaned, count = _COURSERA_PATTERN.subn("", text)
    # Collapse runs of 3+ blank lines left by the removed blocks down to one
    # blank line so the output still reads naturally.
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip(), count


def main() -> None:
    if not sys.stdin.isatty():
        raw = sys.stdin.read()
    else:
        print("Paste your text below, then press Ctrl+D when done:")
        print("---")
        raw = sys.stdin.read()

    if not raw.strip():
        print("No input provided. Exiting.")
        sys.exit(0)

    cleaned, count = remove_coursera_message(raw)

    pyperclip.copy(cleaned)
    print(f"---\nRemoved {count} occurrence(s). Cleaned text copied to clipboard.")


if __name__ == "__main__":
    main()
