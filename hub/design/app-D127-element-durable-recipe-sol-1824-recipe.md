# D127 current source recipe: one normal p2-element submit

READY_SOURCE; independent recipe review PENDING; execution NOTRUN. This is a NEW
recipe made from current committed source and real queue receipts. The helper is
a NEW immutable present-source copy from Runtime e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9:tests/helpers/p2_commit_phase_capture.py,
blob 6984ac1da77f1b499703cfac45d27149eddcbdae, SHA256 4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e. No lost 1809/1818 artifact or historical
1731 raw-capture bytes are claimed recovered. Historical failed recipes stay as-is.

The four exact product commits, trees, detached checkout receipts (including exact
receipt text and hashes), and App target metadata are in source-custody.json.
Runtime ab1e4f6141987706132916e2da16477f5a019464 is the product pin; e319fdbd is
helper-source-only. The helper activation path is the persistent private file
above, never the mutable Runtime home or inherited worktree evidence.

## Reviewable future controller command (NOT executed here)

After independent review and manager dispatch with genuine 5,200,000,000-byte
admission, run this block ONCE through the existing D66 controller. D89c measures
admission once at controller dispatch; same-body dependency prep does not recheck
that floor. Keep one heavy body at a time and the ongoing 4,000,000,000-byte stop
line. No body authorization or admission is claimed by this preparation.

```sh
set -eu
umask 077
ORCH='/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch'
WORKER='/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-element-durable-recipe-sol-1824'
APP_SOURCE_ROOT='/home/user/work/app'
NODE='/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node'
HELPER='/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-element-durable-recipe-sol-1824/evidence/p2_commit_phase_capture.py'
export D66_OUTPUT_DIR='/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-element-durable-recipe-sol-1824/submission/p2-element'
export D66_SUBMIT_PLAN_PATH='/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-element-durable-recipe-sol-1824/submission/p2-element/p2-element-submit-plan.json'
export D66_SUBMIT_TARGET='app-pin-d5a1d1ab'
export D66_CHECKOUT_ROOT='/home/user/work/wt'
export D66_APP_SHA='d5a1d1ab6550187e377fd7387d300102b8b82ece'
export D66_APP_TREE='7be73e2cbbcf89d627bf7b9da940b4ce17968c20'
export D66_APP_CHECKOUT='/home/user/work/wt/app-pin-d5a1d1ab'
export D66_AGENT_SHA='070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2'
export D66_AGENT_TREE='6056414359ae9fce08d999d54cbecf719fda33c3'
export D66_AGENT_CHECKOUT='/home/user/work/wt/agt-pin-070dfc5e'
export D66_RUNTIME_SHA='ab1e4f6141987706132916e2da16477f5a019464'
export D66_RUNTIME_TREE='7d8e77b2f5a4af79305c9212ce5174d3ea9fd657'
export D66_RUNTIME_CHECKOUT='/home/user/work/wt/rt-pin-ab1e4f61'
export D66_COMPOSITION_SHA='635f4de06fda22a85fc2e4cfc764d0153a4c9f40'
export D66_COMPOSITION_TREE='5ab5191a296980a0a6bcd1178ab6902d6478a148'
export D66_COMPOSITION_CHECKOUT='/home/user/work/wt/vw-pin-635f4de0'
export D66_P2_COMMIT_PHASE_CAPTURE_HELPER="$HELPER"
export D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256='4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e'
export ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS='2'
export ASTRID_PYTHON='/home/user/work/venv-agent/bin/python'
export ASTRID_RUNTIME_PYTHON='/home/user/work/venv-runtime/bin/python'
cd "$APP_SOURCE_ROOT"
test "$(git rev-parse HEAD)" = "$D66_APP_SHA"
test "$(git rev-parse 'HEAD^{tree}')" = "$D66_APP_TREE"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
test "$("$NODE" --version)" = 'v20.19.4'
test -f "$HELPER"
test ! -L "$HELPER"
test "$(stat -c %a "$HELPER")" = '600'
test "$(sha256sum "$HELPER" | cut -d ' ' -f 1)" = "$D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256"
test "$(realpath "$APP_SOURCE_ROOT/node_modules")" = '/home/user/work/app/node_modules'
test "$(realpath "$APP_SOURCE_ROOT/node_modules/tsx/dist/loader.mjs")" = '/home/user/work/app/node_modules/tsx/dist/loader.mjs'
test "$("$NODE" --input-type=module -e 'console.log(import.meta.resolve("tsx"))')" = 'file:///home/user/work/app/node_modules/tsx/dist/loader.mjs'
"$NODE" --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2-element --submit
```

