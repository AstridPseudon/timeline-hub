# Dependent suffix — final decision and M0 evidence

The PLAN Decisions log and Agent INBOX final dependent-suffix DECISION are
binding. The earlier `base_view: original-result` proposal is **REJECTED and
superseded in full**, including its original-result reconstruction/retention
requirements. Equal-state ABA is not a counterexample to this decision.

B, authored over unacknowledged A, remains durable UNSENT intent: original
commands, absolute target or relative delta, stable references, dependencies on
A's created IDs, and complete original expect/read/selection guards. Do not
reserve/send B's request while A is uncertain. Exact A retry retains A's original
body and key. After acknowledgement, reserve B with a fresh key and the exact
accepted HA revision/publication pair; retain B's commands and guards unchanged.
The provider verifies those claims against HA **before** recording, then rebases
the same intention over later accepted changes. A real guard mismatch is a
conflict. A rejected predecessor leaves B retained as a conflict. No new basis
DTO field, original-result reconstruction or client semantic rebase is needed.

Value-and-stable-identity equality is sufficient for this handoff. Equal-state
external ABA and same-value publications are allowed. Delete/recreate with a
new identity conflicts. This does not change accepted-publication undo: PLAN's
publication ancestry and intervening-write guards still reject ABA and A→A.

The authoritative browser/Python guard contract is
[edit-recipe.md, clip.move v1 capture](edit-recipe.md#clipmove-v1-shared-operation-and-gesture-time-capture).
Framework-generated App capture freezes raw scoped ownership, closure pins,
placement/source-window/rate, follow-relation presence and complete consumed
read/selection predicates **at gesture time**, before preview; each command
captures its preceding local result. ACK does not recapture or fill missing
guards. The server cannot recover an omitted original read from HA.
Foundation `id_map` is identity-only; reconcile accepted materialization without
rewriting suffix identities. No general remapper, fork or browser rebase is needed.

## Executable coverage

`tl/agt-m0-suffix-conformance`, based on `c71db63e`, replaces the superseded
`tests/m0_suffix` specification. The tests extract frozen R4 with `git archive`
without changing refs, then run isolated subprocesses. Source:
`origin/codex/handover-timeline-r4-20261019-candidate-sdk`
(`11caf1d9de291d76f491cf69f7942606b7471d7a`).

Real APIs exercised: `EditCommand.coerce/to_json`, generated R4 command validation,
`RuntimeCommitService._apply`, recorder plans, timing compiler, `rebase.rebase`,
and `RuntimeCommitService._inverse_history`. The schema adapter extends the
actual R4 `opcall.schema.json` with the recipe's schema version and test-only
read/selection leaves; it is not the final generated DTO artifact.

| Case | Required assertion |
| --- | --- |
| A moves to 5; B absolute to 7 / relative +2 | Both finish at 7; B retains target 7 / delta 2 and original authored read basis at 5. |
| Disjoint C | Real R4 edit survives A/B replay; unchanged B guards and stable scoped references survive. |
| Changed B read / selection membership | Conflict without publication; verify HA first, then the later head. |
| Selection changed before A creation accepts | A remains valid; B's original selection fails at HA before recording. |
| ACK, exact A retry, JSON process-data reload | Same positive/conflict outcomes; exact retries do no semantic work and create no extra publication. |
| A creates a clip consumed by B | Reserved scoped ID, dependency and B's resolved reference survive retry/reload and rebase. |
| A rejects | B remains a retained conflict, with its full original command and no replacement request. |
| Schema / semantic tampering | Missing or forged original guards, order, versions, tagged states and invalid IDs fail; client authorship cannot supply observed writes. |
| Retry identity | B receives a new key; reusing A's key or changing accepted B input under B's key fails. |
| Equal-state ABA / A→A | Dependent B succeeds; a separate real R4 inverse-history test still rejects intervening writes. |

The future-guard adapter deliberately freezes the ordered track selection used
by its fixture move picker. It derives mandatory reads and that query from the
immutable base and checks supplied claims, rather than accepting client-supplied
authority or replacing claims with freshly sampled values. Schema validity alone
is insufficient. The wire cannot attest what a malicious client previously saw;
the server proves consistency with the submitted accepted basis, and the client
outbox is responsible for retaining its original authoring record.

## Verification and limits

Commands from `/home/user/work/wt/agt-m0-suffix-conformance`:

```bash
PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/m0_suffix
# 35 passed in 675.05s (0:11:15), no warnings or skips.
/home/user/work/venv-agent/bin/ruff check --no-cache --config 'include=["tests/m0_suffix/**/*.py"]' tests/m0_suffix
# All checks passed; explicit inclusion runs repo lint rules on these tests.
git diff --check
# Exit 0.
```

Focused guard/basis/inverse verification also passed:
`PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/m0_suffix -x -k 'basis_conflict or guards or inverse_history'`
— **5 passed, 30 deselected in 79.20s**. Initial development probes found fixture
and adapter errors; these were corrected. An initial matrix attempt was stopped
after its new disjoint fixture used an undeclared plate parameter; the corrected
fixture uses declared `zoom`, and the final complete run above passed.

No dependencies were installed. Product code and other design files were not
modified. Full Agent `make check`/pytest lanes/editing_conformance, Runtime suites,
App/browser journeys and renderer tests are not run for this isolated M0 task.

Publication/idempotency storage and the file-backed JSON outbox are reduced
protocol models. Reload discards Python objects and reconstructs from JSON;
it does **not** prove Runtime database durability, atomic crash recovery, browser
restart, tab fencing, real HTTP authority, concurrent head CAS, receipt retention
or generated-client compatibility. Structural C fixtures stand in for another
validated writer; they do not prove structural command admission. The real
R4 runner does validate/compile the A/B and disjoint commands. These tests prove
the bounded recipe experiment, not the M1 production journey.

Concrete M1 gaps:

1. Preserve relative intent: R4 normalizes `clip.nudge` to absolute `clip.on`.
   The adapter retains the original delta plus R4 guards; production must retain
   the declared relative operation/read basis, including fixed `at` when no
   `intent.on` expression exists. Preserve scoped selectors too:
   R4's record may retain a local selector alongside its scoped resolved ID.
2. Implement the recipe's shared Python/generated-App capture contract and verify
   ORIGINAL claims at HA before recording (legacy paths normalize once at ingress).
   Test sequential commands and dependent gestures through the **real App command
   service/drag capture**, not a port of this fixture-specific guard adapter or
   its all-tracks picker policy. Cover occurrence/source revision/window/rate and
   selection changes, fixed-start clears, supported/refused maps, and disjoint
   rebase. M1 wire `clip.move` stays absolute/fixed/non-ripple; the relative probe
   above is characterization, not permission to widen that schema. Allocate
   created IDs early enough to capture destination/occurrence guards on the
   original authoring state: R4's initial add record can omit guards supplied
   only during replay. Derived compiler consequences may change at the new
   head; they are not refreshed original authored guards.
3. Implement App durable UNSENT dependencies and atomic ACK→new B reservation,
   original-byte/key retries, ID retention, rejection/conflict retention and tab
   ownership. Test actual lost ACK and browser/process restart through `/v1`.
4. Implement Runtime's accepted publication pairs, atomic CAS/history/receipt
   storage and exact retry retention. Carry the original verified plan across
   head races. No reconstruction of a predecessor's proposed result is required.
5. Promote these cases into main semantic/atomic acceptance suites and App's
   three-products journey; preserve accepted-inverse ancestry/write checks and
   prove renderer-independent save separately. Prove one track-create/dependent
   inverse through the same generic framework (author supplies schema, handler,
   intent and fixtures; framework supplies metadata); do not claim generality
   from structural C stand-ins. Derive prepared commands from authoritative
   Runtime records and test replay/undo/compile after replacing a consumed
   transcript/config Document using Runtime-retained exact content, without
   latest reads or producer execution. No M2 registry implementation in M0.

Manager review 2026-10-19T18:33Z: reviewed committed b82dba0c source (real R4 APIs + explicit protocol adapters), lint/diff checks and 35-case result. Independently reran relative/reload/disjoint and changed-original-basis cases with a private basetemp: **2 passed in 46.71s**. Initial review rerun collided with the worker's broad pytest temporary cleanup and produced two import failures; the isolated rerun resolves that environment artifact, not a semantic change. Future runs/cleanup must use worker-owned basetemp paths only, never glob shared pytest roots. The branch remains M0 evidence-only and is not merged into the product suite.
