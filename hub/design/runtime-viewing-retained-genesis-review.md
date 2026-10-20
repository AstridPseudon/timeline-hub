# Runtime retained-genesis fixture review

## Decision

Approve the bounded test-only setup, with the exact boundary already accepted by Owner13:46. The existing supported public constructor does **not** suffice for this non-empty retained closure: `create_timeline` only creates/adopts the empty initial publication, while the ordinary S2 commands require existing shot/internal/occurrence owners. I recommend the proposal's narrow private setup in a new caller-owned ephemeral realm, followed by the ordinary restore path. This is not a production writer, importer, endpoint, DTO, or capture-certification mechanism.

The setup is acceptable only when it:

- calls `RealmStore.initialize`, normal `create_project`, normal `create_timeline`, and normal `ingest` first;
- calls only existing `TimelineCommitStore._validate_closure` and `_persist_closure`, under the store's existing mutex and transaction, before the daemon/service is started for the first time;
- uses a new realm path owned by that test and leaves the empty parent head, history, receipt, and accepted publication untouched;
- closes setup before normal service startup, then restores through the sole existing `timeline.restore` command over `/v1/projects/{project}/timelines/{timeline}/commit`, using the real empty head pair and exact retained parent content digest;
- relies on the normal provider, normal Runtime capture validation/admission, and the server's own publication/claim state; and
- keeps the fixture still-image-specific. It does not replace the three-clip/video/audio parity cohort.

Reject the setup if it is used on an occupied/reused realm, writes raw SQL or head/history/certificate/snapshot-reference rows, adds a production helper/API/DTO, publishes the retained parent before restore, uses a non-restore command, bypasses the native mutex/transaction, or substitutes synthetic acceptance for the normal restore/capture path.

## Evidence

Source under review:

- Runtime worktree `/home/user/work/wt/rt-m3-viewing-genesis-fixture-review`, commit `b748ae7` (`tl/rt-m3-viewing-genesis-fixture-review`); current Agent provider source `/home/user/work/agent`, commit `8e310785` (`tl/integration`).
- Supplied proposal and fixture files under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-frame-retained-genesis-fixture-*`.
- Relevant current Runtime code: `runtime_protocol/service.py` (`create_timeline`, `commit_timeline`, `create_task`), `runtime_protocol/timeline_commit_store.py` (`revision_closure`, `_validate_closure`, `_persist_closure`), `runtime_protocol/capture_validation.py`, and `runtime_protocol/snapshot_refs.py`.

Exact commands and results:

1. Native owner witness, using the current Runtime worktree and current Agent integration provider:

   ```sh
   PYTHONPATH=/home/user/work/wt/rt-m3-viewing-genesis-fixture-review:/home/user/work/agent \
     /home/user/work/venv-runtime/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider \
     --basetemp="$witness_dir" \
     /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/\
     handoff-vw-m3-frame-retained-genesis-fixture-proposal.py::test_owner_retained_genesis_restore
   ```

   Executed with `witness_dir=$(mktemp -d /tmp/rt-m3-retained-genesis-witness.XXXXXX)`. Result: **1 passed in 1.27s**. It proved inactive setup, complete retained closure reread, normal restore, exact idempotent retry, accepted head identity, retained source equality, and `integrity_report()["ok"]`.

2. Supplied pure fixture/projector/compiler test, explicit file filter:

   ```sh
   PYTHONPATH=/home/user/work/wt/rt-m3-viewing-genesis-fixture-review:/home/user/work/agent \
     /home/user/work/venv-runtime/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider \
     --basetemp="$test_dir" \
     /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/\
     handoff-vw-m3-frame-retained-genesis-fixture-fixture-test.py
   ```

   Executed with `test_dir=$(mktemp -d /tmp/rt-m3-supplied-fixture.XXXXXX)`. Result: **8 passed in 0.92s**.

3. Bounded retained-fixture capture witness (temporary `/tmp/rt_m3_exact_capture_witness.py`, no repo copy): same setup and restore, then normal `RuntimeService.create_task` capture admission and `claim_next`. Mutations were config, registry, child/shot digest, and missing managed media; each was required to refuse. The unchanged capture was required to admit and claim the retained revision pair.

   ```sh
   PYTHONPATH=/home/user/work/wt/rt-m3-viewing-genesis-fixture-review:/home/user/work/agent \
     /home/user/work/venv-runtime/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider \
     --basetemp="$test_dir" /tmp/rt_m3_exact_capture_witness.py
   ```

   Executed with `test_dir=$(mktemp -d /tmp/rt-m3-capture-witness.XXXXXX)`. Result: **5 passed in 3.83s** (four refusals, one unaltered admission/claim). This is bounded native admission evidence, not renderer or browser evidence.

4. Existing Runtime capture negative/positive cases, explicit file and `-k` filters:

   ```sh
   PYTHONPATH=/home/user/work/wt/rt-m3-viewing-genesis-fixture-review \
     /home/user/work/venv-runtime/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider \
     --basetemp="$test_dir" tests/test_snapshot_authority_refusal.py \
     -k 'forged_capture or exact_saved_capture'
   ```

   Executed with `test_dir=$(mktemp -d /tmp/rt-m3-capture-negatives.XXXXXX)`. Result: **10 passed, 15 deselected in 4.63s** (altered config/registry/shot digest refusals and unaltered saved-capture admissions).

   ```sh
   PYTHONPATH=/home/user/work/wt/rt-m3-viewing-genesis-fixture-review \
     /home/user/work/venv-runtime/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider \
     --basetemp="$test_dir" tests/test_timeline_commit_restore_port.py \
     -k 'test_restore_rejects_damaged_exact_source_before_provider_or_writes and (media or missing_media)'
   ```

   Executed with `test_dir=$(mktemp -d /tmp/rt-m3-restore-media.XXXXXX)`. Result: **4 passed, 47 deselected in 1.53s** (corrupt and missing retained media, direct and adapter restore forms).

## Approval/rejection conditions for downstream App use

Approve downstream use only after the App owner inserts preparation before the first `DirectHarness.startRuntime`, starts the ordinary authoring profile, provisions the ordinary product credential, submits the ordinary restore, and consumes the server-returned head. The App path must not call compatibility `seedRuntime`, the second compatibility publication, or invent generic video/big-download fields for this still fixture. The normal capture caller must submit its actual snapshot; only the Runtime admission path may issue its accepted reference/claim.

Reject downstream qualification if any mutation is admitted, if a refusal changes canonical rows/CAS unexpectedly, if a missing/corrupt media dependency is not refused, if the accepted result differs on exact retry/restart, or if the frame/audio renderer gate is inferred from this still-image witness. No browser, live socket, renderer, audio, full suite, or App integration was run here.

## Worktree/result

No Runtime product files were changed. No shared dependency/cache, pin, authority, merge, or Git ref was changed. The worktree is clean.
