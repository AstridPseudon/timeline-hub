# R2 c271 native/effect coverage: Runtime owner request

Status: **Agent edits stopped; blocked on Runtime normalization repair. G5 stays DRAFT / gated:P1.** No tracked changes, new test, generated artifacts, pins, shared dependencies, store, daemon or environment changes. Diagnostic task completed with the explicitly requested Runtime-owned stop branch.

## Exact cause and source assessment

Agent base is `f120159fae86b5fb1e5379437737b4e0a16627eb`, tree `e56d741e65f94f22122c9dcced134480d08dc03b`; Runtime execution is `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree `f79a2355cfb39d9ada7721978bd20d5702105778`. The complete 2010 archive checksum, byte count and 85 members match the brief. Extracted only under `$TMPDIR` (`/tmp/w-323e42d3de`); no original c271 body executed or copied into authoring.

The offline replay calls current Agent `execute` with the exact captured full request, source boundaries/history and resolver. Its candidate equals the captured prepared canonical document; its native writes and step patches also equal the captured prepared records exactly. Inputs remain unchanged. All 10 emitted native writes are the exact reverse, with before/after swapped, of the accepted source command. Source publication is `txn-0e37f757d72c4226b04fcf6315980651`; the resolver also authenticates its original restructure source `txn-1caf8d8641d74d3aa012388faf0fdd4c`. No captures or history were invented.

Passing those exact values to Runtime `timeline_commit_auth.validate` reproduces the original structured `CommitRejected`, HTTP 422 `validation_error`, details reason `invalid_records`, message `inverse stage native writes do not cover its authenticated effect image`. Stage partition is native `[0, 10]`, effects `[0, 9]`, step `inverse`, source ordinal `[0]`.

**Confirmed defect:** Runtime `runtime_protocol/timeline_commit_auth.py:1200` projects native write index 6, `parent` / `['occurrences']`, directly into the physical parent payload. The write restores occurrence order using authored rows. Immediately before line 1200, all three occurrence rows contain their correct authenticated `shot_revision_id`; immediately afterward all three pins are missing. The final comparison at line 1373 differs only at `parent.occurrences[0..2].shot_revision_id`. Physical root keys and every other payload byte are equal.

This is Runtime's representation boundary: `_inverse_stage_state` at lines 857–863 authenticates the physical occurrence collection through `_inverse_stage_occurrence_collection` (817–854), then removes those pins to compare with the authored native capture. Its write projection fails to preserve the already-authenticated pins when it performs the corresponding order change. Agent `_command_state.py:291` returns authored placements; `State.set` at line 370 permits only an exact authored-row permutation. Adding physical pins to Agent captures conflicts with that existing representation and Runtime's own authored comparison. Agent inverse emission is not missing an authored write, and changing its immutable source captures is not a repair.

The bounded evidence retains the exact request/history/candidate, native/effect/binding records, physical comparison images, partitions and original no-write observations. The replay reads locals with `sys.settrace`; it does not alter Runtime control flow, globals or arguments. Both Agent and Runtime module origins match the named trees before/after. Original head, history and SQL before/after compare equal. The original 2010 authority remains the complete structured exception plus completed observer teardown; no original pytest terminal result is claimed. Original later redo/overlap assertions remain unreached.

## Validation

Exact targeted command (exit 0; **143 passed in 71.30s**):

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_captured_config_root_mirror.py tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_nested_native_aggregate_partition.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_parent_mirror_ranges.py tests/editing_conformance/test_captured_nested_redo.py
```

No NEW_FILE was created or executed: the brief requires stopping Agent edits when Runtime normalization owns the refusal. Existing passing behavior tests and reviewed config-mirror repair remain byte-identical to the exact parent.

Exact bounded causal replay (exit **1**, the deliberately preserved current Runtime RED; full traceback in `offline-red.log`):

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-c271-effect-sol-2013/evidence/replay.py
```

Agent candidate/native writes/steps match the original prepared packet before the real Runtime refusal. This is diagnosis, not a functional green result. No bypass, hypothetical green, fabricated pytest terminal or end-to-end qualification is claimed.

Scoped static comparison (exit 0):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python /tmp/w-323e42d3de/static_compare.py
```

The script is retained verbatim in `evidence/static_compare.py`. Scope: `_step_undo.py`, `inverse.py`, `_root_inverse.py`. It verifies each file byte-identical to `git show f120159:<path>`, runs Ruff `check --no-cache --output-format=json`, and Mypy `--follow-imports=silent --hide-error-context --no-color-output --no-pretty --show-error-codes --no-incremental --cache-dir <private TMPDIR path>`. Parent Mypy uses `--shadow-file` for all three exact-parent blobs. Full diagnostic identities equal the parent for both tools (zero findings); commands, return codes and identities are in `ruff-{parent,current}.json` and `mypy-{parent,current}.json`. No count budget changed.

Additional exact commands (all exit 0):

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
git diff --exit-code f120159fae86b5fb1e5379437737b4e0a16627eb -- .
git status --short
```

Vendor manifest matches; artifacts current; entire Agent source/test tree unchanged, clean status. Runtime execution tree also remains clean. No full suite, live socket/browser suite, SDK FOUR, original c271 execution, P1/P4, waiver, new pin tuple, or G5 activation was requested/performed.

## Precise owner request and remaining limit

Dispatch Runtime owner to the ordinary `_inverse_stage_boundaries` parent-occurrences projection. Preserve the exact already-authenticated occurrence-to-shot revision pins while projecting the proved authored-row order permutation. Keep row membership, authored bytes, order, physical owner/shot/internal identity and digests strict; reject foreign/ambiguous pins and changed membership. Reuse authenticated existing physical facts, without alias-to-byte inference, root copying, source-history synthesis, or identity retargeting. Keep the native/effect final equality and no-write refusals.

Agent source changes and new conformance authoring were stopped as instructed. No source repair or oldRED→newGREEN is claimed. The next step is a bounded Runtime repair and independent strict negative controls there, followed by manager qualification on meaningful source plus independent PASS. The manager owns the single original-c271 qualification afterward. This report requests no decision change.

Evidence directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-c271-effect-sol-2013/evidence` (under 7 MB total worker output; archive stays only in the original worker and temporary extraction). Checksums and derivation are in `evidence/manifest.json`.
