# R1 immutable transcript input capture — 1735

Completed against Agent base `6531622c8f198c3efb509217e303fcad0126c47b`. Product diff: 13 added lines across `commit.py` and `_commit_patch.py`; one new focused regression file. No existing test body changed. No Git writes, branch operations, shared dependency/cache writes, Runtime edits, schema/client/pin changes, or full/browser suites.

## Finding and fix

Read PLAN §3 R1/G2 and C0 request/read/command ordering contract, full retained transcript-head packet (208011 bytes; SHA-256 `47ac8f6840f1c3d2086642979908aa11b0d858c449df28f1c37179eeb05fdb89`), author1709 handoff, and peer1728. Published the early source finding at absolute ORCH `design/peer-agent-to-runtime-20261023T1735-transcript-source-finding.md`. Before product edits, consumed newly published independent Runtime1728 review from hub `design/handoff-runtime-R2r-fullseed-review-1728.md`; retained a copy in evidence. That review confirms the immutable input mismatch is Agent-owned and Runtime pin validation is correct.

`_hydrate()` already authenticates all exact request document sources. Previously their mere presence in `pinned_documents` made `document_from_bundle()` add all their pins before command 0, replacing the source parent identity even when parent bytes were unchanged. Forward hydration now initializes the existing private `_copy_manifest` from the immutable source manifest when new verified inputs exist. `CommitPatch.after()` advances its document list from that command's existing `source`/`transcript` dependency records, requiring a matching verified capture. Thus verified bytes remain available, while dependencies enter command output only when consumed. The next input receives precisely that output.

No public field, snapshot authority, history edge, pin equivalence, or Runtime exception was added. Existing private original/landing/read/history carrier APIs and final-validation callsite are unchanged. Inverse hydration behavior is deliberately unchanged (`inverse_records` path retains its previous handling); this task does not qualify additional inverse scenarios. Eight protected file hashes, including original/history helpers, inverse modules, timing validation, validation, commands, and runtime lock, remain unchanged (see baseline/final source hashes).

## Exact test commands and results

All Agent commands run from `/home/user/work/wt/agt-R1-transcript-input-sol-1735`. All tests clear default marker exclusions and disable pytest cache. Scratch and basetemp stay under `/tmp/w-493af63037`, the assigned worker tmpdir.

New focused GREEN:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime:/home/user/work/agent-runtime-projection-0856/site-packages TMPDIR=/tmp/w-493af63037 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_commit_document_input_capture.py --basetemp=/tmp/w-493af63037/focused-green
```

**5 passed in 0.67s.** Both one-step and separate-step cases require exact immutable command-0 input, an earlier command excluding the future transcript, contiguous boundaries, and the consuming output including its pin. Three negatives reject wrong content digest, foreign project, and wrong document version without bundle mutation. `evidence/focused-green.log`.

Old-source RED, same unchanged new tests, with only the two product modules restored from exact HEAD in a private symlink overlay:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/w-493af63037/baseline-overlay:.:/home/user/work/runtime:/home/user/work/agent-runtime-projection-0856/site-packages TMPDIR=/tmp/w-493af63037 /home/user/work/venv-agent/bin/python -P -m pytest --import-mode=importlib -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_commit_document_input_capture.py --basetemp=/tmp/w-493af63037/focused-red-importlib
```

**2 failed, 3 passed in 1.01s.** Both positive cases fail at exact immutable input equality: same parent bytes, changed physical revision and newly inserted document manifest. The three source-integrity negatives already pass. `evidence/focused-red-importlib.log`. An earlier baseline attempt omitted importlib mode and pytest selected patched modules; its 5 PASS is not credited as a baseline (`focused-red.log` retained).

