#!/usr/bin/env python3
"""Check relative Markdown links in first-party pack documentation."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_ROOT = REPO_ROOT / "astrid" / "packs"
LINK_RE = re.compile(
    r"!?\[[^\]]*\]\((?:<([^>]+)>|([^)]*))\)"
    r"|^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)",
    re.MULTILINE,
)
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def _without_fenced_code(text: str) -> str:
    lines = text.splitlines(keepends=True)
    kept: list[str] = []
    fence: str | None = None
    for line in lines:
        match = FENCE_RE.match(line)
        if fence is None:
            if match:
                fence = match.group(1)[0]
                kept.append("\n" if line.endswith("\n") else "")
            else:
                kept.append(line)
            continue
        if match and match.group(1)[0] == fence:
            fence = None
        kept.append("\n" if line.endswith("\n") else "")
    return "".join(kept)


def _target(match: re.Match[str]) -> str:
    value = match.group(1) or match.group(2) or match.group(3) or ""
    value = value.strip()
    if value.startswith("<") and value.endswith(">"):
        value = value[1:-1]
    else:
        value = value.split(maxsplit=1)[0] if value else ""
    return value


def main() -> int:
    files = sorted(DOCS_ROOT.glob("**/docs/**/*.md"))
    broken: list[tuple[Path, int, str]] = []
    for path in files:
        content = path.read_text(encoding="utf-8")
        searchable = _without_fenced_code(content)
        for match in LINK_RE.finditer(searchable):
            target = _target(match)
            if not target or target.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            relative = target.split("#", 1)[0].split("?", 1)[0]
            if not relative:
                continue
            if not (path.parent / relative).exists():
                line = searchable.count("\n", 0, match.start()) + 1
                broken.append((path.relative_to(REPO_ROOT), line, target))

    print(f"checked {len(files)} Markdown files; {len(broken)} broken relative links")
    for path, line, target in broken:
        print(f"{path}:{line}: {target}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
