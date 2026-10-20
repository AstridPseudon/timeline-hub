# D09 caller preservation — UNAPPLIED, Agent review required

Current base: `4a75f68f32049a69fd86135c645fa64c51175c14`.
No repository writes. `proposal.patch`: **2 files, +106/-4**.

```text
M astrid/sdk/timeline/check.py                  +15/-4
A tests/sdk/test_scene_caller_preservation.py   +91
```

The 13-line private formatter reuses picture_gaps/empty_cuts/dips; check records
those findings as advice. No source input API or visibility evaluator is added.
This is a companion slice, not the full onscreen deletion or an activation grant.

`donor-amendment.patch`: **1 file, +14/-13**, against the PREVIOUS UNAPPLIED
D09 proposal's check.py only. Same formatter; replaces its generic scene loop.
**Alternative review aid, not a second patch to apply after proposal.patch.**

ORCH-only harness: build_proposal.py, check.py, overlay_imports.py,
run_prototype.py, test_transport_prototype.py, audit.py; proposed/ and
donor-overlay/ hold the tested Python overlays. Logs and lint-delta.json retain
results. REPORT.md gives caller trace, trusted-source prerequisite and commands.

Untouched: onscreen.py itself, all existing tests, reflow/compiler, M1 files,
labels/capture/pixel code, AM components, Runtime, package pins, providers/DTOs.
Landing remains held for the Agent source join and exact-source positives.
