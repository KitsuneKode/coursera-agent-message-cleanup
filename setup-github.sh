#!/usr/bin/env bash
# setup-github.sh — Sets GitHub repo description, topics, and visibility.
# Run after pushing: bash setup-github.sh

set -e

REPO="kitsunekode/coursera-agent-message-cleanup"

echo "Setting GitHub description..."
gh repo edit "$REPO" \
  --description "Removes Coursera AI agent compliance boilerplate from copied quiz text. Clipboard-first CLI tool for macOS, Windows, and Linux."

echo "Setting GitHub topics..."
gh repo edit "$REPO" \
  --add-topic "coursera" \
  --add-topic "cli-tool" \
  --add-topic "clipboard" \
  --add-topic "text-cleanup" \
  --add-topic "python-cli" \
  --add-topic "boilerplate-removal" \
  --add-topic "academic-integrity" \
  --add-topic "productivity" \
  --add-topic "ai-agents" \
  --add-topic "quiz" \
  --add-topic "education" \
  --add-topic "pyperclip"

echo "Setting repo visibility and defaults..."
gh repo edit "$REPO" \
  --public \
  --enable-issues \
  --enable-wiki

echo "Done. View at: https://github.com/$REPO"