Required Runtime original node plus directly needed strict variants, from private exact `git archive d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b` at `/tmp/w-493af63037/runtime-d9e`:

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/wt/agt-R1-transcript-input-sol-1735 PYTHONPATH=/tmp/w-493af63037:.:packages/python:/home/user/work/wt/agt-R1-transcript-input-sol-1735:/home/user/work/agent-runtime-projection-0856/site-packages TMPDIR=/tmp/w-493af63037 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p transcript_observer_d9e 'tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[None-True]' 'tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[before-True]' 'tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[late-source-True]' --basetemp=/tmp/w-493af63037/runtime-exact-d9e
```

**3 passed in 44.97s.** Real Agent provider and Runtime public service/port/store; no sockets, daemon, manual realm, provider replacement or weakened guard. Positive includes canonical readback and exact-key retry. Both strict refusals retain exact SQL/history/head equality; observed error is `sequential execution capture does not bind the prepared commit` after test tampering. Runtime auth SHA-256 is exactly d9e `9a009f155c7ca8df021e1016d19a36ff8b41f79aeacefcfcb3d26e30524203e5` in all three target packets. `evidence/runtime-exact-d9e.log`, `evidence/exact-d9e/runtime-capture-{03,06,09}.json`.

A first run used `/home/user/work/runtime` with identical arguments except observer `transcript_observer` and basetemp `runtime-candidate`: **3 passed in 47.61s**, but shared integration advanced to `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, auth hash `3b812936...8f2ef`. This is supplemental only; the exact d9e run above corrects the source-tuple mismatch. Both runs' complete evidence remains retained. No unchanged baseline live recapture was performed; RED Runtime evidence is the supplied original packet.

Existing private original/landing capture controls:

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/tmp/w-493af63037/runtime-d9e PYTHONPATH=.:/tmp/w-493af63037/runtime-d9e:/home/user/work/agent-runtime-projection-0856/site-packages TMPDIR=/tmp/w-493af63037 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_private_sequential_capture.py tests/editing_conformance/test_private_sequential_capture_runtime.py --basetemp=/tmp/w-493af63037/private16
```

**16 passed in 7.88s.** `evidence/private16.log`.

Existing sequential rebase controls (same environment, replacing the test files with `tests/editing_conformance/test_doc_patch_sequential_rebase.py` and basetemp with `private-sequential`): **9 passed in 19.60s**, including moved-head and refusal/no-write controls. `evidence/private-sequential.log`.

## Static and frozen-input checks

```bash
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-493af63037/ruff-cache /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-493af63037/mypy-baseline /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-493af63037/mypy-private /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/commit.py astrid/sdk/timeline/_commit_patch.py --hide-error-context --no-color-output --no-pretty --show-error-codes
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-493af63037/ruff-scoped /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/commit.py astrid/sdk/timeline/_commit_patch.py tests/editing_conformance/test_commit_document_input_capture.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

All pass. Full Ruff count **2149/2149**; full Mypy count **1912/1912**. Scoped Ruff **0 diagnostics**; private two-file Mypy **0 diagnostics**. Vendor lock and artifact declarations current. All **15** lock-owned vendored files compared byte-for-byte with `git archive 34eac0041b0891e9011966b39bcbd26053fde5bc`, and their declared SHA-256 values verified (`evidence/vendor34e.json`). Counts refer to actual checked paths, not a broader schema qualification.

## Permanent custody and disposition

Before candidate execution, copied the original complete packet and baseline module hashes to worker evidence. The observation-only accept wrapper writes complete context/request/prepared/private original+landing/closures/transcript captures/native/effect/owner bindings/read-union/SQL/head/history/module paths and hashes before invoking unchanged acceptance, then attaches result/error and after-state. Observer source is retained. Final positive includes accepted public history and stored private sequential evidence. Test identities and SQL are synthetic fixtures; no real service capture or credentials are claimed.

Portable lossless packets are exported under absolute ORCH `design/` and duplicated in worker evidence, each with `.sha256`:

- `agent-R1-transcript-input-1735-positive-packet.json` — 1839613 bytes, SHA-256 `5314b3f750cda5266cec969aa44ce8c5201e43f7ddc35644e286f2104f2ed1db`.
- `agent-R1-transcript-input-1735-before-negative-packet.json` — 1232932 bytes, SHA-256 `e62dcd4ff226b3905a7da42d129282f664c11ad20d145b5c61dfb7de316aa5f7`.
- `agent-R1-transcript-input-1735-late-source-negative-packet.json` — 1233084 bytes, SHA-256 `7a169b2d3add39bc90c88238dac4588f6382709457eb83308cb5846e170f9bbf`.

No blocker remains for this bounded source correction. Independent Luna review is the next step, then the normal Agent merge worker; preserve the original/landing APIs and later d1d validation callsite when joining. Runtime cohort/full suite/browser/original-nine/P1/P4/native journeys were not rerun, and this work does not grant them qualification or claim complete project green. The requested task is ready for review; no commit was made manually.
