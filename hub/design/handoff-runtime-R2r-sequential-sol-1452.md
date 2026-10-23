# R2r/R1 sequential verifier — source corrected; production qualification BLOCKED

The exact current Agent original-nine acceptance is **not achieved**. No new public body was run: the task requires complete 1435 inputs before another body, and those four captures were cleaned with its scratch directory. Runtime validation and retained-packet causal verification pass, but they are not production qualification. No DONE marker is claimed.

## Exact source and scope

- Runtime branch: `tl/rt-R2r-sequential-sol-1452`; HEAD/base `cfa0af0d476e6954df041c08d7ef378fd6782932`; base tree `3675f446c82c455ef5635ae725409eb6076a4f83`.
- Final candidate tree, computed from Git object encodings without writing Git: `c588dcc500c5f5e68fe3b2a61e9c16ead55d5313`. Per-file SHA-256 values: `evidence/source-manifest.json`. The harness must create the own commit; its future commit ID is not asserted here.
- Agent ready checkout: `/home/user/work/wt/agt-pin-67ba416b`, clean HEAD `67ba416bca813f4931b557f6f2ca2abf935d7d35`. Its source/tests were not changed.
- Waited for predecessor terminal `ended`/`BLOCKED`; imported ONLY the five allowed files from cumulative `cfa0..343664dc79644a38b7dbabc180bacb84587e7a2e`, through file writes, onto fresh current integration. No c8c ancestry or report branch was inherited.
- Changed four Runtime files (private Protocol, request port, auth, minimum store plumbing), one new verifier test file and one 200,611-byte real-capture JSON fixture. No tracked reports or scratch files.

All existing authentication functions except `validate_step`, `validate_bindings`, and `validate` are byte-identical to the current base, including inverse-stage, source-allocation and native projector helpers. Complete six-path scope checks preserve contract/schema/generated/client/lock/pin/ratchet files, including the frozen client surfaces. No public request, prepared shape, history edge or wire API change.

## Recovery and causal correction

Recovered the **original bytes** of 1435's handoff with `git show 343664dc:design/handoff-runtime-R2r-sequential-return-1435.md` and published them at the actual absolute ORCH/design path. SHA-256 `6a32d2c02012bc85b9e2cbac99755068c5bf28a3c87181f75cd675c3c0580430`. Also recovered its 1428 handoff unchanged. Full predecessor/reviewer logs are preserved in this worker's durable `evidence/`.

The predecessor worktree and `/tmp/w-2f30f24c4d` are absent; its durable worker has no capture directory; its commit tracks reports only. Parsing its full log finds the older 59e329 full packet, but no complete 1435 captures. The four 14:42 attempt hashes and partial diagnostics survive and are preserved; complete bytes cannot honestly be published. Absolute flat recovery inventory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-R2r-sequential-sol-1452-recovery.json`. This explicitly records absence, not a substitute completepacket.

1435's offline claim tested `validate_sequential_capture` alone. Running the actual two-stage consumer chain (`validate_sequential_capture`, then normal landing `validate`) on retained 59e329 initially refused all four captures at submitted-assertion resolution. The fix authenticates submitted patches/reads at original command/step inputs, then joins their unique verified bindings to the landing command input. Submitted requests remain unchanged; unlanded original aliases never enter accepted history.

Capture custody detaches finite JSON once, binds exact request context and entire prepared digest, consumes before validation, and clears on invalid/CAS/closed attempts. Records/images reuse existing closed schema validators; ordinal/range checks reject bools, floats, negatives and out-of-range indices. Every nested replay transition checks ordering, original/landing materialization, physical images, complete owners and terminal correspondence through authenticated history. Normal projection checks authenticate both sequences against BASE/HEAD and preceding effects rather than accepting adjacent snapshots alone.

Added packet-based tests for coordinated snapshot/record/source/map/digest tampering, missing/duplicate bindings and map entries, future/nested-self/foreign lineage, malformed capture JSON, ordinal bounds, detachment and consumption after successful/invalid/CAS attempts. Existing passing behaviour tests were not rewritten, skipped, deleted or weakened.

## Commands and results

All commands below ran in the assigned Runtime worktree unless a baseline directory is stated.

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_commit_inputs.py tests/test_timeline_commit_port.py tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_source_duplicate_authority.py tests/test_timeline_source_document_boundary.py tests/test_timeline_raw_capture.py tests/test_timeline_commit_sequential_verifier.py
```

**353 passed in 85.25s** on final source, including 44 verifier tests. Full log `evidence/runtime-final.log`. Earlier development group: 337 passed; later 352 passed. A new lifecycle test initially used an empty PreparedCommit and encountered a pre-existing materialization KeyError; it was corrected to a valid-shaped candidate with an invalid digest to exercise the intended invalid-attempt path. Empty PreparedCommit handling was not changed. Earlier new-file run was 42 passed/1 failed at that test; final group above passes.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python:tests /home/user/work/venv-runtime/bin/python /tmp/w-5c47cf149b/offline_packet.py
```

**4 PASS**, both verification stages, on all exact retained 59e329 capture values. Script retained at `evidence/offline_packet.py`; origins/log at `evidence/offline-final.log`. These are older producer transport captures (moved head, reads absent/present, preview/accept), not the missing 1435 attempts, fresh-head positives or current Agent acceptance.

```sh
/root/.local/bin/ruff check --no-cache runtime_protocol/timeline_commit_auth.py tests/test_timeline_commit_sequential_verifier.py
/root/.local/bin/pyright runtime_protocol/timeline_commit_auth.py
/root/.local/bin/ruff check --no-cache --output-format json runtime_protocol/timeline_commit.py runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py tests/test_timeline_commit_sequential_verifier.py
/root/.local/bin/pyright --outputjson runtime_protocol/timeline_commit.py runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py
python /tmp/w-5c47cf149b/final_checks.py
git diff --check
```

Auth/new-test Ruff **PASS**; auth Pyright **0 errors**. All-changed raw Ruff exits 1 with **22** existing diagnostics; all-runtime raw Pyright exits 1 with **80** existing diagnostics. Exact base comparison uses path/message/code plus source-line identities, preserving multiplicity: **0 added, 0 removed** for both tools. Base was read using `git archive HEAD runtime_protocol packages tests pyproject.toml`, extracted only into `/tmp/w-5c47cf149b/baseline`; identical commands ran there (new test excluded because absent on base). Raw JSON/comparisons and reproducible final-check script are retained under `evidence/`. Scope, computed base-tree cross-check, byte preservation and whitespace **PASS**.

Required current Agent command, **NOT RUN** because predecessor input prerequisite is unmet:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-67ba416b PYTHONPATH=/home/user/work/wt/agt-pin-67ba416b:$PWD:$PWD/packages/python /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider /home/user/work/wt/agt-pin-67ba416b/tests/editing_conformance/test_doc_patch_sequential_rebase.py
```

No full suite, localhost/browser/live socket run, shared dependency/cache write, Git write or public recapture occurred.

## Remaining split and next owner

The missing evidence prerequisite belongs to orchestration/predecessor artifact custody: recover the complete four 1435 input packets from preserved storage if available. Their absence is not permission for a blind recapture. The candidate then needs the one genuine original-nine run against exact current-only Agent 67ba, with observer capture persisted before validation in absolute worker/evidence and flat design, including full prepared/base/head/history/maps/context, before/after origins and no-write evidence. Stop on any new refusal. All four real positives and five strict negatives remain unqualified on this candidate; deeper multi-hop positive lineage has no retained real fixture here. Independent Luna review must follow before any merge. Frozen gates remain held. No settled PLAN/C0 decision was changed.
