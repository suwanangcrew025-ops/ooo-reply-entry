#!/usr/bin/env python3
"""Out-of-office one-liner entry for make.fun.

The program copies the single out-of-office reply stored in ooo.txt to
/output/entry.txt, where the sealed gate scorer reads it. The reply has
to read like a real away message a person would gladly switch on, and
be funny on the first read with no setup: the sender is away until
Monday, the fern on their desk is in charge now, and the joke turns on
what the fern has already survived — three managers, two mergers, and
one fire drill it slept through. A concrete desk plant, a specific run
of office disasters, and the turn at the end; every word earns its
place inside the 160 character cap.

Only the Python standard library is used, so the program runs the same
way in the grader sandbox as it does here, and the output is byte for
byte the stored reply on every run.
"""

import os
import sys
from pathlib import Path

CAP = 160
TEXT_FILE = "ooo.txt"
OUT_FILE = "entry.txt"


def load_reply(here):
    """Read the stored reply, dropping only its trailing newline."""
    raw = (Path(here) / TEXT_FILE).read_bytes()
    line = raw.decode("utf-8")
    if line.endswith("\n"):
        line = line[:-1]
    if not line.strip():
        raise ValueError("ooo.txt holds no reply")
    if len(line) >= CAP:
        raise ValueError("reply is %d characters, cap is under %d"
                         % (len(line), CAP))
    return line


def store_reply(line):
    """Write the reply where the gate scorer reads it, then verify it."""
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / OUT_FILE
    encoded = line.encode("utf-8")
    target.write_bytes(encoded)
    if target.read_bytes() != encoded:
        raise ValueError("written entry differs from ooo.txt")
    return target


def main():
    here = Path(__file__).resolve().parent
    try:
        line = load_reply(here)
        target = store_reply(line)
    except (OSError, UnicodeDecodeError, ValueError) as problem:
        sys.stderr.write("entry failed: %s\n" % problem)
        return 1
    sys.stdout.write("wrote %d characters to %s\n" % (len(line), target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
