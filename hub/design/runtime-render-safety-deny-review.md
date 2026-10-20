# Runtime render safety denial: APPROVE

Independent read-only review of owner11:47's narrow old-endpoint refusal.
No blocking finding in the reviewed change. Approval covers this refusal only.

- Final harness commit: `693462918509964803ae6c127b9b8038a4ac7bf4`.
- Final tree: `a53f2af3f58f763bc7c93419d94864c9a9f0029a`.
- Parent/base: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
- Source worker DONE and harness commit verified before verdict. Central final
  snapshot tree equals the committed tree exactly; no moving WIP was approved.

## Findings

`runtime_protocol/service.py:6694` obtains target authority from the persisted
hash-verified task spec through RealmStore._spec/_load_spec, at the existing
`spec.runtime_dependencies.publication.timeline_id`. The request supplies only
the target being compared. Existing attempt identity, live fence, admitted
continuation and run-project checks remain. Missing/malformed publication data,
corrupt immutable spec and inconsistent optional native target fail closed.
A native declaration alone cannot authorize this legacy publisher. Requiring a
new native pair for every legacy publication would lose legitimate legacy
behavior; no new DTO, public guard or renderer dependency is needed here.

The scoped non-null `parent_composition_heads.publication_id` check refuses
tracked targets without consulting or repairing their history. Corrupt history
therefore cannot make a tracked target eligible. It matches the existing legacy
parent-publication boundary; a revision with null publication ID remains eligible.
Tracking another timeline does not block the admitted legacy target.

The guard runs before checkpoint preparation under the existing store mutex,
and again at line 6811 inside the existing BEGIN IMMEDIATE transaction, before
legacy document UPDATE, timeline/task events, CAS snapshot, render task or completed
checkpoint effects. Canonical acceptance uses the same store mutex; the final
check and downstream writes also share SQLite's write lock. The two permanent
negative diagnostics compare the entire SQL dump, CAS/staging bytes and
SQLite total_changes: all remain unchanged, including no new checkpoint.

TOCTOU qualification is precise: the test introduces real canonical tracking at
the separately committed prepare seam. The second guard refuses with no further
SQL/CAS/staging changes and preserves the readable canonical head. The existing
prepared checkpoint remains prepared; the entire invocation is NOT claimed to
be state-free across this injected race. This preserves the existing restart
checkpoint contract and adds no new state mechanism.

Exact published-checkpoint replay and changed-payload refusal remain before live
lease/spec/target checks. Original render-task identity replays unchanged after
tracking, author cancellation, spec loss and target archival, with no SQL/CAS
changes. Different payload under the same authoring identity refuses. The three
original successful legacy publication/cancel/restart controls retain their
assertions; their fixture now supplies the existing target declaration through
normal create_task admission. The additional legacy-head positive retains normal
publication with a null canonical publication ID.

The final diff contains only service.py (+32/-1), the legacy test fixture
(+10/-2), and 150 lines of permanent boundary tests. No compatibility writer,
legacy row creation, canonical write, worker scope expansion, schema/client/pin
change or family remap was introduced. SQL-seeded historical documents remain
explicit legacy/adversarial fixtures, not evidence of normal registered creation.

## Verification

All independent direct checks ran against a private `git archive` of the final
commit, with shared dependencies read-only and bytecode/pytest caches disabled.
Let `O` be the absolute ORCH directory containing this report, and
`W=$O/workers/rt-m2-render-safety-deny-independent-review`. Working directory for
the following commands was `$W/review-source` (the extracted final commit).

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:$PWD/tests /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --basetemp=$W/probe-temp $W/test_independent.py tests/test_timeline_render_publication.py tests/test_timeline_render_publication_authority.py
```

Initial independent run: **24 passed, 1 failed in 13.21s**. All **20 permanent
publication tests passed**. The failure was private probe setup: deleting retained
history violated a foreign key before invoking the route. A second private-only
run was **4 passed, 1 failed in 3.24s**, because invalid JSON fault injection was
correctly rejected by the schema CHECK. No product defect or behavior expectation
was changed. Final probe corrupts the retained history project sequence instead,
and first proves canonical head() refuses it; the other variant removes its
receipt. Both then prove legacy publication refuses with whole SQL/CAS unchanged.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:$PWD/tests /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --basetemp=$W/probe-temp-final2 $W/test_independent.py
```

Final private probes: **5 passed in 1.15s**, exit 0: corrupt retained history,
missing receipt, foreign-project target, missing publication at authentic task
admission, and final guard executing inside the write transaction. Private probe
source is retained beside this worker's DetailedReport; extracted source and test
realms were cleaned up. Recreate the archive from the commit above to rerun.

Verified source-worker evidence:

```sh
env PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_render_publication.py tests/test_timeline_render_publication_authority.py
```

**20 passed in 36.71s**, final source.

```sh
env PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_render_publication.py tests/test_timeline_render_publication_authority.py tests/test_timeline_headless_overwrite_refused.py tests/test_timeline_commit_baseline.py tests/test_timeline_producer_guards.py tests/test_timeline_producer_checkpoint.py tests/test_timeline_commit_acceptance.py tests/test_task_continuations.py
```

**204 passed, 1 integration deselected in 119.23s**, identical product source;
collection preceded the final added legacy-head positive. This is source-worker
evidence, not an independent broad rerun.

Final exact central service gate:

```sh
$O/bin/request-test rt-m2-render-publication-safety-deny commit-integration
$O/bin/wait-test rt-m2-render-publication-safety-deny-commit-integration-1020115603-31699 1
```

Expanded command:

```sh
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/test_timeline_commit_integration.py
```

**9 passed in 12.79s**, exit 0; status, snapshot and raw log inspected at
`$O/tests/rt-m2-render-publication-safety-deny-commit-integration-1020115603-31699/`.
Snapshot tree exactly matches the approved commit. Recorded external Agent:
`cf7448ed6c1298b172d004914cfe2bb8c99048e7`.
`git diff --check 2c4ac180 693462918509964803ae6c127b9b8038a4ac7bf4` passed.
Reviewer worktree status remains clean. No full or socket/browser suite was run
by this reviewer and no duplicate service gate was requested.

## Limits and next steps

Registered normal-create assembler completion remains an explicit OPEN GAP; the
original strong completion tests/source remain untouched and strict, and were
not rerun here. This approval does not qualify D13 retirement, registered native
settlement, film output or a final delivery tuple. Agent's 11:49 mapping ACK keeps
`rendering.assemble_timeline` distinct from `rendering.render`; public stitch names
remain render-mapped. Native requester -> registered action -> normal settlement
-> requesting client/outbox -> commit remains Agent-owned.

Recommend accepting the exact reviewed safety commit through the normal manager
process, then separately qualifying that native positive. No blocker for this
bounded review. No product edits, Git mutations, integration changes, publishing,
shared dependency writes or new approval requirements were introduced.