The launcher root is the CURRENT clean normal App d5a1 root, with explicit
commit/tree/clean checks. This is necessary because the inherited 1818 worker
branch actually has commit d8c0ce8be5c2fc317293dc5610fa6359c1131332/tree
3f5e08c818ec7fd15b43093fc7ac98f96a84eaaa, containing three tracked evidence
additions versus the product tree. It is not equivalent to product tree 7be73e.
Those inherited files were left untouched and are not inputs to this recipe.
If the normal App moves, STOP for manager instructions; do not relabel the
tuple, use an unchanged-tree exception, or launch from the contaminated branch.
The selected service source remains the official detached app-pin-d5a1d1ab.

## Normal dependency reuse and source custody

Retain the actual 1407/1440 normal dependency reuse: the controller launch root
already resolves node_modules to /home/user/work/app/node_modules and tsx to
file:///home/user/work/app/node_modules/tsx/dist/loader.mjs. The detached App
checkout currently has no node_modules attachment; this is a FUTURE preparation
requirement, not a current tsx failure. The existing central bin/test-run attaches
the service snapshot's ignored node_modules to the target's existing install or
falls back to /home/user/work/app/node_modules. It needs no package installation,
profile acquisition, shared graph write or manual registry workaround. Record
the actual service snapshot realpath and tsx resolution before the body, as
1407/1440 did. Proof's missing-tsx event remains historical. No attachment was
created here and no shared dependency was modified. The fixed existing Node is
v20.19.4 (binary SHA256 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490).
The normal shared Python dependency interpreters are selected explicitly above;
the D66 service source uses these same defaults and overlays genuine exact
Agent/Runtime source roots. Retained 1738 origins are cited separately from new
static origin-file hashes; no imports or bootstrap were rerun here.

## Exact selector and original lifecycle

Existing selector: p2-element; file:
tests/e2e/local/three-products.p2-elements-assets.spec.ts; count: 1; exact grep:
`P2 mounted element edit: real catalog apply, exact params patch, reload and guarded Undo$`.
The entire original body is unchanged: mount/seed, native pre-history and canonical
closure, AM Burst apply, accepted v2 doc.patch/list.insert, exact parent isolation,
authoritative canonical/history, params.bob=12 with one params patch, canonical and
history assertions, reload, guarded native Undo of params, reload, guarded native
Undo of apply, reload to absence, and zero legacy-route assertions. The original
5-second expect wait is unchanged. There is no new selector, shortened body,
timeout change, source guard exception, product pin/adoption or semantic design.

The production caller remains mounted editor -> persisted outbox -> registered
commitTimeline -> genuine Agent/Runtime. Full v2 request: api_version=1,
project_id, timeline_id, base_revision_id, base_publication_id,
commands[{schema_version,op,version,select,args,created?}], label,
steps[{id,label,intent,tags,command_ordinals,patch,reads?}], merge=fields|atomic,
reads, Idempotency-Key, dry_run, source, rationale, group_id. Accepted/merged
results retain canonical/base/landing/merge_mode/receipt/records/bindings/effects/
dependencies/history/undo_steps; conflict retains reason/head; invalid retains
code/path/hint/suggested_command; preview has would_status and null receipt.
Authority, privacy, previous values, ABA, no-write refusals and undo guards remain.

## Fixed durable destinations and exact normal API behavior

Controller output root: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-element-durable-recipe-sol-1824/submission/p2-element`.
Generated authentic plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-element-durable-recipe-sol-1824/submission/p2-element/p2-element-submit-plan.json`.
These are future private outputs; neither directory nor plan was fabricated here.
Use umask 077; directories 0700, private helper/captures 0600. Keep this evidence
directory 0700 and the exact helper 0600 locally. Manager publishes safe recipe
and JSON manifests only, never the helper or raw payload/stack bytes.

