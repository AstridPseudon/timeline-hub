# D108 full P2 route preparation

Static source/API inspection only. No test, `--collect`, checkout, preflight,
service, browser, build, HTTP body, or suite-registry operation was run.
Runtime D111 is intentionally unresolved: the current Runtime `c91626f5...`
is not a qualified full-P2 candidate.

## Existing route and one future resolution point

The existing normal D66 API is `scripts/testing/d66-plain-stack.mjs`, suite
`p2`. It is the only full-tour selector: do not compose the eight tests from
the single-test aliases. The normal `p2` path performs the existing source
preflight, hosted build/direct harness launch, native seed, then two distinct
Playwright phases: `mounted-readiness.spec.ts` first and the eight original
tests second. The suite is `retainRuntimeLogs: true` and uses the existing
20-second phase-capture watchdog.

Known source identities for the later controller:

| role | commit | tree | status |
|---|---|---|---|
| App | `04beedcd18b8abb49502f65cd3facaafbe93db4e` | `300d186a45d3d0b96ef2ae39582f1e9b4a760e7d` | current HOME/base |
| Agent | `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` | `6056414359ae9fce08d999d54cbecf719fda33c3` | D110 already adopted |
| Runtime | unknown D111 release | unknown | current `c91626f5...` is held; do not use |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | existing source |

The later controller must resolve exactly once, in this order:

1. The qualified Runtime D111 release receipt and its normal-adoption receipt
   (full commit/tree, not a short label). No future D111 tuple is captured in
   this note.
2. One detached, clean checkout receipt for each role, with the receipt paths
   produced by the existing API: `queue/done/checkout-app-<full-app-sha>`,
   `checkout-agent-<full-agent-sha>`, `checkout-runtime-<full-runtime-sha>`,
   and `checkout-composition-<full-composition-sha>`. D66 must verify each
   receipt's path, full SHA/tree, detached state, and clean state; the App
   receipt also supplies the stable `app-pin-<8>` service target metadata.

Agent D110 `070dfc...` is already adopted; no second Agent adoption is owed.
Do not resolve or substitute Runtime `c916...` merely because it is current.

## Safe normal command template

The following is the existing `serviceRecipe({ name: 'p2', ... })` shape,
expanded only with the required source/output bindings. The controller binds
`APP_CHECKOUT`, `AGENT_CHECKOUT`, `RUNTIME_D111_CHECKOUT`, and
`COMPOSITION_CHECKOUT` from the four verified checkout receipts and chooses one
private output directory. `D66_OUTPUT_DIR` must be present before the Node
executable so native-seed stderr and both phase records are retained.

```sh
set -eu
: "${APP_CHECKOUT:?bind the App checkout receipt once}"
: "${AGENT_CHECKOUT:?bind the Agent checkout receipt once}"
: "${RUNTIME_D111_CHECKOUT:?bind the qualified D111 Runtime checkout once}"
: "${COMPOSITION_CHECKOUT:?bind the Composition checkout receipt once}"
: "${D66_OUTPUT_DIR:?use one private output directory for this body}"

cd "$APP_CHECKOUT"
env \
  D66_OUTPUT_DIR="$D66_OUTPUT_DIR" \
  D66_APP_SHA='04beedcd18b8abb49502f65cd3facaafbe93db4e' \
  D66_APP_TREE='300d186a45d3d0b96ef2ae39582f1e9b4a760e7d' \
  D66_APP_CHECKOUT="$APP_CHECKOUT" \
  D66_AGENT_SHA='070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2' \
  D66_AGENT_TREE='6056414359ae9fce08d999d54cbecf719fda33c3' \
  D66_AGENT_CHECKOUT="$AGENT_CHECKOUT" \
  D66_RUNTIME_SHA="$RUNTIME_D111_SHA" \
  D66_RUNTIME_TREE="$RUNTIME_D111_TREE" \
  D66_RUNTIME_CHECKOUT="$RUNTIME_D111_CHECKOUT" \
  D66_COMPOSITION_SHA='635f4de06fda22a85fc2e4cfc764d0153a4c9f40' \
  D66_COMPOSITION_TREE='5ab5191a296980a0a6bcd1178ab6902d6478a148' \
  D66_COMPOSITION_CHECKOUT="$COMPOSITION_CHECKOUT" \
  ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS='20' \
  '/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node' \
  --max-old-space-size=6144 --import tsx \
  scripts/testing/d66-plain-stack.mjs 'p2'
```

