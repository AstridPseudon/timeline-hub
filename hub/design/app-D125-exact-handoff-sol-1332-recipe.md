# D125 exact Proof-side recipe

This is a source-only handoff. It was reconstructed from the existing D120
normal persistent-plan API and D124 tagged-plan route. It does not run in this
App worker. Proof owns the private temporary directory, venue-local receipts,
generated plan, central test requests, and returned artifacts.

## Fixed tuple and private paths

Use these exact full pins; never resolve mutable heads or a near-match:

```sh
set -eu
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
WORKER_TMPDIR="${TMPDIR:?Proof must provide its private TMPDIR}"
export D66_APP_SHA=fe3309dba4520835a685f925468bff1acdc0506f
export D66_APP_TREE=e55f0d65dca0c9f2ba3013df4cab999f314308b9
export D66_AGENT_SHA=070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2
export D66_AGENT_TREE=6056414359ae9fce08d999d54cbecf719fda33c3
export D66_RUNTIME_SHA=5e9ad1c6f74241d8771d3284fdd2ce7a214fd344
export D66_RUNTIME_TREE=de2954a0ceadb4455903d9abdfec3b773318a50f
export D66_COMPOSITION_SHA=635f4de06fda22a85fc2e4cfc764d0153a4c9f40
export D66_COMPOSITION_TREE=5ab5191a296980a0a6bcd1178ab6902d6478a148
D66_OUTPUT_DIR="$WORKER_TMPDIR/d125-full-p2/submission/full-p2"
D66_SUBMIT_PLAN_PATH="$D66_OUTPUT_DIR/p2-submit-plan.json"
umask 077
mkdir -p "$D66_OUTPUT_DIR"
```

`D66_OUTPUT_DIR` and `D66_SUBMIT_PLAN_PATH` are private Proof-owned paths.
Do not use this worker's absolute checkout paths as Proof receipts.

## Detached checkout requests and receipt verification

Run the existing Proof-local request command once for each exact full SHA:

```sh
"$ORCH/bin/request-checkout" app "$D66_APP_SHA" "D125 exact App source"
"$ORCH/bin/request-checkout" agent "$D66_AGENT_SHA" "D125 exact Agent source"
"$ORCH/bin/request-checkout" runtime "$D66_RUNTIME_SHA" "D125 exact Runtime source"
"$ORCH/bin/request-checkout" composition "$D66_COMPOSITION_SHA" "D125 exact Composition source"
```

Wait for the four full-name receipts and derive each path from its receipt;
the standard generated names are `app-pin-fe3309db`, `agt-pin-070dfc5e`,
`rt-pin-5e9ad1c6`, and `vw-pin-635f4de0`:

```sh
receipt_path() { printf '%s/queue/done/checkout-%s-%s' "$ORCH" "$1" "$2"; }
receipt_checkout() {
  sed -nE 's/^(created|exists):? +([^ ]+) .*/\2/p' "$1" | head -n1
}
APP_RECEIPT=$(receipt_path app "$D66_APP_SHA")
AGENT_RECEIPT=$(receipt_path agent "$D66_AGENT_SHA")
RUNTIME_RECEIPT=$(receipt_path runtime "$D66_RUNTIME_SHA")
COMPOSITION_RECEIPT=$(receipt_path composition "$D66_COMPOSITION_SHA")
for receipt in "$APP_RECEIPT" "$AGENT_RECEIPT" "$RUNTIME_RECEIPT" "$COMPOSITION_RECEIPT"; do
  while ! test -s "$receipt"; do sleep 1; done
done
APP_CHECKOUT=$(receipt_checkout "$APP_RECEIPT")
AGENT_CHECKOUT=$(receipt_checkout "$AGENT_RECEIPT")
RUNTIME_CHECKOUT=$(receipt_checkout "$RUNTIME_RECEIPT")
COMPOSITION_CHECKOUT=$(receipt_checkout "$COMPOSITION_RECEIPT")
test -n "$APP_CHECKOUT" && test -n "$AGENT_CHECKOUT"
test -n "$RUNTIME_CHECKOUT" && test -n "$COMPOSITION_CHECKOUT"
```

