## G5 child-anchor scope review

**PASS — scope finding only; no product/API approval.** Confirmed the exact
boundary as **OLD child writer vs NEW parent-only native carrier**.

- Old `Clip.nudge`/`Clip.on`/`retime` genuinely supports the retained child
  target `occ-film/clip:inside`, cut `c2`, `on='"second"'`, `at=4.6`.
- Current `clip.anchor` requires an exact typed transcript choice but rejects
  child `select` values at the schema and native handler; its adapters create
  parent targets only.
- The pure kernel's child-shaped `WordBinding` is caller-supplied capability,
  not an existing capture/carrier. `doc.patch` and the journal/emitter
  preserve physical data but do not select semantic words or mint authority.
- Frozen R4 transcript binding is independently pinned/admitted and a
  different format; it cannot be inferred into the current v1 route.

Packet SHA-256 verified:
`b07035a8594e0240c6e05c287eb7d6f83bb4afe0527833f6c992553a1f3f1726`.
The exact Sol evidence is reused: 3 PASS + 1 FAIL acceptance, 41 strict
guards, Ruff 2149/2149, private mypy 1912/1912, and clean vendor/artifact/diff
checks. The unchanged failed ["second"] positive was not rerun.

Focused command run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timing_compiler.py::test_binding_refusals_are_atomic_and_never_repair_by_same_text tests/sdk/test_timing_compiler.py::test_exact_binding_uses_selected_duplicate_word_and_preserves_authored_commands_and_clears tests/editing_conformance/test_commit_timing_validation.py::test_child_declarations_are_not_filtered_and_valid_relations_are_resolved
```

Result: **13 passed in 1.29s**.

No source/product/test/schema/generated/pin/contract/environment/dependency/
guard edits. No merge; G5 P1 remains NO-GO pending an explicit child-capture
contract decision. Detailed report:
`design/agent-G5-child-anchor-scope-review-1356.md`.