`RUNTIME_D111_SHA` and `RUNTIME_D111_TREE` are intentionally not assigned
here; they come from the one qualified release/adoption receipt. This is not a
new launcher or profile. The command is the existing D66 launcher and current
Node 20.19.4 path. The existing `--preflight` form is the same command with
`'p2' --preflight`; it is a source manifest operation, not a replacement for
the normal run. Do not use `--submit`: this task does not change the central
suite registry.

For `p2`, `configureRuntimeLogEnv` is called before direct-harness creation and
native seed with `D66_RUNTIME_LOG_DIR=$D66_OUTPUT_DIR/runtime-private` and
phase ordinal `1`. The original body is launched with the same private sink
and ordinal `2`; the separate readiness launch has no private sink. The
existing harness creates the private `0700` directory and `0600` bounded
phase/seed stderr files, and the existing repeated-start control distinguishes
the seed/start phase from the original phase. “HOME04beed” is the App source
identity above, not a request to change shell `HOME` to a source directory.

## Collection and original eight

The `p2` suite declares exactly these three source specs and `count: 8`:

- `tests/e2e/local/three-products.p2-popup.spec.ts`
- `tests/e2e/local/three-products.p2-tour.spec.ts`
- `tests/e2e/local/three-products.p2-elements-assets.spec.ts`

The existing source-independent list path would assert `Total: 8 tests in 3`
and list these files, but it was not run under this read-only brief. The
normal run's separate readiness source is
`tests/e2e/local/three-products.mounted-readiness.spec.ts`.

The eight original test names, in source order, are:

1. `P2 popup mounted ADD on selected child uses shared occurrence fork and A2 commit`
2. `P2 popup mounted SWAP on selected child uses authenticated old/new media selections`
3. `P2 mounted single parent move: v2 commit, exact field delta, reload and guarded Undo`
4. `P2 mounted transition None single: raw clear preserves opaque data/order and guarded Undo`
5. `P2 mounted transition None bulk: atomic raw clears preserve unknown fields/order and guarded Undo`
6. `P2 mounted element edit: real catalog apply, exact params patch, reload and guarded Undo`
7. `P2 mounted registerAsset save: real file drop, exact media/registry fields, reload and guarded Undo`
8. `P2 mounted automatic child placement: embedded shot file gesture, occurrence command, closure and guarded Undo`

The individual source SHA-256 values at App `04beedcd...` are:

| source | SHA-256 |
|---|---|
| `three-products.mounted-readiness.spec.ts` | `2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593` |
| `three-products.p2-popup.spec.ts` | `09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9` |
| `three-products.p2-tour.spec.ts` | `54ea18f3f3fa8fef2eb31cc0a05809ede76099f9f3bee9bf0511824e652a85f7` |
| `three-products.p2-elements-assets.spec.ts` | `9b8791e6e3b71155daab01440466987de406b23e2b6269dcc67872cc75c807c7` |

The original protected six values retained by the earlier route are:

```text
mounted-readiness  2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593
P1 chain           50960dd2efadc8350b8647a1f7e88a6cad2b44907bf36a7108832ee0ea9ebf17
P2 popup           09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9
P2 tour            54ea18f3f3fa8fef2eb31cc0a05809ede76099f9f3bee9bf0511824e652a85f7
P2 elements        c75baf23fa743c19c9f4bfa5822aa69c8776188436f82a9c27bbf82431c21845
P3                 93c2bf4c72ac3c91442a1a52174e36311113751ab9d8b7e0f52e4a958559a64b
```

D105a is the approved, current scoped successor for the P2 elements file:
`c75b...` → `9b8791e6...`. The other five protected values remain unchanged;
the later controller must not treat the pre-D105a elements hash as the
current source hash.

