# Runtime current production tuple

**PUBLISHED — 2026-10-20T11:28:51Z — Runtime manager**

The reviewed generated-client producer is **2c4ac180c2220bdad966bc01e95ad230e99ce26a**, tree **7ab412cc4bcbe517efcfa806e092336390312e18**. This is the exact tree independently approved in [runtime-release-s2-final-review.md](runtime-release-s2-final-review.md) and tested by the five final lanes below. Agent and App can now make their ONE normal coordinated pin move to this SHA and qualify their consumers. This publication identifies source and generated artifacts; it does not claim consumer activation, an external package-registry publication, or complete project gates.

## Current compatible server patch

At 2026-10-20T11:55:55Z, Runtime integration is **a51267ec3dd94ea465a3161e3b4d8fbcd061009e**, tree **964485ff5bd50cad835f30de95193e658d6cc46e**. Relative to the published client producer2c4, compatible capture authority and retained-text internal presence/custody plus their tests changed. Exact generated artifacts, views signatures and digest are unchanged. Owner11:54 directed retained-text merge a51267e; it restores clear/inverse of authenticated legacy text/plain while NEW first use stays strict. Native public text command qualification is separate. The server patch contains independently approved scoped capture authority and claim-identity validation; artifact manifest, all generated clients and the wire/schema digest remain byte-identical. **Keep the consumer source_commit at2c4ac180; no second client pin is required.** This explicitly distinguishes a compatible server patch from the immutable artifact producer; no new artifact version is being implied.

The capture unit passed frozen141+25+41+9 and actual whole-current Agent cf7448/c8a5e0cb141+25 on exact branch0a04782e before merge; post-merge focused gates are in flight. Four RenderRequest propagation and three SDK early-guard requirements remain OPEN, verifier retained; no complete capture/export or Gate1/7 claim. See runtime-capture-s2-current.md, runtime-capture-actual-current-pair.md and runtime-capture-integrated-gates.md when complete. The intervening57d0f32 merge adds only independently approved media-fence tests.

## Exact release identity

