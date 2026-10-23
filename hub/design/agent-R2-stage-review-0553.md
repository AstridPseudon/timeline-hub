# Agent R2 stage review 0553

**Result: scoped source PASS; joined acceptance pending.**

Reviewed exact port `9e6e9cbb5` atop `31a5e8d3c` with no product source changes. Only the assigned three paths differ. Their blobs match source `48d7c5973` exactly. The `CommitPatch.before` addition binds changed sequential command inputs to the physical image at that command's input boundary. The `CommitPatch.after` change starts inverse stages from the recorded first input closure and chains each subsequent stage from the prior output, so equal historical bytes cannot substitute for the authenticated first revision. The later current-fork helper remains separate and must be preserved on merge: `inverse_closure(bundle, sources) -> Closure(bundle, source_bundles=sources)`.

## Evidence

- Source controls: **PASS, 92 passed in 10.49s** using the exact scoped author command and read-only Runtime on `PYTHONPATH`.
- ABA controls: **PASS, 8 passed, 106 deselected in 4.63s**.
- Runtime forgery controls: **PASS, 5 passed, 68 deselected in 1.06s** from read-only Runtime HEAD `85dafdf`; the author’s exact Runtime-495 evidence was also 5 passed, but that temporary archive is gone.
- Scoped Ruff/mypy, normal Ruff ratchet, mypy baseline ratchet, vendor lock, artifact manifest, and `git diff --check`: **PASS**; ratchets remain `2149/2149` and `1914/1914`.
- Prior exact-495 integration evidence: **5 pass / 1 fail**; the sole failure is the separate V2 nullable `speed` validation before first clip add, owned by `agt-V2-boundaries-return-0553`. The known failed six-case lane was not rerun.

## Decision and next step

Mark this review **source PASS**, not overall R2/G4 DONE. Requalify the three-redo integration path after the corrected joined V2/current-fork tree lands. Preserve all existing authenticated closure, allocation, collision, ABA, and forgery guards during merge-forward. Detailed evidence is in the worker report at `workers/agt-R2-stage-review-0553/report.md`.