Verify full commit, tree, detached state, and clean state before using any
checkout. The receipt text itself must show the same full SHA:

```sh
verify_checkout() {
  role=$1; checkout=$2; sha=$3; tree=$4; receipt=$5
  grep -Eq "(^|[ (])$sha([ ,)]|$)" "$receipt"
  test "$(git -C "$checkout" rev-parse HEAD)" = "$sha"
  test "$(git -C "$checkout" rev-parse HEAD^{tree})" = "$tree"
  test -z "$(git -C "$checkout" symbolic-ref --quiet --short HEAD || true)"
  test -z "$(git -C "$checkout" status --porcelain --untracked-files=all)"
}
verify_checkout app "$APP_CHECKOUT" "$D66_APP_SHA" "$D66_APP_TREE" "$APP_RECEIPT"
verify_checkout agent "$AGENT_CHECKOUT" "$D66_AGENT_SHA" "$D66_AGENT_TREE" "$AGENT_RECEIPT"
verify_checkout runtime "$RUNTIME_CHECKOUT" "$D66_RUNTIME_SHA" "$D66_RUNTIME_TREE" "$RUNTIME_RECEIPT"
verify_checkout composition "$COMPOSITION_CHECKOUT" "$D66_COMPOSITION_SHA" "$D66_COMPOSITION_TREE" "$COMPOSITION_RECEIPT"
```

## Official Node 20.19.4 in Proof private TMPDIR

Do not assume the App worker's Node path or Proof's default Node 22.22.0.
Download only the official artifact into private TMPDIR, verify the exact
official digest, and unpack only under private TMPDIR:

```sh
NODE_VERSION=20.19.4
NODE_ARCHIVE="node-v${NODE_VERSION}-linux-x64.tar.xz"
NODE_URL="https://nodejs.org/dist/v${NODE_VERSION}/${NODE_ARCHIVE}"
NODE_SHA=7a488a09e2fc02fbd1bc4ae084bea8a589314f741c182fc02c5f3f07c79a29d4
NODE_TGZ="$WORKER_TMPDIR/$NODE_ARCHIVE"
curl --fail --silent --show-error --location --connect-timeout 10 --max-time 30 "$NODE_URL" -o "$NODE_TGZ"
printf '%s  %s\n' "$NODE_SHA" "$NODE_TGZ" | sha256sum -c -
NODE_ROOT="$WORKER_TMPDIR/node20"
mkdir -p "$NODE_ROOT"
tar -xJf "$NODE_TGZ" -C "$NODE_ROOT"
NODE="$NODE_ROOT/node-v${NODE_VERSION}-linux-x64/bin/node"
test "$($NODE --version)" = v20.19.4
```

The independent official source line and digest are preserved in
[checksum](app-D125-exact-handoff-sol-1332-checksum.txt). No package, lockfile, generated file, shared runtime,
shared venv, or product checkout is modified.

## Source-verified execution boundary — STOP on the stated Proof host

Frozen App fe3309 hardcodes `nodeDir` at module scope. `serviceRecipe()` emits
that absolute Node executable; `main()` also uses it for collection,
Playwright, npm and Agent launch. There is no supported Node-path env override.
The private Node above can load the controller but cannot redirect these uses.
Do not create links/files in the shared runtime, rewrite registry recipes,
patch source, set an invented env option, or use helper 181952/App 4c56/af5.
Proof's stated Node 22/no-existing-toolchain venue therefore cannot execute
this exact normal route as authorized. Report this first predicate and STOP.
The following is the exact supported route only if the required toolchain
already exists at the immutable source's path; it is not a claim it exists.
The author executed none of it.

