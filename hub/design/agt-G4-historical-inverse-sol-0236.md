**Partial fix delivered; G4 remains blocked.**

Fixed authenticated foreign-occurrence normalization in [native_occurrence_shared.py](/home/user/work/wt/agt-G4-historical-inverse-sol-0236/astrid/sdk/timeline/native_occurrence_shared.py:203). Undo now preserves the accepted physical identity when another destination owner retains the images. Added four [owner/media controls](/home/user/work/wt/agt-G4-historical-inverse-sol-0236/tests/editing_conformance/test_historical_shared_inverse_owners.py). Reserved files were untouched.

Tests used the prescribed qualified environment. With `S=/tmp/w-c3868a10ef` and `P=/home/user/work/venv-agent/bin/python`:

- `$P $S/capture_inverse.py` — **1 failed**, reproducing original last-owner undo.
- `$P $S/capture_parent_owners.py` — **2 failed** with the exact-parent helper.
- `$P -m pytest -q -oaddopts= -p no:cacheprovider tests/editing_conformance/test_historical_shared_inverse_owners.py --basetemp=$S/owner-controls-final --timeout=45 --tb=short` — **4 passed** after the fix.
- `$P $S/capture_final.py` — original historical/same-timeline slice: **30 passed, 1 failed**.
- `$P $S/probe_auth.py` — diagnostic assertions passed, including complete-owner and source-history negative controls.

Scoped Ruff, private mypy, exact-parent diagnostics, `scripts/artifact_manifest.py --check`, and `git diff --check` passed. No full suite, vendor checker, browser tests, or unchanged source-copy redo cohort ran.

**Runtime boundary:** retained [complete pre-validation inputs](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-historical-inverse-sol-0236/historical-final-auth-0.json) show one native occurrence removal but three canonical effects: occurrence removal plus shot/internal closure retirement. Both retired images have sole owner `occurrence:shared-copy/shot`.

Runtime `timeline_commit_auth.py:1078` requires the native-write count to equal the source stage’s count—one. Adding an exact native shot/internal retirement or observing all canonical sites fails that guard; retaining one write fails complete coverage at line 1391. This is a Runtime verification boundary requiring peer work, beyond the earlier Agent-only assessment.

Recommended next step: Runtime must authenticate closure retirement against exact source effects and complete ownership; Agent can then complete native retirement and redo authority propagation. Genuine last-owner undo, exact-source redo access/media/document/archive revalidation, and cleanup remain incomplete.

Wrote `commit-msg` and `BLOCKED`; no `DONE`. Evidence totals under 1 MB.