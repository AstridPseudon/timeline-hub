# R1/G2 review: FAIL

## Scope and source identity

Reviewed `tl/agt-R1-transcript-input-sol-1735` at Agent `eb2f3eb161a1435cba1e8516b27d0bd37e108331`, against base `6531622c8f198c3efb509217e303fcad0126c47b`, PLAN §3 R1/G2 and C0 §§1/2/3. The candidate is the stated 13 product lines in `astrid/sdk/timeline/commit.py` and `_commit_patch.py`, plus the five-test file `tests/editing_conformance/test_commit_document_input_capture.py`; no existing test body was changed.

The retained packet and author packets were checked by hash:

- packet47ac retained head packet: `47ac8f6840f1c3d2086642979908aa11b0d858c449df28f1c37179eeb05fdb89` (208011 bytes).
- author positive: `5314b3f750cda5266cec969aa44ce8c5201e43f7ddc35644e286f2104f2ed1db`.
- author before-negative: `e62dcd4ff226b3905a7da42d129282f664c11ad20d145b5c61dfb7de316aa5f7`.
- author late-source-negative: `7a169b2d3add39bc90c88238dac4588f6382709457eb83308cb5846e170f9bbf`.

Agent source hashes were unchanged from BEFORE to AFTER: `commit.py` `98293f1e8b97e1e999ba185e8ea03b26e2c47c3ff0896e1bc59b75314a6d0088`; `_commit_patch.py` `baf524346b6b0d408a2d91683eb02dc600430145c5a18cb56e13d946ccfcbae1`; new test `010f3d97d1172ff5f32338f01cf92b5e6be70d68bea39aef5514ffc9d273cfea`.

## Finding

**F1 — blocking trust-boundary defect: caller-supplied `_copy_manifest` is accepted as authenticated closure authority.**

At `commit.py:523`, `_hydrate()` uses `setdefault('_copy_manifest', ...)`, so an existing caller-provided `_copy_manifest` is retained. At `commit.py:366-376`, `document_from_bundle()` then reads that field as the document manifest and publishes its pins. `_commit_patch.py:438-445` only appends authenticated consumed pins; it never authenticates or replaces pre-existing entries.

Read-only forged-manifest probe: seed `_copy_manifest.documents` with
`transcript:foreign-project:media:source`, version `99`, digest
`sha256:` plus 64 `f` characters, then call `_hydrate`, execute the candidate
commands, and call `document_from_bundle`. The forged pin survived hydration
and appeared in the final manifest alongside the authentic consumed pin.
The direct `document_from_bundle` probe also returned the forged pin. This
violates the required `_copy_manifest cannot become caller authority` rule,
even though the ordinary authenticated path is correct.

Smallest durable repair: establish the copy manifest only from the
Runtime-authenticated `_runtime_document` for the normal non-inverse path (or
reject/strip caller-supplied `_copy_manifest` before hydration), and keep the
existing authenticated duplicate/inverse paths distinct. Add a regression that
pre-seeds a foreign/wrong-digest manifest and requires rejection or an
authenticated replacement with no write.

## Behavioral evidence

Exact commands (all from the review worktree unless noted):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime:/home/user/work/agent-runtime-projection-0856/site-packages TMPDIR=/tmp/w-501798496d /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_commit_document_input_capture.py --basetemp=/tmp/w-501798496d/focused-new5

PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/wt/agt-R1-transcript-review-1748 RUNTIME_CAPTURE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-transcript-review-1748/evidence/runtime-2a9e-captures PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-transcript-review-1748/evidence:/tmp/w-501798496d/runtime-2a9e:/home/user/work/wt/agt-R1-transcript-review-1748:/home/user/work/agent-runtime-projection-0856/site-packages TMPDIR=/tmp/w-501798496d /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p runtime_observer 'tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[None-True]' 'tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[before-True]' 'tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[late-source-True]' --basetemp=/tmp/w-501798496d/runtime-2a9e-targeted-final

PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/tmp/w-501798496d/runtime-2a9e PYTHONPATH=.:/tmp/w-501798496d/runtime-2a9e:/home/user/work/agent-runtime-projection-0856/site-packages TMPDIR=/tmp/w-501798496d /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_private_sequential_capture.py tests/editing_conformance/test_private_sequential_capture_runtime.py --basetemp=/tmp/w-501798496d/private16

PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-501798496d/ruff-baseline /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-501798496d/mypy-baseline /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-501798496d/mypy-private /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/commit.py astrid/sdk/timeline/_commit_patch.py --hide-error-context --no-color-output --no-pretty --show-error-codes
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-501798496d/ruff-scoped /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/commit.py astrid/sdk/timeline/_commit_patch.py tests/editing_conformance/test_commit_document_input_capture.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

All targeted behavior unrelated to F1 passed:

- New capture tests: **5 passed**. They preserve command-0 immutable input,
  reject digest/project/version damage, and add the verified pin only at the
  consuming command boundary.
- Runtime exact archive at `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, using
  the real Agent provider and public service/provider/store: **3 passed** for
  `[None-True]`, `[before-True]`, and `[late-source-True]`. Runtime auth module
  hash was `3b812936efaa35a165c056fbacee6d8e699d485ca912f12e11cc4cd4bbe8f2ef`,
  distinct from the old d9e baseline (`9a009f155c7ca8df021e1016d19a36ff8b41f79aeacefcfcb3d26e30524203e5`).
  The positive accepted and the strict variants retained SQL/head/history on
  rejection. Full per-accept captures and SHA-256s are in
  `workers/agt-R1-transcript-review-1748/evidence/runtime-2a9e-captures/`.
- Affected private sequential controls: **16 passed**.
- Ruff ratchet: **2149/2149**; mypy ratchet: **1912/1912**.
- Scoped mypy: **0 issues**; scoped Ruff: **0 diagnostics**.
- `vendor_lock.py check runtime.lock.json`: **ok**.
- `artifact_manifest.py --check`: **current**.
- `git diff --check`: **pass**.

Exact command logs and immutable BEFORE/AFTER hashes are in the permanent
worker evidence directory. Credential scan over the nine full Runtime capture
JSON files found zero credential-like keys and zero common credential-value
patterns.

The author report's old-nine supplemental run is disclosed but not credited or
rerun. The review run used the current reviewed Runtime 2a9e pair, not an
integrated Agent claim. No client adoption, schema/pin change, inverse change,
test weakening, full suite, browser suite, or Runtime d9e rerun was performed.
Earlier overlapping launch attempts while collecting the Runtime capture output
are uncredited; only the final isolated 2a9e run in the named capture directory
is authoritative.

## Limits and disposition

No product files, tests, Runtime files, schemas, clients, pins, environments,
Git refs, or daemons were modified. The prompt-listed R4 control-doc directory
and `scratchpad/luna/reports` were not present; the available PLAN, candidate
brief/design, packet47ac, and author permanent packets were used. The candidate
is **FAIL** until F1 is repaired and covered by a focused negative regression.
