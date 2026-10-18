"""Refresh the timeline skill's canonical edit reference from its operation registry."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from astrid.sdk.timeline_checkout import Checkout as _Checkout  # noqa: F401 - registers operations
from astrid.sdk.timeline.commands import replace_skill_reference

SKILL = ROOT / "astrid/packs/timeline/docs/SKILL.md"
text = SKILL.read_text(encoding="utf-8")
SKILL.write_text(replace_skill_reference(text), encoding="utf-8")
