# Agent canonical element successor S2

2026-10-20. Reviewed-source composition candidate only. **S1 is immutable. S2 needs an explicit manager freeze before normal Runtime generation.** No activation, new Agent/Runtime pair, endpoint retirement or WC4 closure is authorized by this document.

## Explicit source and schema

- Candidate branch: `tl/agt-m2-element-current-union`; worktree: `/home/user/work/wt/agt-m2-element-current-union`.
- Exact base: `df2739f903edac02bd36b4446deeea847524c040` (current integration at assignment: public12, D07, auto/pool and equal-state delete controls).
- Final commit: harness-assigned after worker exit; manager must resolve this branch and record/verify the commit before freezing S2. No fabricated future commit is asserted here.
- Changed product-source manifest SHA256: `82102acd57bc562a321708eda295053953cb582bc52f36d3f03125928fb5c88a`. Defined as SHA256 of the UTF-8 manifest below, including its final newline; this identifies the source bytes before the harness commit, not a Git commit/tree hash.
- Canonical schema: `astrid/core/timeline/schema/edit-command.schema.json`.
- Raw schema SHA256: `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.
- Inventory: **48 definitions / 22 operation conditions** (20 native recipes plus inverse/restore).

Operations in canonical order:

`clip.delete`, `track.set`, `shot.set`, `clip.set-params`, `clip.set-element`, `timeline.inverse`, `timeline.restore`, `clip.move`, `clip.add`, `occurrence.add-media`, `occurrence.swap-media`, `placement.move`, `placement.create`, `placement.unplace`, `shot.pool`, `track.create`, `clip.set`, `clip.trim`, `clip.split`, `occurrence.duplicate`, `occurrence.delete`, `producer.guard`.

```text
a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef  astrid/core/timeline/schema/edit-command.schema.json
43e77236a368b7a6170298e2938857276dd87d4ba57fbd269e056267582233dd  astrid/sdk/timeline/__init__.py
6e3e2bb14b110d3db7190a311d3975444674ece2b2ebb54d2c24107a65e64774  astrid/sdk/timeline/_clip_scalar_commands.py
fbde10228b7365ace7c4757fa2a378838011ae75d9b3ddb301cb640cbac7e2b8  astrid/sdk/timeline/_recording.py
06aec244813de84be00bee0c495ce14b54ba00c58a2266064fce96f6df4b42f7  astrid/sdk/timeline/commands.py
6355cab5a7cd033bf9e179c2b729eeb0f1425e20901df1e0c4fc2c8f92e116c4  astrid/sdk/timeline/commit.py
420d44af09fef5f793d34fa0eeddb111bc94b750f58c7466f4d28690268be32f  astrid/sdk/timeline/producer.py
dde8eb5474ed9df4798d7816c70da30e93e66dd75f2b543ecb4c01681c9e3ee3  astrid/sdk/timeline/rebase.py
56a3427b46ed00d3ff00d1fea59a9fdf91974146032333fabb5ba358cad6285b  astrid/sdk/timeline/sync.py
ac8f651e371ef4d12aa746bae297045cc4892106c857df085c43e7c130281f50  astrid/sdk/timeline_elements.py
```

## Three bounded parts

**Producer only:** port `0a0ac7baaa74e15485b10bcbaa80eda1afe48c00^` → `0a0ac7baaa74e15485b10bcbaa80eda1afe48c00` only for producer registration, provider capture, recording/replay, existing requester outbox support, producer tests and the schema compatibility helper/floors. Auto-placement code and old auto/media fixtures are not copied. `producer.guard` remains pin-only, with the original settled digest, commands, rationale and admitted base carried through the existing outbox; no new outbox behavior is claimed for the element helper.

**Element / WC4 source:** port `167d050506b9ae81fe8839f122de34d2082558cf^` → `98c38a7c85a3f1d2a8c5a1019a5815898ec922f5` on the bounded helper, scalar recipe, declaration resolver and their tests. The helper emits one native batch: set-element, optional source-seconds hold, optional nonempty params patch. It keeps selected owner/id/kind, exact retained declaration/snapshot inputs, absent/empty params and opaque authored data. The whole-candidate helper publisher stays deleted. Existing recording derives any config.clips mirror. The permanent Runtime-service module now includes raw element-only authority/refusal inputs and a second genuinely admitted owner with matching id/kind; both provider and helper refuse owner substitution.

**Current preservation:** current auto/pool/eligibility code and fixtures, public12 render/theme adoption, D07/native scalar/selected-schema flow, ordinary operations, inverse/restore, roots and delete positives remain. No `92427b3a` host/capture delta was imported (it was absent from the assigned base); no existing host/capture hunk was changed. No parent `clip.add-media` or `timeline.assembled-target` variant was added. Runtime pin/client and endpoints are unchanged.

## S1 stays frozen; S2 is additive

S1 source `0a0ac7baaa74e15485b10bcbaa80eda1afe48c00`, raw schema SHA256 `30da4fde84c328e7cb44035b50eb53fd2cd9637a14a0c948f4412f6469ce34bd`, remains untouched along with `design/agent-canonical-current-union.md` and its manager freeze.

S2 is byte-identical to that S1 schema except the reviewed `ClipSetElementArgs` definition: optional `schema_source: {"$ref":"#/$defs/DocumentPin"}` and the reviewed owner/retained-pin description. Required remains `["elementRef"]`, additionalProperties remains false. All five producer definitions, the producer.guard conditional, both closed optional consumed arrays, all ordinary definitions/conditions, numeric constraints, roots and inverse/restore definitions remain unchanged.

`tests/sdk/test_timeline_current_union_schema.py` checks all definitions and operation conditions of FOUR complete immutable input schemas, exercises every dropped definition/op and numeric narrowing, and independently enforces the exact S1 → S2 allowance. Snapshots and pinned raw digests:

| Input | Raw SHA256 | Defs / ops |
| --- | --- | --- |
| Agent c456b328 (prior floor) | `40ce6d81487f39236fbfb3adf13e6e0c3f43cfcc375b39b7badc32d65531fd4b` | 43 / 21 |
| Runtime 6023cfb / 0.2.10 (published floor) | `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9` | 35 / 14 |
| Agent current df2739f9 | `83a476f894f31dc359514e9c081bf28da2b1f8cd515bb30cce14292823753224` | 43 / 21 |
| Frozen Agent S1 0a0ac7ba | `30da4fde84c328e7cb44035b50eb53fd2cd9637a14a0c948f4412f6469ce34bd` | 48 / 22 |

The old 43-definition element candidate is not the outgoing source. It would remove producer/consumed behavior; S2 corrects that exact handoff hazard.

## Qualification boundaries and manager gate

Public helper retry remains narrower than captured-request replay: `update_parent_element(expected_head=old, idempotency_key=same)` reopens the head, sees the already accepted revision and returns conflict before Runtime idempotency lookup. The retained-element cases prove replay of the original captured request through RuntimeService, not restart-safe helper/outbox behavior. They also do not qualify HTTP-to-public-ErrorObject mapping or element-specific changed-payload/same-key behavior on a new generated pair.

The original real producer positive is retained as strict xfail. Against untouched Runtime6023cfb, preview still fails `producer_dependency_unavailable` / “producer authority requires its guard record”: Runtime compares the bare request guard to Agent's normalized recorded command. Four artifact mutation refusals pass; accepted producer mutation/restart/retry/undo is not green. No Runtime code or request shape is changed to evade this boundary.

Agent remains pinned to Runtime94114269 / 0.2.9; the real element cases use that immutable Runtime via the normal test locator. Runtime6023cfb's public schema still has no explicit typed producer guard. Generic-envelope transport is not publication qualification. New generated element/producer types, authentic assembler/App handoff, sockets/browser/render/pixel/macOS evidence and WC4 closure remain outside this source composition.

Manager next: verify final harness commit and S2 raw schema hash, explicitly approve/freeze **S2**, then have Runtime publish a NEW normal generated pair from these exact complete bytes (`python generators/generate.py`, `python scripts/artifact_manifest.py` and normal release checks). Refresh Agent with `scripts/vendor_lock.py`, rerun retained-element and original producer positive qualification on that immutable pair, and only then consider activation/endpoint/WC4 gates. Never rewrite S1's freeze or historical releases. No full/full* suite was requested.
