## Result

Implemented private D68 wrapper: [scripts/delivery_gate_build.py](/home/user/work/wt/rt-F-final-D68-isolated-1546/scripts/delivery_gate_build.py)

It:

- Validates immutable gate tuple/hash and source refs.
- Stages fresh upstream privately.
- Applies only base→gated-tip via three-way merge.
- Retains conflicts for normal resolution.
- Preserves owner additions and feeds staged roots to f25d builder.
- Rechecks all source refs/status afterward.
- Preserves builder args, extras, checksums, and verification.

## Evidence

- Synthetic controls: unchanged upstream, owner additions, disjoint same-file edits, delete/rename, conflict retention, source-ref immutability, and f25d dry-run: all PASS.
- Old reverse-direction algorithm erased owner additions; candidate preserved both deltas.
- Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-D68-isolated-1546/evidence/`

## Checks

- `python3 -m py_compile scripts/delivery_gate_build.py` — PASS
- `ruff check scripts/delivery_gate_build.py` — PASS
- `mypy --no-incremental scripts/delivery_gate_build.py` — PASS
- `git diff --check` — PASS

No live installation, registry/doc change, network fetch, real build/ZIP, full suite, or 3309 route execution was performed. Active stale `3dfd` and held 3309/f25d facts remain unchanged for later owner installation review.

Commit message written and `DONE` marker created.