| Field | Value |
|---|---|
| Generated-client producer SHA | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` |
| Client producer tree | `7ab412cc4bcbe517efcfa806e092336390312e18` |
| Reviewed source commit | `f7081c14efd9a5b834987e7a1e2abf597b66313b`, merged without any tree change |
| Stable producer checkout | `/home/user/work/wt/rt-m2-pin-2c4ac180` (KEEP retained, HEAD equals source SHA) |
| Protocol | `workspace.v1` |
| CONTRACT_VERSION / both generated clients | `0.2.13` |
| SCHEMA_DIGEST | `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4` |
| Artifact version | `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56` |
| Artifact count | 75, including handwritten `operation-handle.ts` |
| Artifact manifest file SHA256 | `129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497` |
| COMPONENT_MANIFEST_SHA256 | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| Frozen Agent schema source | `26ef2bbb31b4892fdd7c15ee5b20700bd40cb933` (S2) |
| Raw command-schema SHA256 | `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef` |
| Command definitions / operations | 48 / 22 |
| HTTP operation IDs | 133 unique: 52 GET, 1 HEAD, 72 POST, 5 PATCH, 2 PUT, 1 DELETE |

S1 `0a0ac7baaa74e15485b10bcbaa80eda1afe48c00` stays immutable history. S2 changes only optional existing `DocumentPin` `schema_source` and description on `ClipSetElementArgs`. Five full historical compatibility floors and all 99 old DTO names remain; one gains optional `consumed`, 19 names are added. DTO/root exports are independently generated; the existing HTTP TypeScript generator's fixed-point boundary is documented honestly in the review.

Supported operations: `clip.add`, `clip.move`, `clip.set`, `clip.set-params`, `clip.set-element`, `clip.trim`, `clip.split`, `clip.delete`, `track.create`, `track.set`, `occurrence.add-media`, `occurrence.swap-media`, `occurrence.duplicate`, `occurrence.delete`, `placement.move`, `placement.create`, `placement.unplace`, `shot.pool`, `shot.set`, `producer.guard`, `timeline.inverse`, `timeline.restore`.

## Safety and wire behavior

F1 restored-publication occupied shot destinations and F2 hidden legacy-document shell adoption are refused atomically. Current main `29d0954` worker credential isolation, advisory render admission and disk estimate are preserved, as is the reviewed producer normalized-record comparison. Exact accepted replay remains ahead of live producer/selection checks. Existing M1 closure, guard, restore, opaque-value and occupied-slot behavior remains.

Four verified reads share one implementation family, with unchanged separate wire shapes: `getProjectMediaSelection`, `getProjectVerifiedMedia`, `getProjectVerifiedDocumentObject`, `getProjectVerifiedDocument`. Retained exact declaration/object inputs are scoped and custody checked. No new endpoint was added by this release.

Persisted `POST .../timelines/{timeline_id}/views` now requires **projects:write and an explicit Idempotency-Key**. The response remains plain. Identical retries recover the original artifact after head advance/restart within the existing replay window; changed payload under the key refuses. `inspect` remains a read requiring no key. Browser-door `/views` remains denied.

Generated signatures:

```text
Python: create_timeline_view(project_id, timeline_id, options=None, *, idempotency_key)
TypeScript: createTimelineView(projectId, timelineId, options, idempotencyKey)
```

Agent must compose caller port `0cfdddd5b85d5a32e5319365e64cb58293381490` or its reviewed descendant with its official pin: remove create-view from read classification, forward stable keys and request write authority. App's reviewed inventory has no production persisted-view caller; it imports the official generated client and matching lock and runs its typecheck. Consumer live qualification is still pending and belongs to each manager.

The connector fixes endpoint/client/credential for negotiation and dispatch, validates and privately captures authenticated identity before exposing mutable public handshake data, retires before switch/dispose, and fences transport after awaits. Credentials never follow redirects or cookies. Direct owned transport is supported; delayed rediscovery wrappers and hosted/absolute-door activation are not. App's separately agreed same-origin proxy handle stays inactive until actual outbox/receipt/restart proof.

The restored legacy composition-revisions route remains until BOTH App D01 and Agent whole-candidate consumers migrate. Do not retire it early. F3/capture basis, parent/init/text/word schema successors and native text-clear are NOT hidden additions to this tuple.

## Exact passing evidence

All five candidate service snapshots below equal the merged tree `7ab412cc4bcbe517efcfa806e092336390312e18`; no stale-tree result is relabeled.

| TestID | Result |
|---|---|
| `rt-m2-release-s2-final-compose-targeted-1020110503-8618` | 800 passed, 1 deselected, 1 unchanged strict text-clear xfail; exit0 |
| `rt-m2-release-s2-final-compose-ts-client-check-1020110503-30973` | Build, public API compile, 61 passed; exit0 |
| `rt-m2-release-s2-final-compose-commit-integration-1020110503-17965` | 9 passed; exit0 |
| `rt-m2-release-s2-final-compose-occupancy-integration-1020110503-17107` | 1 passed, 17 deselected; exit0 |
| `rt-m2-release-s2-final-compose-producer-agent-s2-integration-1020110503-5266` | Original 5 actual frozen S2 producer cases passed with --runxfail; exit0 |

The targeted lane includes normal generation/check, artifact manifest, conformance/client parity and source compatibility checks. Independent review recalculated every artifact hash and audited the actual frozen Agent archive. Producer tests exercise original Node numeric forwarding, preview, acceptance, restart/exact retry, one-shot, undo and immutable-artifact tampering; no absent-provider or private-schema substitute.

Post-merge integration checks on the same tree: `runtime-commit-integration-1020112501-17354` **9 passed**, `runtime-ts-client-check-1020112501-16056` **PASS**. Full integration request `runtime-full-restore-integration-1020112501-27435` is **QUEUED**. The service recomputes integration HEAD while queued and freezes its source only when it STARTS; it is not an immutable2c4 snapshot yet. Its actual final `snap`/tree will be recorded with the result; no full pass is being assigned to2c4 or any later head before execution. Previous full on predecessor8609333/tree2ae8508a was **5194 passed /7 known baseline failures /18 skipped /25 xfailed**, zero new failure nodes (`runtime-full-restore-integration-1020095412-22308`). That is historical evidence, not a release-tree full pass. The seven are six `test_runtime_boundary.py` nodes and `test_zero_shim_boundary.py::test_start_does_not_inject_checkout_into_child`.

No current App browser journey, full Gate5, final capture certification, pixels/audio parity, owner-film or macOS claim is made.

## Consumer pin procedure

Set `runtime.lock.json` `source_commit` to `2c4ac180c2220bdad966bc01e95ad230e99ce26a` through the consumer's normal procedure. Producer checkout is read-only and retained at `/home/user/work/wt/rt-m2-pin-2c4ac180`; see [runtime-final-producer-checkout.md](runtime-final-producer-checkout.md).

Agent:

```sh
python scripts/vendor_lock.py update runtime.lock.json --producer /home/user/work/wt/rt-m2-pin-2c4ac180
python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-m2-pin-2c4ac180
```

App:

```sh
node scripts/vendor-lock.mjs update runtime.lock.json --producer /home/user/work/wt/rt-m2-pin-2c4ac180
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-m2-pin-2c4ac180
```

Then each owner runs its current paired tests and records its exact final consumer SHA. Consumer pins do not wait for some other consumer to pin first. Generated bytes move with their lock as one unit. Activation and writer retirement still require their real acceptance/reload/retry/undo proof.

## Historical affected tuples

Both `94114269d1ce23ab3224d7eca5a85138ce2b5fed` /0.2.9 and `6023cfb10307b4c0004642b5fa1995d72ba4f6d1` /0.2.10 are **AFFECTED by F1/F2**, even though their artifact checks passed. They are superseded and must not be relabeled safe. Historical0.2.10 details are preserved in [runtime-tuple-0.2.10-historical.md](runtime-tuple-0.2.10-historical.md). Staging0.2.11/0.2.12 are not consumer targets. Frozen older bundle tuples remain historical and unchanged.
