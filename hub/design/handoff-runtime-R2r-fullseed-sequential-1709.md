# R2r full-seed sequential binding — 1709

**PASS: faithful full seed RED→GREEN. FAIL: the complete cohort has one independently reproduced HEAD failure.** This is one bounded Runtime correction; merge still requires independent Luna review and explicit disposition of the existing transcript-capture failure.

## Actual cause and correction

On exact Runtime base `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b` / tree `9b07545cac9a8bbafb16246aaa6f72050ef7cffe`, exact Agent `bac094180aef38a77b86ab165962e6159f873c60` / tree `3c9296e3670586e920f921c9b1b95bbb99b53b82`, the unchanged App seed script from `4c4c9c77c96fab70c4efef09db9a3bc456b0d803` reproduces `invalid_records: submitted assertion has no unique authenticated sequential binding`.

The actual failing claim is top-level `reads[0] = {kind: scope, ref: timeline, path: []}`, command ordinal `[0]`, dependency matching, cardinality **zero**. Agent `_commit_patch.py:282-289` faithfully records a timeline read as one `commit.read` binding per physical closure image, without a single `dependency` field. Runtime's matcher previously required that field. At ordinal 0 there are distinct parent bindings for `batch-read` and `input`; later step inputs expand to parent + shot + internal images.

`runtime_protocol/timeline_commit_auth.py` now verifies complete unique physical coverage on **both authenticated original and landing inputs**, separately for batch-read and step-input phases. Ordinary single-image claim matching is also phase constrained. It retains exact ordinal/source/owner/pin/history validation; it does not pick a first match, broadcast one physical match, equate bytes with identity, or accept capture presence as authority. The existing capture verifier authenticates pairs and pins before this matching runs. No port/store/contract/provider/pin changes.

## Faithful regression and limits

The bounded JSON fixture contains the exact 13,073-byte App `commitNativeSeed` Python script, SHA-256 `90f926fe13b7f20f1690eb21672451e0a82c51bd3c5b5ab45385a3da8e3721dd`. Its **21 commands, 21 steps and all 21 original assertions** remain intact. The test uses ordinary Runtime media import/selection and native Agent captures, retaining atomic merge, full raw parent/occurrence/shot/internal expectations, opaque values, receipt and request/document digest checks.

Only the SDK transport is adapted in-process: bundle opening returns Runtime's pristine bootstrap closure; committing invokes the public `RuntimeService.commit_timeline`, actual Agent provider, request-private port and durable store. No helper-only acceptance, HTTP/browser claim, credentials, daemon, extra publication, fields substitution or fixture stripping. Synthetic image/video bytes are imported through normal media services; this is a source-faithful offline seed reproduction, not the destroyed service20942 capture or a rerun of its browser journey.

The new positive also checks stored history, restart without a provider, exact-key replay and no database writes from that replay. Nine production-port negatives cover missing batch/step coverage, wrong ordinal, foreign physical source, outside alias, duplicate, ambiguous physical coverage, tampered source digest and wrong phase, each asserting refusal and complete database equality. The previous 57 cases are retained as an exact source prefix. The original Agent nine/five strict negatives and old qualified atomic scopes were neither edited nor rerun.

## Exact commands and results

All local commands run from `/home/user/work/wt/rt-R2r-fullseed-sequential-sol-1709` unless stated. Markers are deliberately included by clearing `addopts`; no default marker exclusions are inherited.

Focused acceptance:

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-bac09418 PYTHONPATH=.:packages/python:/home/user/work/wt/agt-pin-bac09418 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_sequential_verifier.py
```

PASS on the final exact source tree: **67 passed in 65.49s**, exit 0; `evidence/focused-final-tree.log`. Earlier complete focused run: 67 passed in 64.80s (`focused-final.log`).

Faithful seed RED, before source change: same command with `-k public_three_products --basetemp=/tmp/w-e58cf986ee/red-run`: **1 failed, 57 deselected in 13.03s**, at the exact reported matcher. `evidence/red.log`. A second observation-only reproduction retained the complete red packet and unchanged database hashes (`red-capture.log`).

Faithful seed GREEN with complete permanent capture: focused command with `PYTHONPATH=/tmp/w-e58cf986ee:.:packages/python:/home/user/work/wt/agt-pin-bac09418`, `-p seed_observer -k preserves_full_raw`, and `SEED_EVIDENCE=<worker>/evidence/green-complete`: **1 passed, 66 deselected in 24.13s**. Observer source retained in `evidence/seed_observer-final.py`; log `green-complete.log`.

Required nine-file cohort:

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-bac09418 PYTHONPATH=.:packages/python:/home/user/work/wt/agt-pin-bac09418 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_commit_inputs.py tests/test_timeline_commit_port.py tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_source_duplicate_authority.py tests/test_timeline_source_document_boundary.py tests/test_timeline_raw_capture.py tests/test_timeline_commit_sequential_verifier.py
```

**FAIL: 1 failed, 437 passed in 187.71s.** The sole failure is `test_created_child_public_captured_transcript_advances_sequential_manifest[None-True]`, described below. All 67 sequential cases pass in this final-source cohort. Full output: `evidence/cohort.log`.