```sh
SOURCE_NODE=/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node
if ! test -x "$SOURCE_NODE"; then
  printf '%s\n' 'STOP D125: frozen D66 source Node path unavailable' >&2
  exit 1
fi
test "$("$SOURCE_NODE" --version)" = v20.19.4
AVAILABLE_BYTES=$(df -PB1 "$WORKER_TMPDIR" | awk 'NR==2 {print $4}')
test "$AVAILABLE_BYTES" -ge 6000000000
export D66_APP_CHECKOUT="$APP_CHECKOUT"
export D66_AGENT_CHECKOUT="$AGENT_CHECKOUT"
export D66_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT"
export D66_COMPOSITION_CHECKOUT="$COMPOSITION_CHECKOUT"
export D66_SUBMIT_TARGET=app-pin-fe3309db
export D66_OUTPUT_DIR D66_SUBMIT_PLAN_PATH
export ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS=20
cd "$APP_CHECKOUT"
```

All eight full SHA/tree variables exported above are required by
`selectPinnedSources` (the frozen source has no `inputsFromEnv` export).
`D66_OUTPUT_DIR`, `D66_SUBMIT_PLAN_PATH` and `D66_SUBMIT_TARGET` are supported.
`serviceRecipe` embeds all twelve tuple fields and watchdog 20 itself; it does
not propagate private Node or controller output paths into the service rows.
Reported Proof disk is 6.3–6.5 GB, with a 6.0 GB admission floor; recheck locally.
No sourceguard exception is authorized.

### Venue-local preparation regeneration (source API, no preflight/body)

Do not copy the published preparation JSON to the durable submit path: the
source treats any existing JSON there as a resumable artifact. Use an initially
absent durable path, retain it across restart, and regenerate a separate local
preparation using the actual exported full tuple and receipt-selected paths:

```sh
"$NODE" --input-type=module - <<'JS'
import assert from 'node:assert/strict';
import { writeFileSync } from 'node:fs';
import { buildSubmitPlan, serviceRecipe, receiptCheckout } from './scripts/testing/d66-plain-stack.mjs';
const roles = ['app', 'agent', 'runtime', 'composition'];
const homes = {app:'/home/user/work/app',agent:'/home/user/work/agent',runtime:'/home/user/work/runtime',composition:'/home/user/work/composition'};
const pins = {}, checkouts = {};
for (const role of roles) {
  const prefix = `D66_${role.toUpperCase()}`;
  const head = process.env[`${prefix}_SHA`], tree = process.env[`${prefix}_TREE`];
  assert.match(head, /^[0-9a-f]{40}$/); assert.match(tree, /^[0-9a-f]{40}$/);
  checkouts[role] = process.env[`${prefix}_CHECKOUT`];
  const receipt = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/checkout-' + role + '-' + head;
  assert.equal(receiptCheckout(receipt, role, head), checkouts[role]);
  pins[role] = {checkout: homes[role], head, tree};
}
const plan = buildSubmitPlan({name:'p2',target:process.env.D66_SUBMIT_TARGET,pins,checkouts});
const recipes = {preflight:serviceRecipe({name:'p2',pins,checkouts,preflight:true}),normal:serviceRecipe({name:'p2',pins,checkouts})};
writeFileSync(process.env.D66_OUTPUT_DIR + '/D125-venue-preparation.json', JSON.stringify({status:'PREPARATION_ONLY',plan,recipes},null,2)+'\n', {mode:0o600});
JS
sha256sum "$D66_OUTPUT_DIR/D125-venue-preparation.json"
```

Hash and retain that local preparation. The frozen normal persistent API then
registers its own two service recipes and writes its real `version:1` artifact:

```sh
"$NODE" --max-old-space-size=6144 --import tsx \
  scripts/testing/d66-plain-stack.mjs p2 --submit
sha256sum "$D66_SUBMIT_PLAN_PATH"
```

This is the sole submission command. It requests one actual central source
`p2 --preflight`, waits for terminal PASS, then requests exactly one normal
full body on Proof. Do not also run a local `p2 --preflight`: that would add
another preflight. Source preflight writes **manifest.json**, at
`$ORCH/tests/<preflight.id>/d66/manifest.json` in the central snapshot, not a
file under this controller's output. Its manifest has `suite`, `mode`,
`repo_heads`, `repo_trees`, `source_checkouts`, `service_source`, `service_target`.
Normal manifest adds XML paths `d66/readiness.xml`, `d66/p2.xml`, test hashes,
readiness/original exits and service versions. Verify all tuple identities.

