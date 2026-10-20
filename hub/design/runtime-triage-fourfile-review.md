# Runtime four-file triage review — APPROVE

Independent read-only review completed 2026-10-20 by `rt-m2-triage-fourfile-review`.

**APPROVE the four-file source unit. No blocking finding.** This approves the reviewed source and its recorded evidence; it does not claim a tested merge onto the newer S2 integration tree. No product, test, dependency, pin, publication, or Git state was changed during this review.

## Exact scope

- Candidate: `9abc5c65de784d8d04bc5af2284fbc365ca625fa` (`tl/rt-m2-triage-clean-current`). Tree: `0c4887d04467f1b269570255d80283fed9667967`.
- Comparison base: `642eef7467a6b766480df3f34e7377e8d755fe92`. Tree: `28d91969970396579041ef1a64501b919c4cd5fd`.
- Current-port comparison: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`. Tree: `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Exactly four changed files: `runtime_protocol/store.py`, `tests/test_render_historical_admission.py`, `tests/test_spec_reference.py`, `tests/test_timeline_pack_inputs.py`. Diff: 83 insertions, 27 deletions.
- Read PLAN.md first. Surrounding implementation and shared test helpers were read only to establish the four-file change's behavior and compatibility.

## Proven findings

### Snapshot exception conversion is narrow and preserves refusal

At candidate `store.py:2462`, the new handler converts only `NotFoundError` with the exact message `timeline snapshot reference object is missing or corrupt`, only when the request is historical and an earlier Runtime render admission was found. It preserves the established `ConflictError` details: `reason=render_revision_integrity`, `dependency_id` equal to the Runtime-built snapshot digest.

At `store.py:2575`, the existing later historical-replay handler is narrowed from all `ConflictError`/`NotFoundError` to that same specific object-integrity error. Parent-revision missing/changed errors, invalid digest/project validation, and outside-project custody conflicts retain their own errors. First admissions and nonhistorical admissions do not gain this conversion. Historical requests reject caller-supplied snapshot references and capture snapshots during freezing, so the converted reference is the Runtime-built retained snapshot, not an arbitrary caller-selected snapshot.

The two handlers cover distinct damage cases. If an indexed snapshot's bytes are missing/corrupt, preparation rejects it early. If its object metadata is absent, the prepared snapshot can pass the read-only preparation check, but replay validation without `prepared` rejects it before publication. Neither handler repairs bytes or writes anything.

### Historical integrity, archive checks, and replay ordering remain intact

`create_task` still reads prior persisted render admission evidence before freezing; normalization and full stored-request equality checks remain before receipt reuse or reconstruction. Historical publication remains deferred until admission guards, input checks, readiness/storage checks, and replay resolution have passed. The early snapshot rewrite calls `prepare_snapshot`, which validates provenance without publishing CAS or writing rows.

Archive refusal remains live for first admission and replay. First admission checks `timelines.archived_at`; replay's history lookup calls `TimelineCommitStore._membership`, which also excludes archived timelines, before any replay result is returned. The fixture now sets only the scoped archive timestamp under the store mutex and transaction, asserts one row changed, then retains the original refusal and complete database/CAS/staging equality assertion. Calling the retired `archive_timeline` method would refuse before creating the state this test needs.

Tests still verify selected A after later C and restart, exact snapshot/config/registry and immutable dependency bytes, receipt/publication identity, current-C control, replay before and after restart without writes, selector mismatch, corrupted media and custody, parent/dependency/event integrity, late admission refusal, and missing/corrupt replay snapshot refusal. Their expected behaviors were not rewritten into refusal-only substitutes.

Commit replay remains ledger-first: `CommitExecutionCoordinator.execute` looks up the accepted result before creating a request port or calling the semantic provider. The pack retention positive still asserts exact retry equality, unchanged database state, and `provider.calls == 0` after restart. This four-file patch does not modify commit coordination. Render replay deliberately rechecks retained integrity/archive authority before returning; it is not a bypass of those checks.

### Fixture repairs retain meaningful positive coverage

- Historical fixture: its prerequisite installs a factory returning `load_timeline_commit_provider("astrid")` before `canonical_scene` registers the provider and creates the timeline. The loader imports the real `astrid.sdk.timeline.commit` factory and validates it. The fixture no longer attempts a forbidden second provider registration. A and C are still real Agent `capture_move`/bundle commits through the Runtime commit path. No fake Agent module, private product overlay, or prepared-provider replacement for those measured edits was introduced.
- Seed: `_accept_publication` uses the existing real `TimelineCommitStore.accept` fixture boundary, recording acceptance/history/receipt data rather than fabricating revision SQL. It is fixture preparation, not evidence that Agent authored the seed command. The updated seed selector reads the accepted revision and canonical-parent digest from the real acceptance envelope.
- Visualize: real provider registration precedes timeline creation. A real accepted retained parent is projected by `provider.project_capture`; admission, CAS reference readback, and the real `GenericPackHost` materializer remain exercised. The deliberate source deletion now disables foreign keys only within the isolated corruption setup and restores them in `finally`. The original missing-source claim refusal remains.
- Pack: the only fixture change adds a `media.import_bytes` transport adapter delegating to real `service.ingest` with project, bytes, MIME, filename, and idempotency key intact. It restores admission's media dependency without bypassing Runtime ingestion. Existing portable CAS custody tests remain unchanged. The older local-cache resolver positive is still explicitly limited to the Document boundary, not claimed as full Agent activation/CAS hydration proof.

