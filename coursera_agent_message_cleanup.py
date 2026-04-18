#!/usr/bin/env python3
"""
coursera_agent_message_cleanup.py

Removes the Coursera AI agent compliance/academic-integrity boilerplate
from question text and outputs the cleaned result.

Default flow (fastest):
    1. Copy quiz text from Coursera (Ctrl+C)
    2. Run: coursera-cleanup
    3. Cleaned text is on your clipboard — paste wherever (Ctrl+V)

Usage:
    coursera-cleanup                           # clipboard -> clean -> clipboard (default)
    coursera-cleanup -f questions.txt           # read from file
    coursera-cleanup < file.txt                 # from stdin redirect
    cat file.txt | coursera-cleanup             # pipe
    coursera-cleanup -f q.txt --screen          # also print to terminal
    coursera-cleanup -f q.txt -o out.txt        # also write to file
    coursera-cleanup -f q.txt --screen -o f.txt # terminal + file

Install (no uv required):
    pip install pyperclip
    python coursera_agent_message_cleanup.py -f questions.txt
"""

import argparse
import platform
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

# Version from pyproject.toml (kept in sync manually)
__version__ = "1.3.0"


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


_CLIPBOARD_ERROR_HINTS = {
    "Linux": (
        "On Linux, pyperclip requires xclip/xsel (X11) or wl-clipboard (Wayland).\n"
        "  sudo apt install xclip        # Debian/Ubuntu (X11)\n"
        "  sudo apt install wl-clipboard  # Debian/Ubuntu (Wayland)\n"
        "  sudo dnf install wl-clipboard  # Fedora"
    ),
    "Darwin": "On macOS, pyperclip uses the built-in pbcopy. Should work out of the box.",
    "Windows": "On Windows, pyperclip uses the built-in clipboard API. Should work out of the box.",
}


def _read_clipboard() -> str | None:
    """Read from clipboard. Returns None on failure."""
    try:
        return pyperclip.paste()
    except Exception:
        return None


def _write_clipboard(text: str) -> bool:
    """Copy text to clipboard. Returns True on success, False on failure."""
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        system = platform.system()
        hint = _CLIPBOARD_ERROR_HINTS.get(system, "")
        print(f"Warning: Failed to copy to clipboard: {e}", file=sys.stderr)
        if hint:
            print(hint, file=sys.stderr)
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="coursera-cleanup",
        description="Remove Coursera AI agent boilerplate from copied quiz text.",
        epilog=(
            "DEFAULT FLOW (no flags):\n"
            "  Reads from clipboard -> cleans -> writes back to clipboard.\n"
            "  Copy from Coursera (Ctrl+C), run this, paste anywhere (Ctrl+V).\n\n"
            "OUTPUT FLAGS (additive — combine any):\n"
            "  --screen       Also print cleaned text to terminal\n"
            "  --output FILE  Also write cleaned text to a file\n\n"
            "INPUT OPTIONS:\n"
            "  -f FILE        Read from file instead of clipboard\n"
            "  stdin          Pipe or redirect: cat file.txt | coursera-cleanup\n\n"
            "EXAMPLES:\n"
            "  coursera-cleanup                         # clipboard -> clipboard (default)\n"
            "  coursera-cleanup --screen                # clipboard -> clipboard + terminal\n"
            "  coursera-cleanup -f questions.txt        # file -> clipboard\n"
            "  coursera-cleanup -f q.txt --screen       # file -> clipboard + terminal\n"
            "  coursera-cleanup -f q.txt -o cleaned.txt # file -> clipboard + file\n"
            "  cat q.txt | coursera-cleanup             # stdin -> clipboard\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Read input from FILE instead of clipboard",
        metavar="FILE",
    )
    parser.add_argument(
        "-s",
        "--screen",
        action="store_true",
        help="Print cleaned text to terminal (additive, always available)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write cleaned text to FILE (additive)",
        metavar="FILE",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Determine input source: file > stdin pipe > clipboard (default)
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                raw = fh.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied: {args.file}", file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    else:
        raw = _read_clipboard()
        if raw is None:
            print("Error: Could not read from clipboard.", file=sys.stderr)
            system = platform.system()
            hint = _CLIPBOARD_ERROR_HINTS.get(system, "")
            if hint:
                print(hint, file=sys.stderr)
            sys.exit(1)
        if not raw.strip():
            print("Clipboard is empty. Copy some quiz text from Coursera first.", file=sys.stderr)
            sys.exit(1)

    if not raw.strip():
        print("No input provided. Exiting.")
        sys.exit(0)

    cleaned, count = remove_coursera_message(raw)

    # Always write to clipboard by default (primary output)
    # Additional destinations are additive
    status_parts = []

    clip_ok = _write_clipboard(cleaned)
    if clip_ok:
        status_parts.append("clipboard")

    if args.screen:
        print(cleaned)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(cleaned)
            status_parts.append(f"file: {args.output}")
        except PermissionError:
            print(f"Error: Permission denied: {args.output}", file=sys.stderr)
            sys.exit(1)

    # Summary to stderr so stdout stays clean for piping
    summary = f"Removed {count} occurrence(s)."
    if status_parts:
        summary += " Sent to " + ", ".join(status_parts) + "."
    else:
        summary += " Clipboard failed — check stderr above."
    print(summary, file=sys.stderr)


if __name__ == "__main__":
    main()
