# Independent review: native retained frame fixture port

## Decision

**APPROVE owner port** for App commit `dba11c8432cee8df6e8bced4eae4d82e79f2b652` on
`tl/vw-m3-frame-native-retained-fixture-port` (parent
`b1ef4b9b910ba72375c34cf319692f90d22edc25`, tree
`79fca36dcc07d83d457bc2db5f822cad28054d71`). No source or guard was lost in
the port. This approves the owner-port seam and its native-fixture evidence;
it does not approve a browser/render parity or Player Gate 6 claim.

## Exact source review

The exact commit changes only these five App test-infrastructure files:

- `tests/e2e/local/support/harness.ts`
- `tests/e2e/timeline/viewing-parity/fixture.ts`
- `tests/e2e/timeline/viewing-parity/harness.ts`
- `tests/e2e/timeline/viewing-parity/native-fixture-helper.py`
- `tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts`

The diff is 358 insertions and 11 deletions. `DirectHarness.start()` keeps its
default seed behavior and adds only an opt-in `seed: false` plus a
`beforeRuntimeStart` callback. Only the viewing-parity harness opts into those
options; the normal M1 path remains unchanged. The existing fallback fixture
and normal four-case render/download consumers are retained. The original
three-media fixture is preserved: generated 64x48 gradient image, the marked
640x360/30fps 45-frame VP8 WebM, and 44.1 kHz stereo WAV with the existing
audio placement/fades. The output resolution remains parameterized, including
explicit 1920x1080 native-profile runs.

The private helper uses `RuntimeService` on the harness-created inactive realm
to create the project/timeline and ingest all three media objects with expected
SHA-256 digests. It builds the complete parent/shot/internal closure and
dependency manifest, then calls the existing `TimelineCommitStore` closure
validator and persister only inside `service.store._mutex` and
`service.store._transaction()`. It verifies closure readback and that the
empty head pair is unchanged. It does not write a head, history/publication,
command, certificate, capture reference, or direct SQL of its own.

After Runtime startup, the fixture adopts that closure through the ordinary
authenticated HTTP `/v1/projects/.../timelines/.../commit` route with
`timeline.restore`, and asserts the canonical document, head pair, closure,
manifest media identity, and fetched media byte hashes. The fixture-specific
integration test also asserts no legacy `/composition-revisions` request and
that a forged `/v1/tasks` request leaves project objects unchanged.

Runtime source inspection confirms `_validate_closure` checks the complete
sorted shot/internal/media manifest, payload media membership, CAS bytes and
digests; `_persist_closure` writes the closure rows and dependencies without
installing the head. Media ingest uses the native CAS publication path and
project-object association. The source therefore satisfies the requested
native-store/transaction/CAS/manifest/byte-identity constraints.

## Evidence and attribution limits

The saved central result is:

`integration-viewing-native-retained-fixture`: **1 pass, 0 fail**, exact App
tree `79fca36dcc07d83d457bc2db5f822cad28054d71`.

Its recorded command/env is:

```text
env ASTRID_CHECKOUT=/home/user/work/agent \
    ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
    ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
    ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
    node --import tsx --test tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts
```

The central result records checkout paths, but not Git revisions/tree hashes
for Agent or Runtime. The available checkout history shows Runtime
`7f6dd8920e1ceec41b137358df5e7fecc304888d` (13:58:57Z) and Agent
`8e3107853d17453758a933d1f47215cc1c002660` (13:42:35Z) before the central
result at 14:00:46Z. This is useful corroboration, not literal run-time
revision capture. Do not relabel this central PASS as the older `2c4ac180...`
/ `d8749a9c...` witness.

The older recovered witness is separately recorded in
`handoff-vw-m3-frame-native-retained-fixture-port-COMMAND.md`: it archives
Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` and Agent
`d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, and ran a normal native
`RuntimeService` direct-method probe. It reports:

- restore, restart, exact retry, byte-identical closure/head/integrity: PASS;
- saved positive capture ref
  `sha256:bac1004db17ee73de4d7a6ff437944bcc7e7b7666ecd4418d88ddf6fde429a21`:
  PASS;
- forged config, registry, digest, and missing-media captures: all refused
  before object/CAS changes: PASS.

That witness is not an HTTP-scope proof: its restore and capture calls use the
native `RuntimeService` directly. The central test is the evidence for the
HTTP `/v1` restore, but its Agent/Runtime revisions are not frozen in the
result. This distinction is intentional.

## Tests

Saved source-worker evidence:

- `npx eslint tests/e2e/local/support/harness.ts tests/e2e/timeline/viewing-parity/fixture.ts tests/e2e/timeline/viewing-parity/harness.ts tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts --report-unused-disable-directives --max-warnings 0`: **PASS**.
- `node --import tsx --test tests/e2e/timeline/viewing-parity/harness.test.ts tests/e2e/timeline/viewing-parity/media.test.ts tests/e2e/timeline/viewing-parity/canvas.test.ts tests/e2e/timeline/viewing-parity/authority.test.ts tests/e2e/timeline/viewing-parity/admission.test.ts`: **5 PASS**.
- Central named suite above: **1 PASS**, no browser or renderer.

I did not rerun browser, render, localhost, full, or blind central tests. No
Composition files were modified by this review.

## Recommended next step

Before treating the native fixture as a fully attributed cross-repository
qualification, run one manager-approved, no-browser named integration proof
with the exact App tree above and explicitly frozen Agent/Runtime paths plus
literal revision/tree evidence in the result. Keep the older `2c4`/`d874`
direct-service capture witness labeled as such. Browser/render four-case
qualification remains a separate pending App/Agent capability pair.