AST comparison found no removed test functions: historical 18→18, spec reference 7→7, pack inputs 13→13. Only the archive fixture consumer, seed-selector consumer, and visualize test bodies changed. All three files contain zero `xfail`, `skip`, or `skipif` markers before and after; no behavior expectations were weakened.

Nonblocking naming limitation: `test_real_retained_legacy_publication_uses_verified_source` now selects a recorded acceptance fixture receipt, not a legacy `parent_composition.publish` receipt. Its positive retained-publication assertion remains valid, but the name must not be cited as new proof of the legacy receipt branch. No legacy publication API was re-enabled for this repair.

## Exact evidence inspected

All four central `snap` files identify candidate tree `0c4887d04467f1b269570255d80283fed9667967`, byte-identical to the held commit. Inspected each `request`, `snap`, `summary`, and `log.txt`; inspected external-source records where present. The ordinary 76-test result is a **direct worker run**, not a central result.

1. Direct ordinary run, source worker `log.txt:6001–6006`, exit 0:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m 'not integration' tests/test_render_historical_admission.py tests/test_spec_reference.py tests/test_timeline_pack_inputs.py
   ```

   **76 passed, 59 deselected in 43.27s.** No independent central snapshot stamp accompanies this direct run; the subsequent central results do stamp the candidate tree.

2. Central `rt-m2-triage-clean-current-marked-integration-1020094826-20361`, exit 0:

   ```sh
   env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -n 3 -m integration tests/test_render_historical_admission.py tests/test_spec_reference.py tests/test_timeline_pack_inputs.py tests/test_canonical_render_admission.py
   ```

   **59 passed in 47.41s.** This includes historical positives/negatives, archive cases, restored visualize, and real pack admission.

3. Central authority neighbors `rt-m2-triage-clean-current-targeted-1020095200-18164`, exit 0:

   ```sh
   /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_canonical_render_admission.py tests/test_snapshot_authority_refusal.py tests/test_snapshot_preflight.py
   ```

   **113 passed in 76.37s.**

4. Formerly queued focused run `rt-m2-triage-clean-current-marked-integration-1020095603-18620`, now complete, exit 0:

   ```sh
   env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -n 3 -m integration tests/test_render_historical_admission.py::test_historical_replay_never_repairs_a_missing_or_corrupt_snapshot tests/test_spec_reference.py::test_visualize_task_hydrates_exact_saved_revision_and_refuses_missing_source
   ```

   **3 passed in 4.08s** (both missing/corrupt parameters plus visualize).

5. Formerly queued `rt-m2-triage-clean-current-commit-integration-1020100130-17053`, now complete, exit 0:

   ```sh
   env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/test_timeline_commit_integration.py
   ```

   **9 passed in 11.67s.**

Central evidence directory root: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/`. Direct source log: the corresponding `orch/workers/rt-m2-triage-clean-current/log.txt`.

External provenance limitation: central commands use the real shared Agent checkout, not a frozen Agent snapshot. The 59-test run's `ext` monitoring records span Agent `efb96034fc7c80a6e73900bfc57dac53260beb3c`, `26c3b0a8229ec78b670097df60b539d70be55428`, and `76737ca2f9c86a075e7e03dfc8990e3090acc234`; the later focused/commit monitoring spans `df2739f903edac02bd36b4446deeea847524c040` and `e2ad59584addc892f1a6dd9fd644c75f80a2e28f`. Those records establish the real checkout context but do not establish one immutable Agent SHA for every test. App/Composition records show `18becfbede00038830b97e63345445eeef54fa42` / `e80c46baf5aa4b50a10b77a5ceadcb7ec4ab27ab`. No frozen current-tuple qualification is inferred.

## Independent cheap checks and current-port guidance

Executed from the assigned clean `2c4ac180` worktree:

```sh
git diff --check 642eef7 9abc5c65
git diff 642eef7 9abc5c65 | git apply --check -
git status --porcelain
```

Whitespace check passed; all four source hunks apply cleanly without writing; worktree status remained empty. An inline Python AST/`compile()` check of all four `git show 9abc5c65:path` sources passed and verified the test counts/markers above without writing bytecode. No pytest suite, full suite, broad repeat, live socket, or browser run was requested or executed by this reviewer.

**No required code adjustment found for the current port.** Against `642eef7`, current integration changes `store.py` only in storage estimation/seam commentary, away from these replay handlers; the three target test files are unchanged. Preserve current S2 storage estimates and seam behavior by applying the reviewed hunks, not by replacing `store.py` with the old candidate file. Current `create_timeline_view` requires an idempotency key, but these four files do not call it; their shared acceptance helper and provider loader remain compatible by inspection. No view-key addition is required here.

Recommended next step: the orchestrator may port only the approved four-file diff, then qualify that actual composed tree with the focused historical/visualize cases, relevant fixture tests, and commit integration using the intended real Agent source. Existing results qualify the held tree, not an untested composition with `2c4ac180`. No full or broad repeat is recommended by this review.

Agent Linux custody/activation identity failures and the ordinary stale client pin remain separate work. They were not patched, waived, or counted as passing here. No new decision was needed beyond distinguishing approval of this source unit from current-tuple qualification. Review itself has no blocker.
