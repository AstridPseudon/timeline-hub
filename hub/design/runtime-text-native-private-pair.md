# Runtime native text private pair — PASS (private proof only)

The unchanged Agent native tests now pass against final S2 plus the approved Runtime presence/retained-legacy correction. Both original legacy positive requirements ran with `--runxfail`: exact main `text/plain` restoration after replacement/restart, and exact clear/inverse after restart. Canonical new-selection MIME refusals, empty text presence, first-birth undo and retained-V1/group inverse also pass. No Agent product or test edits were made.

## Frozen inputs and private outputs

| Input/output | Exact identity |
|---|---|
| Runtime S2 base | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` (includes final S2 `f7081c1`) |
| Presence patch | `bfec49af4e2bcb82ae2beed922dda99a977b7d72` |
| Retained-legacy correction | `e41f3d1e655a005904bbdc90f04b3ab825f4f225` |
| Agent `tl/agt-m2-text-clear-retained-pair` | `9bf654387c8c1aaa2bc3ef74210fa4a6825956ad` |
| Agent feature provenance | `cb1e907c6846341997e50d7f51aed65a84b6c335` (direct parent) |
| Exact supplied command schema SHA256 | `f0bef48e2a23cc4bdcda27c3b4e2d06ed3bb52487e2a58accfc8d5657673f5c0` |
| Private contract version | `0.2.14` (generated, unpublished) |
| Generated contract schema digest | `sha256:ab8b5dba56f777b935518f2fdaf348e10813224b9aa8cabb2a8b2c1905a3885c` |
| Generated artifact version (75 entries) | `sha256:9bae19991e0e786dc9f7f72e773fe102994db2e1721c1e68273bfbb962075f35` |
| Artifact manifest file SHA256 | `f3af87c8af8573fa0b333a50d2c8c1fa43ba93e8e027dc6db1e87ef784acc2c0` |
| Private candidate inventory SHA256 | `47dd1ea9dd64934dc97f8f85ec2145b698700955d9cc55438637850502660ab6` |

Runtime archive directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-text-clear-native-private-pair/runtime-candidate`.
Agent archive directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-text-clear-native-private-pair/agent-source`.
Full source identities, archive/patch SHA256 and unchanged-test SHA256: [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-text-clear-native-private-pair/source.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-text-clear-native-private-pair/source.json).
Every private file changed from S2: [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-text-clear-native-private-pair/candidate-inventory.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-text-clear-native-private-pair/candidate-inventory.json).

This is a composition of the S2 archive plus the two exact commit patches, not an invented Runtime commit identity. The presence patch applied with zero fuzz (service offsets of nine lines); the legacy patch applied directly. Source verification compared all 3,024 Agent files byte for byte with its frozen archive and checked the 413 Runtime base files plus all 25 private changed/new files. Patch backup output was removed before the successful central submission.

The supplied schema was copied byte for byte into Runtime's canonical schema input, then all clients/bundles/metadata were generated normally. No schema environment override, hand-edited generated client, fake provider, new DTO or newly authored operation definition was used. Structural checks prove all 22 S2 operation clauses and other definitions remain unchanged; the three additive reference unions retain the exact S2 branches and existing native Agent branches, with only Agent's existing `TextBindingSetArgs`/`text-binding.set` added. Normal generation passed all five compatibility floors.

## Evidence

- Central named suite `text-native-private-pair-integration`, result [rt-m2-text-clear-native-private-pair-text-native-private-pair-integration-1020115514-4206](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-text-clear-native-private-pair-text-native-private-pair-integration-1020115514-4206/summary): **46 passed in 19.87s**, exit 0 (service wall time 42s). Exactly the two native text conformance files from the Agent report, all original assertions unchanged, both legacy xfails executed as positives by `--runxfail`. No skips, xfails, xpasses, failures or deselections reported.
- Private Runtime targeted text clear/custody/selection/schema-compatibility neighbors: **199 passed in 103.66s**, exit 0.
- Normal generation, TypeScript conformance generation/check, artifact generation/check and read-only source verification: exit 0. The two legacy-MIME new-input service cases (`mime`, `stored-mime`) and both Agent trusted-inverse/new-legacy-selection unit cases are included in the central pass. Runtime also passes first-use `text/plain`/`text/markdown` refusal on both port and projection, arbitrary-MIME refusal and retained-scope/hash/size/custody/corruption negative controls.
- The native service tests restore the genuine main-API film backup and use the real Agent provider, Runtime service, project-managed CAS, accepted history/closure, restart/retry and atomic projection. No SQL positive history was manufactured. Existing test monkeypatches record real reads or corrupt fixture-local CAS for a negative race test.

Exact commands, generation steps, logs and limitations: [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-text-clear-native-private-pair/notes/report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-text-clear-native-private-pair/notes/report.md).

## Boundary and next step

**PRIVATE proof only; this is not the next public schema freeze or a qualified public consumer tuple.** Runtime public schema remains **22 operations**, version **0.2.13**; observed integration `27ad20bf45f7840c26dfefc69f32d52222abc33a` had schema SHA256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`. No public package, lock, pin, tuple, integration worktree or shared dependency/cache was changed. The assigned Git worktree is clean.

The task is complete with no blocker. Native completion and writer retirement still wait for the normal owner-approved final schema union, fresh authorized public release/pins, and qualification of that real tuple. No full suite, wheel/package build/install, public TypeScript compile, browser/socket/App journey, ZIP, merge or publish was run or claimed. Keep legacy strict markers unchanged here; Agent owner can promote them later with its normal reviewed pair. No design decision was changed or found contradicted by this evidence.
