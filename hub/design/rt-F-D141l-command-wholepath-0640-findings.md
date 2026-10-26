# F D141l whole-path investigation — FAIL7 confirmed

Investigation date: 2026-10-26. This was one finite, read-only source pass. No
request-test, test-run, body, collection, product import, service admission,
receipt admission, registry, kit install, or acceptance action was run.

The ordinary source-worker admission was dispatched by the orchestrator at
`4608532480` available bytes, `2026-10-26T06:50:42.455577+00:00`. The required
continuous trace is retained in `disk-trace.txt`; its first sample is above the
4,000,000,000-byte stop and its terminal sample is recorded after analysis.

## Source identity and authenticity

The current clean source tuple was verified read-only: Agent
`ecdc242ed9b673f641759ecf029f95e89a2c6f92` / tree
`d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`, Runtime
`95d98f038320d5d46bd679ac000ab3e15825c935` / tree
`78df31d62c5b9ba4c84dee4ea346e43a767718c1`, App
`4de54db14bdc9ddc2ce2e5887258b03acbffd30d` / tree
`84c3fb7f73f08c22220f8e808962fe3f24aaa0aa`, and Composition
`635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / tree
`5ab5191a296980a0a6bcd1178ab6902d6478a148`.

Pristine Agent `64197afa297f86f1e738238d5e80aff6d33e303a` / tree
`6c0488b3efdfa47479b0ad1b7bd20608383be26e` was inspected with `git show`: the
published claimed root `tests/v10/timelines_create.py` is absent, while
`tests/v10/test_timelines_create.py` exists. The published 0515 command hashes
match review0626 for command-cut (`b3693e96…d11d2`) and command-pristine
(`17800a02…9b2f9`); the checker hash does not: review0626 claims
`c5afc8a5…8c128`, while the published checker is
`c5af3e45c06a8ab9c068f628178224442ef19277d7094bae2dfebd7c3988c128`.

## The seven review0626 findings

### F-D141L-001 — stale integrated tuple

`agt-F-D141l-proof-return-0515-command-cut.sh:97-112` binds App's receipt and
the live Agent/Runtime/Composition guards to Agent `8585ed9c` / tree `92a3ffdb`
and Runtime `6a011d58` / tree `ac5b8627`; `command-pristine.sh:90-105` repeats
the stale App-Agent binding and pristine-only guards. The source manifest
records the same stale integrated tuple at lines 5-8. The actual live tuple is
the one above, and the genuine App receipt 0545 independently records App
`4de54db1`, Runtime `95d98f03`, Agent `8585ed9c`, Composition `635f4de0`.
Therefore this packet cannot authenticate the current Agent/Runtime pair. App
catch-up is separately owned; no App head beyond that genuine receipt is
claimed here.

### F-D141L-002 — non-executable pristine root

`command-pristine.sh:255-273` contains `tests/v10/timelines_create.py`. A
read-only `git show 64197afa:tests/v10/timelines_create.py` fails with a missing
path; `git show 64197afa:tests/v10/test_timelines_create.py` succeeds. The
checker `check-source.py:94-95` counts regex-matching root lines only and never
resolves them in the pristine tree, so its reported 17 roots cannot prove an
executable selection.

### F-D141L-003 — caller-authorized admission is not an authenticated producer

`command-cut.sh:152-193` and `command-pristine.sh:134-165` parse a caller-named
JSON file and compare locally supplied strings and hashes. `service_id` is only
printed at the end; it is not checked against a service row or producer. There
is no check of a durable request-test/test-run record, canonical receipt schema,
authenticated request/body hash, exact command/tuple/manifest/source-manifest
owner binding, or immutable lifecycle state. The acceptance surface is thus a
hand-written JSON assertion, not the production admission producer.

### F-D141L-004 — pristine manifest/source-manifest alias

`command-pristine.sh:135` passes `$SOURCE_MANIFEST` as both the manifest and
source-manifest argument. There is no distinct `MANIFEST` input in that script.
The comparison at lines 153-154 therefore hashes one file twice and cannot
prove a production command manifest distinct from the source-manifest or bind
either to an owner.

### F-D141L-005 — launcher controls are declared, not executed for this tuple

`controls.json:38-46` records positive/poison controls as
`DEFINED_NOT_RUN_THIS_RETURN`; the positive stub and both manifests named by
`check-source.py:49-68` are not present in the published 0515 design packet.
The retained 0309 dry-control report is for Agent `28e56cac`, not the current
Agent `ecdc242e`, and its own poison result is a refusal from the stale tuple.
The current D73 launcher (`/home/user/work/agent/tools/p4-d73-pinned-launch.sh`,
sha256 `9f668e39…110cd0`) would authenticate live checkout SHA/tree/clean state
at lines 41-58, then materialize the caller manifest at lines 60-73; that
existing route was not executed by 0515. No `exit=17/call=1` positive or
`exit=1/call=0` agent-SHA-only poison result is therefore proved for ecdc242e.

### F-D141L-006 — checker is token/static-only

`check-source.py:39-47` checks Git objects, `:49-79` checks syntax/JSON/hash and
tokens, and `:81-95` checks frozen objects, token presence and a root-line count.
It does not execute either command, resolve every root, invoke request-test or
test-run, validate an adversarial receipt, run D73, inspect actual custody, or
check current normal checkout identity. The claimed checker PASS is therefore
not evidence for the controls it names. Its required positive-stub/manifests
are also physically absent from the published packet.

### F-D141L-007 — custody/lifecycle chain is open

Both scripts hash and stat files in `custody` (`cut:210-218`,
`pristine:180-188`), but `check_custody` removes every SHA line before its
comparison (`cut:220-224`, `pristine:190-194`), so content changes are not
detected. It checks existence, not non-empty/parseable raw/JUnit data, exact
owner/mode/immutable KEEP state, interpreter/runtime/service/caller linkage, or
producer-to-receipt dataflow. `chmod` failures are ignored (`cut:307-308`,
`pristine:289`); `status.txt` is written before final custody/checking
(`cut:272-284`, `pristine:238-250`), leaving `evidence_exit` stale if the late
checks fail. The required source-before/after, raw/JUnit, trace, KEEP, monitor,
body exit and final status chain is not closed.

## Additional blocking source/control defects

1. **No actual registered named-row path.** `request-test:8-15` accepts only a
   suite present in `tests/suites.conf`; no `agent-core-full` row exists (only
   `agent full` at line 10). `test-run:11-19` sources the request and resolves
   the child command solely from that registered row. The 0030 published row
   explicitly says `candidate named service row; do not add here or run from
   suites.conf` (service-row.txt:4), while 0515 `rows.txt:1-20` is metadata and
   has no executable argv. Consequently the claimed request-test → test-run →
   named-row → command path has no producer for this packet; the inline
   `admitted_dispatch` cannot repair that absence.

2. **Published review hash integrity is broken.** The exact mismatch above is
   between `agt-F-D141l-command-review-0626-source-manifest.json` and the
   published `agt-F-D141l-proof-return-0515-check-source.py`. The two command
   hashes do match, but the checker provenance does not, so the review cannot
   be treated as byte-authentic for the checker.

3. **The published checker input set is incomplete.** The checker opens
   `positive-stub.sh`, `positive.manifest`, and `poison.manifest` relative to
   its packet root, but all three exact paths
   `/home/user/timeline-hub/hub/design/agt-F-D141l-proof-return-0515-{positive-stub.sh,positive.manifest,poison.manifest}`
   are missing. This is a finite missing-input defect, not permission denial;
   no substitute was fabricated.

## Reusable production seams and applicability limits

The smallest existing seams are: ORCH `request-test` (queue record),
`test-run` (registered-row command resolution, source snapshot, heavy floor,
child trace and terminal result), `d141-validate-receipt.py:239-350`
(manager-owned fixed receipt, source head/tree and command hash), the current
D73 launcher, and the previously passing 0030 lifecycle wrapper. The latter's
`git show 0710897c…:evidence/command.sh` captured all source guards, owned
`setsid --wait` body reaping and final witnesses, but it intentionally used the
freeze-1 plain 17-root pristine path and required manager gate files. The 0309/
0318 cut route added the D73 dry controls and corrected inclusive after-body
floor, but it is tied to its own freeze-1 tuple and private evidence root.
Neither passing tuple can be copied to ecdc242e/95d98f03 or used to claim the
missing 0515 receipt/row/launcher execution. Existing seams are reusable only
after the Agent-owned repair binds authentic current inputs and the eventual
review verifies them.

No C0 contract change is implicated. The C0 v2 request still requires
`api_version`, project/timeline/base IDs, commands, label, steps, merge,
declared reads, idempotency and the source/rationale/group annotations; replies
must be authenticated accepted/merged receipts or structured conflict/invalid
responses, and dry-run has no mutation. This source admission investigation
did not submit a C0 request and proves none of those runtime outcomes.
