# G5 c271 qualification report

Status: **PASS, source-stage only.** G5 remains DRAFT/P1-gated; no integrated merge or P1 GO is claimed.

- Agent: `830fba00bcb4d205bdeca6f1287a67b218208694`, tree `3bdbdd03…`
- Runtime: `8ea0766f5e9fb23cea26c7398770a8aaac06b258`, tree `6047ac303…`
- Authentic fixture SHA: `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`
- c271 body lock: `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`
- Collection: `1 selected, 0 deselected`
- Sole body: **1 passed in 40.92s**, exit 0
- Forward restructure, whole undo, redo, and guarded overlap refusal all completed. Final refusal was `an intervening publication wrote a guarded address`; SQL/head/history remained unchanged.
- Evidence: [packet archive](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-config-qualified-c271-2105/evidence/c271-config-qualification-packets.tar.gz), SHA-256 `3040be2f4db679e64954e0895dff63fa4705866004b55640e3e11bc9c116898f`, 11,397,752 bytes.
- Evidence validation: 81 packets, credential findings 0, Runtime-origin mismatches 0.
- Static checks passed: Ruff, mypy, vendor lock, artifact manifest, `git diff --check`.
- Worktree has no tracked edits. Commit message and empty `DONE` marker were written.

Exact body command used:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS='' \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f \
PYTHONPATH="$TMPDIR/g5-c271-observer:/home/user/work/wt/agt-G5-config-qualified-c271-2105:/home/user/work/wt/rt-pin-8ea0766f" \
timeout -k 15 480 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p g5_corrected_observer \
tests/sdk/test_timeline_restructure_guarded_runtime.py::test_restructure_whole_inverse_redo_and_intervening_overlap_refusal
```

The supported prior 2041 packet (`8bf50ade…`) and observer lineage were used only for continuity; denied 2017 material was not used. Full/integrated/browser suites remain unverified.