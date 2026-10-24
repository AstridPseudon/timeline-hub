Implemented the bounded R2r repair in [timeline_commit_auth.py](/home/user/work/wt/rt-R2r-shared-inverse-auth-sol-0647/runtime_protocol/timeline_commit_auth.py:1011), plus one separate regression.

- Historical `item_id:item-1` differs from the accepted placement-local item identity. The repair derives correspondence from the accepted copy and verifies complete sequential native captures.
- Shared restoration now restores only the recorded consumer while preserving retained sibling images and edges.
- Existing singleton turnover guards remain. No store, Agent, contract, schema, client, or pin edits.

Runtime base: `1d9ddba546f8fb1300f55ff62607ed492719cbaa`. Agent diagnostic source: archived `d33fe5f9f0e69d874ff60fe1ea513fc3bbe11190`.

Commands used `PYTHONDONTWRITEBYTECODE=1`, worktree-first `PYTHONPATH`, and `/home/user/work/venv-runtime/bin/python`:

```bash
-m pytest -q -o addopts= -p no:cacheprovider \
  "$TMPDIR/agent-source/tests/editing_conformance/test_authoring_item_observation_boundary.py" \
  -k 'two_shared_occurrences_inverse_accept_and_preview or retained_source_copy_inverse_passes'
```

Before repair: **4 failed, 2 passed**.

```bash
-m pytest -q -o addopts= -p no:cacheprovider \
  tests/test_timeline_shared_inverse_authority.py \
  tests/test_timeline_inverse_stage_authentication.py
```

With `ASTRID_CHECKOUT="$TMPDIR/agent-source"`: **177 passed**.

```bash
-m pytest -q -o addopts= -p no:cacheprovider \
  "$TMPDIR/agent-source/tests/editing_conformance/test_authoring_item_observation_boundary.py"
```

Final frozen diagnostic: **89 passed, 6 failed**. All four shared positives and both source-copy comparisons pass. Six untouched diagnostic assertions still expect the previous refusal sites; the frozen file is **not green**.

Scoped parent/final Ruff and Pyright passed with zero diagnostics. In-memory compilation, artifact manifest, protected-file hashes, frozen source/AST checks, and `git diff --check` passed. JUnit, packets, logs, and [provenance](/tmp/w-c125561bd7/provenance.json) remain in private scratch.

The repair covers one accepted shared `occurrence.swap-media` copy stage. Independent security review must approve its source-derived placement mapping before a reviewed Agent join. Agent diagnostics need owner review; original11466 and D47 remain held. No HTTP, original-journey, or full-suite qualification claimed.

Commit message and `DONE` written.