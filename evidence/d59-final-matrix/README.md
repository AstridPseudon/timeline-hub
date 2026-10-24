# D59 final matrix runner

This is private preparation for one final cut.  `commands.sh` is the production
caller: it consumes one already-captured `READY` four-repository tuple and
dispatches the venues in order.  It does not read `/home/user/work/{agent,
runtime,app,composition}` to recapture heads, request a checkout, or replace a
captured tuple.  A newer home therefore cannot invalidate a proof already bound
to the tuple.

The tuple must carry each repository SHA and tree, source and selected-checkout
paths, genuine checkout-receipt path and SHA256, checkout HEAD/tree, test
receipt hashes, the schema digest, manifest bindings, and the authentic render
environment receipt when one exists.  The checked-in template is deliberately
`PENDING`; it is not a final tuple and cannot be submitted.

It also carries `d73_source_tuple` and `d73_tuple_sha256`: the exact original
four-key D73 tuple consumed by the inherited `run-final-services.py` interface,
plus the parametric D73 manifest fields required by the existing pinned
launcher.  The D59 envelope never translates or recaptures those identities.

The inherited D84 runner and custody files live in `inherited-d84/` beside this
runner.  They are byte-copied into this durable evidence before any D59 edits;
their hashes are checked by the runner, so no predecessor worker path is a
runtime dependency.  The Agent2236 packet is preserved under `agent2236/`.

## Venues and normal commands

Every row below is one normal `request-test` command.  `--no-cache` is retained.
Each later receipt stores the exact argv, stdout, stderr, return code, and a
parsed normal `TEST <id>` when the dispatcher emits one; an absent ID is
recorded as null rather than invented.
The runtime P5 row uses the existing D84 `run-final-services.py` interface so
its 92-Python-target selector and preserved TypeScript/P5 coverage remain exact.

| id | normal route | finite prerequisite |
|---|---|---|
| app-p1 | `request-test app full-e2e-three-products --files tests/e2e/local/three-products.p1-chain.spec.ts --no-cache` | none |
| app-p2 | `request-test app full-e2e-three-products --files "tests/e2e/local/three-products.p2-tour.spec.ts tests/e2e/local/three-products.p2-elements-assets.spec.ts tests/e2e/local/three-products.p2-popup.spec.ts" --no-cache` | eight isolated P2 PASS receipts; only then this one full P2 |
| app-p3 | `request-test app full-e2e-three-products --files tests/e2e/local/three-products.spec.ts --no-cache` | App owner GO/source receipt |
| app-core | `request-test app full --no-cache` | all active core open=0/regressions=0 |
| agent-p4 | `request-test integration:agent p4-current-becfe-http-3legs --no-cache` | owner must publish the existing five-selector row; final P4 remains the separate three-original-selector handoff |
| agent-core | `request-test agent full --no-cache` | Agent core open=0/regressions=0 |
| agent-d77-render | `request-test agent m3-public13-bounded-files-gate --no-cache` | genuine installed D77 environment/receipt; source-only preparation is not render credit |
| runtime-p5 | existing D84 `run-final-services.py --source-tuple <d73_source_tuple> --tuple-sha <d73_tuple_sha256> core` | Runtime P5 14+24 preserved and final tuple READY |
| runtime-core | `request-test runtime full --no-cache` | Runtime core open=0/regressions=0 |
| composition-full | `request-test composition full --no-cache` | Composition source receipt |

The App owner-specific P1/P2/P3 names and the Agent P4 row are documented
owner seams, but the installed local `suites.conf` currently lacks the P4 row.
The runner records that exact finite missing input as `PENDING_OWNER_REGISTRATION`
and refuses submission rather than inventing a host command.  The current Agent
row is the historical five-selector 29429 evidence.  Final P4 is exactly three
original selectors (CLI/sheet, ten-note, conflict/rerun), with the parametric
launcher command and membership preserved in `agent2236/`; its aggregate test
hash must be recomputed from the absolute files in the final Agent checkout.
D77 is similarly `PENDING_AUTHENTIC_ENVIRONMENT` until its real installed
receipt is attached.

Agent core uses the active Agent2234 rehearsal (9,263 collected nodes across
408 files) when its final scope is rendered.  The Agent1755 8,817-node packet
under `agent2236/prepared-1755/` is historical preparation only and is not a
final-core receipt or scope.

Product-source changes rerun P1–P5 plus the changed repository core; a
test/harness-only change reruns only its affected gate.  The runner does not
make that classification decision or authorize a run.  All original 45-second
budgets remain in the plan.  No real body, core, full, browser, build, ZIP,
network, checkout request, or registry mutation is performed by this preparation.

## C0 wire-shape preservation

The machine-readable plan retains the C0 request/reply obligations without
creating another contract: request `api_version`, `project_id`, `timeline_id`,
exact `base_revision_id` and `base_publication_id`, ordered native/`doc.patch`
commands, `Idempotency-Key`, `label`, steps with `id`, `label`, `intent`,
`tags`, `command_ordinals`, `patch`, and `reads`, `merge` (`fields|atomic`),
request `reads`, `dry_run`, `source`, `rationale`, and `group_id`.  Accepted and
merged replies retain `{data, receipt}` with canonical closure/digest,
commands/idmap, compiler/provider, steps/dependencies, publisher,
base/previous/accepted heads, and `result=data`/authenticated event.
Conflict, invalid, and refused replies retain `code`, `path`, `hint`,
`suggested_command`, `head`, and `conflicts`; preview retains a full candidate
or null receipt.  ABI 1|2 and the D62 known gap are unchanged.

## No-body controls

Run `python3 stubcontrols.py`.  It uses a private fake `request-test` only: one
positive venue dispatch proves tuple SHA propagation and count=1; wrong SHA,
missing schema input, stale checkout identity, and a pending owner route each
refuse before dispatch, proving poison count=0.  Pending final tuples refuse
before checkout, submission, and final receipts.  It does not queue a service
request or mutate a ref.
