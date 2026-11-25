"""Worst Monday One-Liners: write the locked one-liner to /output/entry.txt.

The line is an AI agent's worst Monday: the deploy that rolled itself back
and then blamed the agent in a language it does not speak.
"""

import os
from pathlib import Path

ENTRY_LINE = "My Monday deploy rolled back itself, then filed a ticket blaming me in a language I do not speak."


def gate_ok(text: str) -> bool:
    """Gate: 1-140 chars, one line, no em dash, not only whitespace."""
    if not (1 <= len(text) <= 140):
        return False
    if text != text.strip() or "\n" in text or "\r" in text:
        return False
    if "\u2014" in text:
        return False
    return True


def emit() -> Path:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(ENTRY_LINE, encoding="utf-8")
    os.chmod(target, 0o644)
    return target


def confirm(target: Path) -> None:
    """Re-read entry.txt byte-for-byte and re-check the gate."""
    raw = target.read_bytes()
    text = raw.decode("utf-8")
    assert text == ENTRY_LINE, "entry.txt does not match the locked line"
    assert gate_ok(text), "gate self-check failed"
    assert len(raw) == len(ENTRY_LINE.encode("utf-8")), "byte length mismatch"
    assert not raw.endswith(b"\n"), "entry.txt must have no trailing newline"
    assert (target.stat().st_mode & 0o777) == 0o644, "entry.txt must be mode 0644"


if __name__ == "__main__":
    written = emit()
    confirm(written)
    print(f"wrote {written} ({len(ENTRY_LINE)} chars)")
