# Registered assembler admission durability handoff

2026-10-20. Worker `agt-m2-assembly-admission-durable-flight`. **Qualified for the
exact task-create admission crash window**, ready for review/composition. No
render restoration or family remapping is claimed.

The existing TimelineSession outbox retains the original completed createTask
wire body and key before POST, using only the local `flight.kind =
assembly-admission` variant in that same JSON file. The existing atomic write
fsyncs file and directory. Untagged commit flights retain their existing format.
Normal prepare_admission runs once; normal dispatch_admission replays the exact
saved body under current transport credentials, without rebuilding capture or
reading child/media/head inputs. Session reopening resolves scope without opening
a current composition. Changed intent/key/scope refuses and keeps the original
flight. An ACK clears only the matching admission flight, preserving the session
base and newer pending timeline edits; it never creates accepted timeline history.
No second journal, table, accepted-history cache, fake EditCommand, public DTO,
wire field, schema change or HTTP framework was introduced.

Exact source tuple:

- Worker `/home/user/work/wt/agt-m2-assembly-admission-durable-flight`, branch `tl/agt-m2-assembly-admission-durable-flight`.
- Base registered requester commit `32d6de6a8a50f05032a9b1f110ff1ac5a8975f4f`, tree `4c000d64c9048910889266f00fd4036a47ffebd3`.
- Central qualified source tree **`4ffb60245f1dd3e723073da3e0a957ee6e09b3d9`**.
- Final tracked source tree **`a0650c21b268f879969a9420bdb2921e4008289b`**. Only the original local strict-xfail decorator was removed after the central pass; product/HTTP source bytes are unchanged. Final local tests pass. Tree hashes were computed read-only, with the pre-removal calculation matching the central snapshot; no commit/release identity is fabricated.
- Product SHA256: `astrid/sdk/timeline/assembly.py` = `e5faf15b139c4da8463da3b01dedd6c746f9d8ef41ba8927eddec30cef7ef346`; `sync.py` = `6c82655db96e8ff6d15fb08eacb2263683af2f55664acef79992db3f79e79781`.
- Existing outbox implementation is unchanged, SHA256 `dfb1e46123be49539cf053a9e49060d9c8ad1ec73f15393a3a1d3427dac95a99`. Product diff: **+78/-16**, only assembly.py/sync.py.
- Private native Agent parent `b5cfce5096f91f39bfb86d39823f97f0f59ce8a2` plus the complete existing `tests/helpers/registered_native_pair.py` overlays; Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
- Private normal generator contract version `0.2.14`; whole 53-definition schema/full S2 floor SHA256 `fafb1985a326e6121aa8c9fb34bbda196edc3dfaf462352070372e631bea1f52`; unchanged normal artifact manifest `sha256:48c7b6533e2774a70e36517948a18fd5cee07f4d30e8f339776be9b3ec74ed4e`. Normal Python/TypeScript generation/checks and all 75 artifact hashes pass; no public contract/lock mutation.

Final central command:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
$ORCH/bin/request-test agt-m2-assembly-admission-durable-flight identity-pin94114269-integration --files tests/packs/rendering/test_registered_native_pair.py
$ORCH/bin/wait-test agt-m2-assembly-admission-durable-flight-identity-pin94114269-integration-1020131041-30429 1
```

**Exit 0; inner 15 passed, 2 held legacy xfailed; outer 4 passed.** The outer
three unchanged identity controls use Runtime `94114269d1ce23ab3224d7eca5a85138ce2b5fed`;
the inner native qualification uses the private tuple above. The original nine
native action/proposal/requester positives pass, plus four new real HTTP recovery
cases and two existing regular command ACK-loss/restart/suffix/inverse journeys.
The new cases cover distinct/duplicate CAS, task acceptance followed by dropped
HTTP ACK, crash after ACK before outbox cleanup, actual Runtime/requester restart,
head C and child association V2 after original acceptance, fresh same-actor
credential, authenticated foreign-actor refusal, changed intent/key refusal with
unchanged flight, byte-exact original request/key replay, original task/receipt,
one durable task, unchanged stored spec/history and pending suffix preservation.
Tripwires forbid head inspection/history during reopen and preparation/media reads
on retry. No runner task is deleted.

After that pass, the original strict admission xfail became a real positive with
its retry expectation retained and stronger no-recapture tripwires. Local command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_sync_native.py tests/packs/rendering/test_runtime_stitch.py tests/packs/rendering/test_assemble_timeline.py
```

**133 passed in 25.53s**, including the original 123. Scoped Ruff and
`git diff --check` pass. No full/full* run, shared dependency/cache mutation,
integration edit or git mutation. Report contains exact lint/development commands.

Remaining limits: one exploratory whole M1 journey passed commit recovery and undo
then failed its archived cohort's `visualize` call because `create_timeline_view`
lacks an idempotency key. That code/test is unchanged and that whole journey is
not green here. No render/decoded-film/pixel/audio/macOS evidence, public native
release activation, historical render, render admission recovery or D13/legacy
completion qualification. The two held legacy strict xfails stay intact. Child
bytes are small fixtures labelled video. This is a private normally generated
cohort qualification, not a public release identity.

Next: compose these narrow hunks with the reviewed native requester cohort,
preserving the current root's newer stage/sheet-basis/producer-pending guards;
do not replace current sync.py wholesale from this older branch. Qualify that
composed release normally. The source owner should separately fix/requalify the
M1 visualize call. No PLAN decision was changed and this bounded task has no blocker.

[Full worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-assembly-admission-durable-flight/notes/report.md).
[Final central log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-assembly-admission-durable-flight-identity-pin94114269-integration-1020131041-30429/log.txt).
