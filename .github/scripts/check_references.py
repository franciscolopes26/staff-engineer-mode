#!/usr/bin/env python3
"""
check_references.py — validate that every @-reference inside the skill
points to a file that actually exists.

Examples of references the skill uses:
  @scripts/contracts.md
  @scripts/find-callers.sh
  @references/refactoring.md
  @playbooks/incident-response.md
  @anti-patterns/01-silent-swallow.md
  @examples/01-adding-feature-to-legacy.md
  @SECURITY.md
  @MINDSET.md
  @SKILL.md
  @bench.md

Run from repo root:
  python3 .github/scripts/check_references.py

Exit codes:
  0  all references resolve
  1  one or more broken references (printed)
"""

import re
import sys
from pathlib import Path

SKILL_DIR = Path("skills/staff-engineer-mode")

# Top-level skill files (siblings of SKILL.md)
TOP_LEVEL_FILES = {"SKILL.md", "MINDSET.md", "SECURITY.md", "bench.md"}

# Subdirectories under the skill that hold referenced content
SUBDIRS = ("scripts", "references", "playbooks", "anti-patterns", "examples")

REF_PATTERNS = [
    # @subdir/filename.{md,sh,py}
    re.compile(
        r"@(" + "|".join(SUBDIRS) + r")/([A-Za-z0-9_./-]+\.(?:md|sh|py))\b"
    ),
    # @TopLevel.md
    re.compile(r"@(SKILL|MINDSET|SECURITY|bench)\.md\b"),
]


def find_refs_in_file(path: Path):
    """Yield (line_no, raw_ref, resolved_path) for every @-ref in path."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pat in REF_PATTERNS:
            for m in pat.finditer(line):
                raw = m.group(0)
                if raw.startswith("@SKILL.md") or raw.startswith("@MINDSET.md") \
                        or raw.startswith("@SECURITY.md") or raw.startswith("@bench.md"):
                    rel = raw[1:]
                else:
                    rel = raw[1:]
                yield lineno, raw, SKILL_DIR / rel


def main() -> int:
    if not SKILL_DIR.exists():
        print(f"ERROR: expected {SKILL_DIR} to exist (run from repo root)")
        return 2

    broken = []
    checked = 0

    for md in SKILL_DIR.rglob("*.md"):
        for lineno, raw, target in find_refs_in_file(md):
            checked += 1
            if not target.exists():
                broken.append((md, lineno, raw, target))

    if broken:
        print(f"FAIL: {len(broken)} broken @-reference(s) out of {checked} checked\n")
        for md, lineno, raw, target in broken:
            print(f"  {md}:{lineno}: '{raw}' → no file at {target}")
        print()
        print("Each @-reference in the skill must resolve to a real file.")
        print("Fix by either creating the target file or correcting the path.")
        return 1

    print(f"OK: all {checked} @-reference(s) resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
