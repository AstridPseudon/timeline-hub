"""Read-only M0 observations; no proposed extension implementation is executed.

Run from the Agent worktree with Python's standard library only. Frozen source
is read through git show, never checked out or imported through its package.
"""

import ast
import json
import re
import subprocess
import sys
import types
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
R4_REPO = "/home/user/peteromallet/astrid-agent"
R4_REF = "origin/codex/handover-timeline-r4-20261019-candidate-sdk"


def frozen(path):
    return subprocess.check_output(
        ["git", "-C", R4_REPO, "show", f"{R4_REF}:{path}"], text=True
    )


def moments():
    module = types.ModuleType("m0_frozen_moments")
    sys.modules[module.__name__] = module
    source = frozen("astrid/core/timeline/moments.py")
    exec(compile(source, "<frozen R4 moments>", "exec"), module.__dict__)
    return module


class ExistingSeamObservations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mo = moments()

    def test_beat_ordinal_changes_identity_when_an_earlier_beat_is_inserted(self):
        ctx = types.SimpleNamespace(fps=30, cut_start=lambda _: 0)
        ctx.beats = lambda _: [1.0, 2.0, 3.0]
        self.assertEqual(self.mo.resolve("beat 2 after c1", ctx), 2.0)
        ctx.beats = lambda _: [0.5, 1.05, 2.05, 3.05]
        self.assertEqual(self.mo.resolve("beat 2 after c1", ctx), 1.05)

    def test_exact_source_word_and_clip_anchor_grammar_round_trips(self):
        for text in (
            'source-word "doc" "lineage" "revision" '
            '"occurrence:opening/clip:vo" "digest" "word-7"',
            'clip-start "occurrence:opening/clip:title" +2f',
        ):
            moment = self.mo.parse(text)
            self.assertEqual(self.mo.parse(self.mo.format_moment(moment)), moment)
        self.assertEqual(self.mo.parse("marker").kind, "word")

    def test_sheet_parser_retains_version_but_does_not_retain_scope(self):
        # Only execute the existing pure parser helpers. No Checkout, pack,
        # schema, media-handle or third-party imports are needed for these rows.
        source = (ROOT / "astrid/sdk/timeline_sheet.py").read_text(encoding="utf-8")
        names = {
            "parse_sheet", "_strip_comment", "_parse_header", "_canon", "_parse_layer",
            "_tokens", "_read_seconds", "_read_value", "_with_text",
        }
        tree = ast.parse(source)
        body = [
            node for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name in names
        ]
        namespace = dict(
            re=re, json=json, mo=self.mo, Any=Any, ELIDED=object(),
            CLAUSES=("on", "until", "for"), SheetError=ValueError,
        )
        exec(compile(ast.Module(body=body, type_ignores=[]), "<main sheet parser>", "exec"), namespace)
        parsed = namespace["parse_sheet"](
            "film P · TL · 1920×1080 · 24 fps · v abcdef123456\n"
            "scope c1 (1 cuts): apply changes only these cuts\n"
            "0.00 ┃ c1\n"
            'type title type "hello" for 12f\n'
        )
        self.assertEqual(parsed["version"], "abcdef123456")
        self.assertEqual(parsed["cuts"][0]["layers"][0]["for"], 0.5)
        self.assertNotIn("scope", parsed)
        self.assertIs(namespace["_read_value"]("…", 1), namespace["ELIDED"])

    def test_pack_v3_has_metadata_slot_but_no_top_level_extensions_slot(self):
        schema = json.loads(
            (ROOT / "astrid/core/pack/schemas/v3/pack.json").read_text(encoding="utf-8")
        )
        props = schema["properties"]
        self.assertFalse(schema["additionalProperties"])
        self.assertNotIn("extensions", props)
        action = props["actions"]["additionalProperties"]
        self.assertEqual(action["properties"]["metadata"], {"type": "object"})
        rendering_types = props["rendering"]["additionalProperties"]["properties"]["type"]["enum"]
        self.assertIn("element", rendering_types)


if __name__ == "__main__":
    unittest.main()