The exact generated persistent schema is `version:1`, `suite`, `pins` (each
`checkout/head/tree`), `checkouts`, `target`, `suites`, `recipes`, `preflight`,
`normal`. Authentic request results populate `.preflight.id/.resultDir` and
`.normal.id/.resultDir`; `.normal` is null before its request. Example 1145
has this schema. Example 1306 is BLOCKED preparation, not a successful run.
Suite names are `d73-p2-fe3309db-submit-preflight` and
`d73-p2-fe3309db-submit`. If already registered without the matching durable
plan, STOP; never choose another suite name to evade collision.

```sh
NORMAL_ID=$(jq -er '.normal.id | select(type == "string" and test("^[A-Za-z0-9_.-]+$"))' "$D66_SUBMIT_PLAN_PATH")
NORMAL_DIR=$(jq -er '.normal.resultDir' "$D66_SUBMIT_PLAN_PATH")
test "$NORMAL_DIR" = "$ORCH/tests/$NORMAL_ID"
set +e
"$ORCH/bin/wait-test" "$NORMAL_ID"
WAIT_STATUS=$?
while test "$WAIT_STATUS" -eq 124; do
  "$ORCH/bin/wait-test" "$NORMAL_ID"
  WAIT_STATUS=$?
done
set -e
sha256sum "$D66_SUBMIT_PLAN_PATH"
test "$WAIT_STATUS" -eq 0
test "$(cat "$NORMAL_DIR/status")" = pass
```

On controller timeout 180/restart, retain the same durable path and inspect it
first. If `.normal.id` exists, wait that ID only. If `.preflight.id` exists but
`.normal` is null, the same `p2 --submit` path resumes that preflight and queues
normal only after PASS. Exit 124 from wait-test always means wait the same ID.
Never use a fresh plan to retry. A crash between request acceptance and saving
its ID leaves an ambiguous window in this source: correlate the existing
service result; STOP if unresolved, rather than queueing a duplicate.
On classifier/safety/sourceguard refusal, STOP/report; never automatically
resume refusal. Retain private runtime logs under normal result
`d66/runtime-private/`, including repeated-start namespaces.

## Tour and safe handback boundary

The existing `p2` selector runs readiness first and exactly these eight
original checks from the three source specs: popup ADD; popup SWAP; parent
move; transition None single; transition None bulk; element edit; register
Asset; automatic child placement. Preserve all existing request/reply checks,
zero-old-route checks, field/opaque/order checks, reload/history checks, 5s
applied wait, default 12s seed, placement-only 14s seed, readiness waits, and
native guarded Undo. No helper activation, new Apphook, collector, probe,
native replay, or second body is authorized.

Proof may return only safe bounded fields: actual ID, result directory,
status/exit, readiness/original counts, first unmet predicate, source and
receipt hashes, generated plan hash, and SWAP tag/reason/hash/correlation.
Keep raw payload, Idempotency-Key, auth, credentials, URL, opaque IDs, stacks,
private stderr, and phase bodies private. App dispatches the sole independent
`app-D125-P2-Proof-GO-review`; Proof does not self-review or self-GO.

## Full production C0 envelope retained

Mounted gesture → durable A2 outbox → registered commitTimeline → real Agent
provider/Runtime → canonical reply → authoritative history/reload → guarded
native inverse. Request: api_version=1, project_id, timeline_id,
base_revision_id, base_publication_id, commands[schema_version,op,version,
select,args,created], label, steps[id,label,intent,tags,command_ordinals,patch,
reads?], merge=fields|atomic, reads, Idempotency-Key, dry_run, source, rationale,
group_id. Replies: accepted|merged canonical/base/landing/receipt/records/
bindings/effects/dependencies/history/undo_steps; conflict reason/head;
invalid code/path/hint/suggestedcommand; preview would_status/null receipt.
No request/reply assertions are removed. Original eight, readiness, 5s applied
wait, default12/placement14 seeds and native inverse stay exactly frozen.
