# R2/G5 inverse orientation investigation (1416)

G5 DRAFT ONLY; P1 NO-GO. No merge requested.

Ownership: only `astrid/sdk/timeline/inverse.py:apply_inverse/_restore_write`,
`astrid/sdk/timeline/_root_inverse.py` inverse preparation helpers, or
`astrid/sdk/timeline/_commit_patch.py:CommitPatch.after/finish` inverse-record
construction as causally proven, plus a focused new regression file. No edits
in commit.py (R1 worker1403 execution; redo1404 document_from_bundle302–311 /
historical child compiler inputs). No Runtime or native_restructure edits.

Read PLAN, C0 request and inverse contract, diagnosis1358 and independent1406.
Offline reconstruction on the lossless retained input currently contradicts
one key statement in both reports: source event117/131 accepted restructure
revision caa332 has config e6d3 and THREE occurrences; previous event129
revision a58d has config3261 and ONE occurrence. Thus the digest names
flat/split were reversed in the reports. Source native captures and the
reconstructed candidate both currently agree in orientation with actual
immutable input. Investigating the exact Runtime refusal offline before any
product repair; no speculative swap or guard waiver will be made.

Harness tmpdir is a pointer file to `/tmp/w-08581704c3`; scratch uses that
private directory without replacing the pointer (D18 setup interpretation).
