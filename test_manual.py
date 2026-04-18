#!/usr/bin/env python3
"""
Manual smoke-test runner for coursera-agent-message-cleanup.

Runs a battery of invocations against the script and checks expected output.
Useful for quick validation after changes, especially on a new OS/platform.

Usage:
    uv run python test_manual.py
"""

import subprocess
import sys
import os

SCRIPT = os.path.join(os.path.dirname(__file__), "coursera_agent_message_cleanup.py")
TEST_FILE = os.path.join(os.path.dirname(__file__), "test.txt")

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

passed = 0
failed = 0


def run_test(label: str, args: list[str], check_stdout_contains: str | None = None, check_stderr_contains: str | None = None, check_stdout_absent: str | None = None, check_stderr_absent: str | None = None, expect_rc: int = 0, stdin_data: str | None = None) -> None:
    global passed, failed
    cmd = [sys.executable, SCRIPT] + args
    result = subprocess.run(cmd, capture_output=True, text=True, input=stdin_data)
    ok = True
    reasons: list[str] = []

    if result.returncode != expect_rc:
        ok = False
        reasons.append(f"exit code {result.returncode} != {expect_rc}")

    if check_stdout_contains and check_stdout_contains not in result.stdout:
        ok = False
        reasons.append(f"stdout missing '{check_stdout_contains}'")

    if check_stderr_contains and check_stderr_contains not in result.stderr:
        ok = False
        reasons.append(f"stderr missing '{check_stderr_contains}'")

    if check_stdout_absent and check_stdout_absent in result.stdout:
        ok = False
        reasons.append(f"stdout should NOT contain '{check_stdout_absent}'")

    if check_stderr_absent and check_stderr_absent in result.stderr:
        ok = False
        reasons.append(f"stderr should NOT contain '{check_stderr_absent}'")

    if ok:
        passed += 1
        print(f"  {GREEN}PASS{RESET} {label}")
    else:
        failed += 1
        print(f"  {RED}FAIL{RESET} {label}")
        for r in reasons:
            print(f"         {r}")


with open(TEST_FILE, "r") as fh:
    test_content = fh.read()

print("Running manual smoke tests...\n")

# --- Default (no flags): clipboard only (stdin pipe simulates clipboard input) ---
run_test("default mode: stdin -> clipboard", [], check_stderr_contains="clipboard", stdin_data=test_content)

# --- Screen + clipboard (stdin pipe) ---
run_test("--screen: stdout + clipboard", ["--screen"], check_stdout_contains="Question 1", check_stderr_contains="clipboard", stdin_data=test_content)

# --- File output + clipboard (stdin pipe) ---
out_path = os.path.join(os.path.dirname(__file__), ".test_output.txt")
if os.path.exists(out_path):
    os.remove(out_path)
run_test("--output: file + clipboard", ["-o", out_path], check_stderr_contains="file", stdin_data=test_content)
if os.path.exists(out_path):
    with open(out_path, "r") as fh:
        content = fh.read()
    if "Question 1" in content and "You are a helpful AI assistant" not in content:
        passed += 1
        print(f"  {GREEN}PASS{RESET} file content is correct")
    else:
        failed += 1
        print(f"  {RED}FAIL{RESET} file content is incorrect")
    os.remove(out_path)
else:
    failed += 1
    print(f"  {RED}FAIL{RESET} output file was not created")

# --- File input ---
run_test("-f file input: clipboard + terminal", ["-f", TEST_FILE, "--screen"], check_stdout_contains="Question 1", check_stderr_contains="clipboard")

# --- All three: screen + clipboard + file ---
if os.path.exists(out_path):
    os.remove(out_path)
run_test("all three: screen + clipboard + file", ["-f", TEST_FILE, "--screen", "-o", out_path], check_stdout_contains="Question 1", check_stderr_contains="file", stdin_data=test_content)
if os.path.exists(out_path):
    os.remove(out_path)

# --- Stdin pipe ---
run_test("stdin pipe works", [], check_stderr_contains="Removed 16 occurrence(s)", stdin_data=test_content)

# --- Missing file ---
run_test("missing file gives error", ["-f", "nonexistent.txt"], expect_rc=1)

# --- No boilerplate input ---
run_test("plain text returns 0 occurrences", ["--screen"], check_stdout_contains="Removed 0 occurrence(s)", stdin_data="Just some plain text without boilerplate\n")

# --- Help flag ---
run_test("--help works", ["--help"], check_stdout_contains="Remove Coursera AI agent boilerplate")

# --- Version flag ---
run_test("--version works", ["--version"], check_stdout_contains="coursera-cleanup")

print(f"\n{'='*40}")
print(f"Results: {passed} passed, {failed} failed")
if failed:
    sys.exit(1)