I missed the cohort's existing localhost test before launching it directly. It passed locally, but that local launch did not follow the central-service rule. Its authorized central rerun was:

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-R2r-fullseed-sequential-sol-1709 targeted --files tests/test_timeline_commit_read_basis.py::test_generated_python_client_lists_commits_over_real_http
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test rt-R2r-fullseed-sequential-sol-1709-targeted-1023172033-11708
```

**PASS: 1 passed in 1.74s**, service exit 0 in 2s, exact final snapshot tree `f79a2355cfb39d9ada7721978bd20d5702105778`. `evidence/central-socket-summary` and `central-socket-log-txt`. This socket case uses its local PreparedProvider and does not qualify an Agent source tuple.

Static commands, both final tree and exact HEAD archive `/tmp/w-e58cf986ee/head`:

```bash
/root/.local/bin/ruff check runtime_protocol/timeline_commit_auth.py tests/test_timeline_commit_sequential_verifier.py --output-format json
/root/.local/bin/pyright runtime_protocol/timeline_commit_auth.py --outputjson
git diff --check
```

PASS: Ruff 0 diagnostics, Pyright 0 diagnostics; exact HEAD baseline also 0/0. Normalized identities **0 ADDED** for both; saved raw and normalized JSON under `evidence/`. Diff check exit 0. All 78 artifact hashes match declarations and HEAD, 61 tracked schema/package/generator files match frozen `34eac0041b0891e9011966b39bcbd26053fde5bc`, edit-command SHA-256 remains `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`. Other frozen controls/references, including the inherited `819acf` reference, were not modified; `819acf` is not a resolvable local Git abbreviation and is not presented as a newly verified ref. No files deleted.

## Independently reproduced HEAD blocker: one Agent capture owner needed

Exact HEAD archive, **without this patch**, exact Agent bac, from `/tmp/w-e58cf986ee/head`:

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-bac09418 PYTHONPATH=.:packages/python:/home/user/work/wt/agt-pin-bac09418 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider 'tests/test_timeline_commit_authentication.py::test_created_child_public_captured_transcript_advances_sequential_manifest[None-True]'
```

**FAIL: 1 failed in 9.88s**, same `invalid_records: sequential original or landing input does not match its authenticated head`; `evidence/head-transcript.log`. Observation-only rerun retained the full failed packet and no-write hash equality (`head-transcript-capture.log`, `transcript-head/`). Baseline loaded module paths/hashes are in `baseline-loaded-source.json`.

The actual source-to-capture mismatch is established: original and landing command-0 inputs replace the authenticated parent revision `authoring-parent-revision-93873646c209cca589320cfce38879f7ea217d4f2daea7139a39f447a67623d7` with `authoring-parent-revision-7ada0006a0b49533db80901c8c1b04e79fccf0ccbf21a5a60c8ca138c221dd86`. Captured input also already contains the new transcript document pin while the immutable source manifest has no document pins. Parent payload bytes are equal; parent physical pins are not. Runtime refuses before the new matching code is reached.

Exact producer seam: Agent `commit.py:1070` hydrates documents before `execute`; `document_from_bundle` at `:371-373` adds hydrated pinned documents and `:404-414` computes a different parent revision for the changed manifest. `_commit_patch.py:336` constructs the input Closure from that hydrated bundle, and `:458-461` exports that reconstructed closure as command input. Route this packet to **one Agent capture owner** to retain the true immutable initial pin while staging newly captured dependencies at their causal command boundary. Do not relax Runtime's pin comparison based on equal payloads. No speculative fix for this separate defect was made here.

## Custody and next steps

Permanent evidence root:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-fullseed-sequential-sol-1709/evidence/`

Flat portable packets are also exported under absolute ORCH `design/`, each with `.sha256`:

- `runtime-R2r-fullseed-sequential-1709-red-packet.json`: `4d61b786f88146437a66e22afd109c6ca4c5874513ae64298fb60862ed4dc6a4`.
- `runtime-R2r-fullseed-sequential-1709-green-complete-packet.json`: `7a5c9263afe0543439a822030c15273dedaf4779c6b042c6e2943939bc472141`.
- `runtime-R2r-fullseed-sequential-1709-transcript-head-packet.json`: `47ac8f6840f1c3d2086642979908aa11b0d858c449df28f1c37179eeb05fdb89`.

The red and green packets retain complete requests, original/landing plans and captures, candidate, physical binding pairs, history input, error/no-write or acceptance transition. The final green packet additionally includes actual public history and receipt/result. Generated local test identities are non-secret; no credentials or real service20942 private capture are claimed. Earlier failed observer instrumentation remains as experimental logs, explicitly superseded by `green-complete.log` and its packet; nothing was deleted.

No full/browser/original-nine/native journey rerun, schema/client/generated changes, shared dependency writes, daemon provisioning, Git writes, commits, pushes or merges. Independent Luna review remains required before merge. Recommended next step: review this narrow R2r patch, dispatch the single Agent capture correction using the separate HEAD packet, and requalify through normal dispatcher services. P2/P3 browser bodies remain unqualified by this offline work.
