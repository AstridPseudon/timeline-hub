# agt-m3-capture-source-final

Base: tl/agt-m3-capture-source-recover 99eed3cf. Runtime: /home/user/work/runtime (unmodified, read-only use). No pins, no Runtime edit.

## Changes
- `tests/sdk/test_capture_source_runtime.py`: fixture fixes only (idempotency keys `media-<hex>`/`capture-<hex>` instead of `sha256:` values; capability registered with Runtime's default digest `sha256(capability)`; `_replace_values` applied per closure element; `admit` builds a ref only for non-inline; native case drops both `capture_authority` and `canonical_timeline`). The after-the-fact `pytest.xfail` is replaced by `@pytest.mark.xfail(strict=True)` over the forged-capture test; the `values.timeline_source is None` expectation is unchanged.
- `astrid/core/rendering/verified_source.py`: `validate_snapshot` compares canonical JSON (`_canonical`), not Python `!=`.
- `tests/packs/rendering/test_verified_source.py`: new `test_capture_replacement_is_exact_across_bool_and_numeric_encoding` (1->True, 2->2.0 refused).

## Commands / results
Runner: `/home/user/work/venv-agent/bin/python <scratch>/run.py <files>` (sets ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime in-process, `-m integration -o addopts=`).
- `tests/sdk/test_capture_source_runtime.py`: 6 passed, 12 xfailed.
- Same with `--runxfail`: 12 failed (all `assert VerifiedTimelineSource(...) is None`), 6 passed. So every forged case is genuinely admitted and given a source (not an error elsewhere).
- Neighbours (`test_verified_source.py`, `test_verified_canonical_preparation.py`, `test_capture_closure_source.py`, `test_timeline_filmstrip_execution.py`): 84 passed, 8 errors. The errors are all `test_verified_canonical_preparation.py::test_verified_prepared_file_compiler_and_scene_agree[...]` setup: "requires this worktree's locked npm ci" (node_modules absent; environmental, not touched by this change).
- New bool/numeric test: 2 passed. Ruff clean on touched files.
- Full suite not requested (targeted change; no localhost/browser).

## Findings
- Positives: saved and working-copy x inline and ref reach claim and materialization with exact snapshot, authority, base digest and a RenderRequest-verified source. Duplicate replaced ref refused at host ("differs from admitted context"). Native compiled capture gets `timeline_source is None`.
- Known xfails (12, strict): config / registry / shot content_digest x saved/working-copy x inline/ref. Runtime `publish_snapshot` checks only the parent revision row and the working-copy marker, never snapshot content. Escalated in design/runtime-coordination.md and viewing-coordination.md with an existing-admission recommendation (recompute projection from stored closure and require byte equality, else publish as native `cas`).
- Inline snapshots are rewritten by Runtime into refs using the snapshot's own metadata, so "inline" is not a separate trust path.
- A capture with `capture_authority` removed but `canonical_timeline` kept is published as a revision ref and the Agent host refuses it (fail closed); not separately tested.
- Boundary labelled exactly: this proves public CAS -> admission -> claim -> Agent materialization and RenderRequest parsing. No renderer, pixels, public9 pin or launch-render claim. M3 gate 6 stays open.
- Caller ports/wire/env replacement negatives were already covered in test_verified_source.py (reserved ports, direct render ports, env anchor, file replacement); passing in the 84.
- Registry bool/numeric variant not added: it shares the `_canonical` code path and the helper's registry is empty.
- Sandbox note: env-var prefixes on Bash commands trigger approval, so the runner sets the env inside Python.
