## Result: FAIL

The six earlier-refusal adaptations pass behaviorally, but the review fails the strict Pyright requirement.

- Targeted pytest: `14 passed`
- Ruff: passed
- In-memory compile: passed
- `git diff --check`: passed
- Six cases preserved: `None`, `[3, 2]`, `"3/2"` × child/parent
- SQL/CAS no-write assertions unchanged
- All 8 non-target function ASTs unchanged; all 3 retained read/speed/timing ASTs unchanged
- No skips, xfails, deselection, broad exception tuples, or production/schema/client changes
- Real `RuntimeService.publish_parent_composition()` directly invokes the 410 retirement guard before reading speed; retained reader/HTTP paths remain covered

Strict Pyright comparison using the exact command `pyright tests/test_timeline_null_speed_retained.py`:

- Parent: 10 diagnostics
- Current: 11 diagnostics
- New diagnostic: `reportOptionalSubscript` at the added `error.value.details["reason"]` assertion
- Therefore: one new diagnostic identity/multiplicity; author’s weaker changed-line check was insufficient.

Source: base `458595850c354f4403dabc58a72b98bebbc2c3a3`; current `213d530abfa6245b77818848c41d01103904f0b4`; current tree `6ba24f03b5e1b34ce189a6313abdcce4f2352593`.

No full suite was run. No reviewer tracked edits were made. Commit message and `DONE` marker created.

Recommended next step: resolve the new Pyright diagnostic, then repeat this narrow review.