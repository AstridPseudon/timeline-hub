# D15 copied-source baseline — 1232

Source fix ready for independent review; G5 migration remains DRAFT ONLY and P1 remains gated. Base is `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`, not G5 draft ancestry. No Git mutation performed.

## Change and decision

Changed only `astrid/core/timeline/authoring_bundle.py`, `astrid/sdk/timeline/native_occurrence_duplicate.py` (the shared native fork/copy implementation), and new `tests/editing_conformance/test_occurrence_fork_source_baseline.py`.

Native copies now retain an internal dictionary subclass carrying their source occurrence/exact shot pin and destination identity. This provenance survives recorder deep copies but is excluded from authored JSON, canonical documents, commands, and receipts. It therefore does not change the existing D17 portable golden. A JSON caller cannot supply this internal type. Ordinary published documents reopen through the existing verified closure route; serializing an unpublished preview does not grant copy provenance.

The compiler reconstructs the copied baseline from the verified immutable `_runtime_document`, checks its project/timeline and exact parent pair, verifies the original occurrence/shot revision and destination placement, and applies the existing deterministic item remapping. It does not use caller `base_payload`, `base_internal_timeline`, or mutable shot-source mapping claims to authorize the copied baseline. A copy is still a new root requiring materialization. The existing competing-selection checks run against this reconstructed baseline unchanged.

This permits retained `{OLD,AUDIO}` shot metadata alongside internal selections `{OLD}` without treating retained audio as a new selection. It does not suppress new competing selections. Internal provenance was chosen over a serialized baseline field: adding a field initially broke the existing portable D17 golden; the final representation preserves that exact fixture and exposes no new protocol surface.

## Causal RED

The new fixture uses `app_closure()` and exactly the frozen `6120c254...` `seed_emitter_parent` preparation, converted through the existing pure trusted-seed `_closure()` helper. It preserves the original media mismatch and shared physical closure.

Before the source change, the initial new test file produced **2 failed, 6 passed**: both normal `document_from_bundle(execute(...).bundle)` and `execute(..., commit_request={})` failed with `AuthoringBundleError: shot 'selected-shot' has competing selected media between shot items and internal clips`. Preview creation had already succeeded. This independently confirms the producer/compiler cause before historical reuse, not Runtime/client/authentication.

Durable log: `ORCH/workers/agt-A3-fork-source-baseline-1232/red.log` (here and below, ORCH is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`).

## Verification

All commands ran in the assigned worktree. Shared dependencies were read-only; scratch/cache paths were private. No full, HTTP/socket, browser, broad native, P1/P4, or central full-suite run was requested.

Initial RED command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-5d30ac6a62/red tests/editing_conformance/test_occurrence_fork_source_baseline.py
```

Focused new + existing D15/D17 regression command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-5d30ac6a62/final tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_recipe_occurrence_fork.py tests/editing_conformance/test_provider_occurrence_fork.py tests/editing_conformance/test_recipe_occurrence_duplicate.py
# 105 passed in 16.95s; exit 0. Log: workers/.../final-targeted.log
```

After final import formatting/type annotations, the new file alone was run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-5d30ac6a62/final-focused tests/editing_conformance/test_occurrence_fork_source_baseline.py
# 17 passed in 4.32s; exit 0. Log: workers/.../final-focused.log
```

The focused file covers both compilation boundaries; full copied payload/internal equality; item remapping; source media manifest; unchanged sibling images, placement order, opaque/null-bearing data; fork reload and exact undo; original shared-alias contradiction; new competing media; JSON-forged provenance; forged old payloads/source mapping; source pin/parent staleness; outside/foreign owners; and occupied IDs. Existing fork stale/undo/redo and D17 copy tests are unchanged.

One new test exercises the actual current3b RuntimeService with its startup-loaded Astrid provider and credential authorization, using the existing retained fixture setup and ingested media. It sends the full v2 request (exact base pair, commands, per-step patch/reads/ordinals, label, merge, reads, dry-run, source/rationale/group and idempotency). Preview has `would_status=accepted` and no receipt/write; acceptance validates `CommitAccepted` and returns the exact same full canonical closure, selected edit and unchanged original sibling images. It uses no sockets or alternate executor.

Quality and frozen-artifact commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. RUFF_CACHE_DIR=/tmp/w-5d30ac6a62/ruff make ruff PY=/home/user/work/venv-agent/bin/python
# 2149 / 2149; PASS (ruff.log)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-5d30ac6a62/mypy make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python
# 1912 / 1912; PASS (mypy.log)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-5d30ac6a62/scoped-mypy /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --follow-imports=silent astrid/core/timeline/authoring_bundle.py astrid/sdk/timeline/native_occurrence_duplicate.py tests/editing_conformance/test_occurrence_fork_source_baseline.py
# Success: no issues found in 3 source files; scoped new identities 0 (scoped-mypy.log)
/home/user/work/venv-agent/bin/ruff check --no-cache astrid/core/timeline/authoring_bundle.py astrid/sdk/timeline/native_occurrence_duplicate.py tests/editing_conformance/test_occurrence_fork_source_baseline.py
# All checks passed
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
# ok runtime.lock.json (matches producer manifest)
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# artifacts.json is current
git diff --check
# PASS
```

The first combined quality invocation used the typecheck interpreter for Ruff, which lacks Ruff; it exited 2 before checks. Corrected commands above use the proper existing interpreters. No installs or dependency changes. Scoped Ruff's new-test import formatting was corrected; no baseline was edited.

## Additional finding and next steps

A broader exploratory assertion after the real-provider fork+emitter acceptance attempted whole-transaction undo. It failed with `inverse stage native writes do not cover its authenticated effect image`. The accepted/preview portion had already passed. The durable traceback is `ORCH/workers/agt-A3-fork-source-baseline-1232/combined-undo-red.log`. This exploratory new assertion had never passed and was not retained as an expansion of this source-baseline test's scope; no existing passing expectation was changed, skipped, xfailed, deleted, or converted to refusal. Existing D15 undo controls and the new retained-source fork-only exact undo pass. The combined transaction inverse remains unverified/unresolved and should go to the inverse/R1 owner; no prohibited inverse/commit file was touched.

Request independent review of this source fix before integration. Then let the G5 test-port owner resume the original retained selected-edit migration with normal projected fork input, retaining the complete canonical/sibling/provider refusal assertions and P1 gate. Investigate the separately captured combined-undo failure before treating that expanded journey as qualified. No decision from PLAN was overridden; no emitter, migration source6120, journal/publish/checkout, R1 atomic, Runtime, schema, generated client, contract, pin, artifact, or dependency file changed.