Preserve every existing `90_000` response ceiling, `240_000` worker fixture
timeout, readiness/connected waits, request/reply assertions, exact field and
opaque/order checks, zero-old-route checks, reloads, history reads, and native
guarded Undo. The gestures retain their current inputs: parent move to `5`
with the existing 12 mouse steps; transition clear on one clip and on the
two-clip selection; element `AM Burst` (`am-burst`) followed by parameter
input `12`; registerAsset's real file drop at the existing reference/hold
inputs; popup ADD/SWAP's existing authenticated file/media selections; and
the placement drop's existing `from=3`, `referenceAt=6`, `time=4.5` inputs.

## D105a and D96 fixture constraints

D105a's scoped inverse oracle is already in the current elements source. It
uses the projected canonical child identity `<occurrence-id>:<raw-clip-id>`;
reload must find exactly one projected identity and zero raw-ID fallback rows.
It rejects wrong occurrence, sibling physical owner, raw fallback, duplicate,
and byte-identical mutations. The inverse must remain RED while the projected
residue exists and turn GREEN only after that exact scoped identity is absent.
This is an oracle scope rule, not a product or Runtime wait change.

D96 forbids a global shared-seed `12→14` change. The popup helper at
`three-products.p2-popup.spec.ts:280` deliberately keeps its copied
occurrence at `on: 12`; because `occurrence.place-shared` copies `duration_ms`,
the old geometry is `[0,12)` plus `[12,24)`. The placement-only fixture is
already explicit in `three-products.p2-elements-assets.spec.ts`: its worker
seed calls `seedThreeProducts(..., 14)`, while the other seven use the normal
seed default. Do not alter the popup fixture or shared harness to make the
14-second placement setup global.

## Production caller and v2 API declaration

The production path inspected is the mounted editor save funnel:

`mounted gesture → shotTimelineDataProvider.localDocumentSave.capture`
(`shotTimelineDataProvider.ts:1016+`) → `createLocalSaveSession` durable
IndexedDB outbox (`localSaveSession.ts`) →
`RuntimeClient.commitTimeline` (`client.ts:735+`) → generated client POST
(`generated.ts:202-204`) → canonical `{data, receipt}` reply → outbox basis and
display adoption → reload/readback → guarded native Undo as another
`timeline.inverse` commit. The outbox keeps the original commands, reads,
step IDs, guards, bindings, and created IDs; only the base pair advances from
the accepted canonical reply. Rejected dependent intents are revalidated or
rolled back by the existing session path.

The exact generated transport is:

```text
POST /v1/projects/{project_id}/timelines/{timeline_id}/commit
Content-Type: application/json
Idempotency-Key: <persisted intent key>
body: JSON.stringify(CommitRequest)
```

`timeline-commit-types.ts` declares the request as `api_version`,
`project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`,
`commands`, optional `label`, `steps`, `merge`, `reads`, `dry_run`, `source`,
`rationale`, and `group_id`. Each command is the existing
`{schema_version, op, version, select, args, created, ...}` envelope. Steps
carry `id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, and
optional `reads`.

Accepted/rebased/merged replies are `{data, receipt}`. `data` carries the
canonical document/digest, `id_map`, commands, steps, dependencies/effects
through the recorded command/step structures, base/previous/accepted pairs,
versions, publisher, history metadata, and guarded-undo records. Preview uses
`status: preview`, `would_status`, and `receipt: null`. Conflicts carry the
reason/head and conflict choices; invalid/refused replies carry the existing
code, path, hint, and suggested command. The tests additionally authenticate
`receipt_id`, idempotency key, request hash, history, canonical closure, and
the `timeline.inverse` guarded publication target.

## Static inspection result

The D66 source exposes a safe `--collect` list mode, but this task explicitly
prohibited test collection/reruns, so it was not invoked. The recipe and all
selector/count claims above are from static source and the existing submission
API/tests only. No product, test, generated, pin, manifest, kit, or suite
registry file was changed.