D66 --submit requests/waits for all four official checkout receipts, validates
the exact detached sources and App target metadata, generates normal API recipes,
registers its two rows through its existing API, stores the version-1 plan,
submits source preflight, waits for actual PASS, then submits ONE p2-element body.
Generated suite names are d73-p2-element-d5a1d1ab-submit-preflight and
d73-p2-element-d5a1d1ab-submit. No manual registry edits, extra flags or invented
environment names. Watchdog 2 seconds is generated by serviceRecipe for this
element-only route (20 seconds belongs to full p2, which is held).

The controller D66_OUTPUT_DIR fixes the plan root; it does NOT override the
central runner's service output root. Actual service outputs are durably fixed
by bin/test-run to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/<authentic-id>/d66` for each generated ID, with
manifest.json, runtime-private/, readiness.xml, p2-element.xml, and Playwright
stage outputs. The private sink is inside runtime-private/; subsequent launches
use the existing random launch directory and -2 suffix to preserve isolation.
IDs, namespaces and private launch directories cannot honestly be preassigned.
Use the generated plan's preflight.resultDir and normal.resultDir as authority;
retain exact plan SHA, both IDs, source manifests, JUnit and private captures.
The existing harness enforces a private child of TMPDIR for Runtime logs. At
future execution confirm that the service output location meets that existing
check; never point it at an invented external sink or weaken containment.

If the authentic plan exists, continue the SAME plan/IDs through the controller's
existing resume logic. Once normal is present it prints those IDs and does not
enqueue again. Wait the SAME normal ID with the existing wait-test; exit 124 is
still queued/running, so wait again, never resubmit or change suffix/tuple.
Preflight/setup failure remains zero-body. Do not put preparation JSON at the
generated-plan path, fabricate a service ID, or copy an old successful plan.

## Existing review evidence and honest limits

1630 independently passed exact keysets, privacy, bounds, loss/share/denominator
checks and bootstrap controls, but its OVERALL verdict is FAIL for lifecycle
cross-field validation. Keep that FAIL. 1723 independently SOURCE PASSed the
corrected lifecycle validator against exact helper SHA 4ee0424b..., including
16 flags, 128 phase shapes, 16 retention pairs and 53 generated summaries; its
positive controls were PARTIAL (D78 PASS; P2 bootstrap setup shortfall), integration
NOTRUN. 1738 retains the subsequent 1731 observer bootstrap TAP/origin PASS:
exit 0, 1 passed, 4 skipped, 0 failed. 1731 raw selector log, helper copy and JSONL
capture remain absent. Its event count, mode, capture hash, phase/lifecycle and
privacy results are retained-log assertions, not recomputed current raw custody.
Exact source/reference hashes and recorded module origins are in source-custody.json.

Historical 10721 element request 3 remains pending_at_stop, key SHA
69c6463f169cffb79e62788ca6d42b02ebeb00aaf6a4f72520a989b20312faf4,
352 samples/3 lost, provider/response/wall denominator UNKNOWN. Do not substitute
request 2, borrow native 1.75s, infer CPU share from frame counts, or call a
dominant cost from these historical facts. A later genuine profile must correlate
the same key SHA, method/path, capture namespace, PID/birth and request ordinal;
separate arrival/dispatch/lock/handler/response only where supported. Preserve
completed/raised/returned_without_response/pending_at_stop, loss/truncation,
observer overhead and privacy state. Missing boundaries/denominators stay UNKNOWN.
Only bounded safe inclusive/leaf aggregates may be published; raw keys, bodies,
headers, URLs, credentials, exception text, locals and raw stack blobs stay private.

D130 SWAP/WAL/recovery/full-tour absolute HOLD remains. This existing element-only
route is unrelated. No held work, retry, rollback, machine transfer or alternate
route is authorized. This worker performed source/syntax/hash/JSON/receipt/origin
file checks only: no preflight, submit, request-test, pytest, vitest, tsc, lint,
browser/native/backend, collector/sampler, profile/build or repeated D78/23.
Next: independent review of these persistent bytes; body controller only after
that review and a later genuine 5.2 GB admission under D89c/4.0 GB ongoing stop.
