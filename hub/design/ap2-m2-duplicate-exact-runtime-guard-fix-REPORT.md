# AP2 M2 duplicate exact Runtime guard fix

## Outcome

The duplicate actual gate remains **unqualified and blocked by invalid source
environment**. I did not submit a fresh central browser request: the required
source preflight fails before queueing because the authoritative Runtime
checkout has a ref spelling the required SHA but does not contain that commit
object. The old queued result is therefore not a product result.

Candidate App source is the committed deletion candidate:

- App commit `4006b673b3edaef2db2df8ade2012d644319df7e`
- App tree `dcc0e371ed4aa3a4161ce3a4051a6e74c4e49f85`
- Agent commit `8130a401bf44a518d5a40ae274d398b8c560be55`
- Agent tree `236c3e57e0265c52b81ba8085de3193026176bff`
- Required Runtime commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a2`
- Required Runtime tree `7ab412cc4bcbe517efcfa806e092336390312e18`
- Composition graph: package `0.0.13`, artifact SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`

The App candidate includes the reviewed readiness fix
`b77ccaf2dbf2da85d7ba5828e5114627325cdea6` (tree
`74130f681f6b0c87a7c61cb33d4ae6a092c03046`) as an ancestor. No readiness fix
was overlaid or changed here.

## Guard repair

The private runner handoff is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-duplicate-exact-runtime-guard-fix/run-central-duplicate-repaired.sh`

It makes the following checks fail-fast before build/browser work:

- exact commit object with `git rev-parse --verify SHA^{commit}`;
- exact commit tree and clean source status for Agent and Runtime;
- absolute executable Python, Node/npm, and public13 Composition package/bin;
- private Agent/Runtime checkouts only, with exact private HEAD/tree/status;
- frozen source imports through the private `PYTHONPATH`;
- private node graph and per-run caches; shared node_modules is only unlinked
  at the snapshot symlink and never modified;
- cleanup of the one per-run root on exit.

This corrects the prior guard weakness where `git rev-parse SHA` could echo an
unknown SHA and the runner proceeded toward a checkout. It also avoids the
old `git checkout --detach <sha> <path>` failure by resetting the private clone
to the already verified exact commit.

## Preflight evidence

Command:

```sh
SOURCEGUARD_ONLY=1 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-duplicate-exact-runtime-guard-fix/run-central-duplicate-repaired.sh /home/user/work/wt/ap2-m2-duplicate-exact-runtime-guard-fix
```

Result: exit 1, before private checkout, build, browser, Runtime door, or
queue submission:

```text
source guard: missing commit object 2c4ac180c2220bdad966bc01e95ad230e99ce26a2 in /home/user/banodoco/banodoco-workspace-runtime
```

Direct corroboration: the ref
`refs/remotes/hub/timeline/runtime/tl/rt-m2-pin-2c4ac180` prints the required
SHA with `git show-ref -s`, but
`git rev-parse --verify '2c4ac180c2220bdad966bc01e95ad230e99ce26a2^{commit}'`
exits 128 (`Needed a single revision`), and the exact tree read exits 128.
The integration checkout has the same missing object. This is an environment
object-availability failure, not permission to substitute Runtime `26a2`, the
moving integration head, or another pin.

Other read-only checks passed before that Runtime guard:

- App candidate clean, exact commit/tree above;
- Agent exact commit/tree above and clean;
- `/home/user/work/venv-app2-native/bin/python` exists and is Python 3.12.3;
- locked Composition graph reports `0.0.13` and its public13 artifact hash is
  the exact value above.

The historical central IDs are invalid environment only:

- `ap2-m2-duplicate-final-actual-gate-e2e-m2-duplicate-three-products-1020181911-32716` — exit 128 before build/browser because the runner used the malformed Runtime checkout command;
- `ap2-m2-duplicate-final-actual-gate-e2e-m2-duplicate-three-products-1020182334-29416` — exit 128 before build/browser because the Runtime object was unavailable; already terminal/claimed and not a product claim.

No new test ID exists because the required sourceguard did not pass. The
required UI gesture, lost ACK, disjoint Agent edit, reload/restart, exact
retry, opaque preservation, zero legacy traffic, and guarded undo therefore
remain unrun in this task.

## Required next step

Restore or provide the exact Runtime commit object/tree in the authoritative
read-only source, and provide the approved Python executable(s) if central
execution still requires `/home/user/work/venv-agent/bin/python` and
`/home/user/work/venv-runtime/bin/python`. Re-run the complete sourceguard
first; only after it passes should the manager submit exactly one fresh
`--no-cache e2e-m2-duplicate-three-products` request on App `4006b673b` using
the repaired runner. Do not mark the duplicate deletion ledger row `DELETED`
until that central run passes.
