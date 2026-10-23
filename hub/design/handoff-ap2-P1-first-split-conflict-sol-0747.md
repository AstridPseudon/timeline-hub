# P1 first-split conflict: bounded offline diagnosis

Worker: `ap2-P1-first-split-conflict-sol-0747`. Read-only product investigation, 2026-10-23. **No H3 GO. Independent review and owner-assigned corrections are next.**

## Finding and owners

The source-derived witness reproduces the retained 20165 signature: **409 / conflict / path `["clips"]` / `Read the current timeline and retry the edit` at the first split, at an unchanged head.** Its actual provider reason is `identity_conflict: contradictory parent mirrors` in Agent `astrid/sdk/timeline/_doc_patch.py:264`, called at line 415. This is not a stale declared collection or a bad previous-value operand at the original base.

Two defects compose:

1. **Agent / R1:** an id-addressed parent clip leaf installs into the primary clip row only (`Closure.native_sites`, `_doc_patch.py:184–187`; `Closure.install`, line 222). The config mirror is synchronized by `Recording.compile_mirrors` (`_recording.py:229`) only at command completion (`commands.py:247`). A later, unrelated change inside the SAME `doc.patch` observes the provider's temporarily inconsistent bundle and fails `validate_payload`. The contradictory-mirror guard is necessary; its input is wrong because the provider deferred its own mirror write.
2. **App / A2:** the split's resolved display config introduces unrelated authored changes: the selected clip's absent `label` becomes the derived asset display name, and raw `config.output.file: "out.mp4"` becomes the rebuilt default `"output.mp4"`. The latter comes from `useTimelineCommit.ts:533` → `serializeForDisk` (`serialize.ts:146`, deletes output) → `buildDataFromCurrentRegistry` → `assembleTimelineData` (`timeline-data.ts:451–474`, fills defaults and supplies resolved display labels). `timelineLocalSaveHandoff.ts:187` then interprets those differences as authored intent. This extra output change exposes the Agent sequencing defect after the clip changes.

**Not an already-fixed execution gap:** the relevant `patch`, `validate_payload`, `normalized_path`, `value_at`, `Recording`, and `State` ASTs are identical between pinned Agent `f894c3c9dda25ab03527eeb7f52da5da31d627c1` and requested comparison Agent `4edc4b321cae5cfc58252d7ed89e3f0408238646`. They are also identical in the current Agent source observed during this investigation (initially `d24da4af0…`, subsequently `e49a6e76b3ab363e312c55b313714af1f845f54b`). A second pure provider execution using current Agent + Runtime `a5d4258312c979024865ee704da2d632ca5b2730` fails at the same line with the same reason. Runtime cannot repair an exception raised before prepared-record authentication/acceptance. The frozen full-v2 CLIENT34e is a separate concern and needs no change for this diagnosis.

## Original basis, wire operands, and exact failing boundary

App candidate is `2b26c20a99fd14a9076fd0cbd6aa5548de14e35b`, tree `45f4b3ca9e204d3cc0223bb9929301ab5e40cf25`; P1 spec SHA-256 is `d72798b2301973bfdabcf3b07c2746896e9ec5cd6188bebeda53733c070647a8`. App integration `890b9561666c3619f69335dd747b15e042b3a9a3` has identical relevant source; its handoff SHA-256 is `c2dc575f9657ad37453edd27bc6d2e0306cb0fa96047b335ee993b83a086a445`. No paired-head regression or publication waiver is proposed.

The production caller is `useClipSplitting` → `useClipEditing.applyConfigEdit` → `useTimelineCommit` → scheduled save → `useTimelineSave` → `timelineLocalSaveHandoff` → `documentPatchIntent` → `localSaveSession` persisted outbox → `provider.commitTimeline`. `loadTimelineCommandBasis` (`dataProvider.ts:872`) captures history's exact revision/publication pair, scoped immutable parent/child reads and verified pins. The handoff checks that original head and source; it does not refresh the original operands at send time. The session adds the full-v2 commands, label, complete submitted step patch, merge and reads while retaining the original allocated ID and persisted request/key.

The original seed (`seedOneClip`) has equal top-level `clips` and `config.clips`, one `p1-chain-source` row with `at=0`, `hold=8`, `from=0`, `to=8`, `speed=1`, track V1, media asset `p1-video`, no authored label, and the original opaque/null/app namespaces. Output is resolution `1280x720`, fps 30, file `out.mp4`. There are no occurrences or child images.

The seed's legacy publication precedes `enableTimelineAuthoring`. Runtime stores its payload through `canonical_json(parent_payload)` (`service.py:3125`; `util.py:24` sorts object keys). `install_verified_baseline` (`timeline_commit_store.py:1276`) authorizes, checks membership, verifies/rechecks the existing publication and imports history against its exact head. `baseline_install_plan` (`timeline_commit_baseline.py:401`) does not manufacture a new publication. The immutable parent bytes remain the basis; this is not an empty bootstrap replacing the seed. Sorted raw payload keys put `clips` before `config`.

`documentPatchIntent.ts:203` walks that key order and emits one logical clip address, suppressing its config mirror. The reconstructed production transform emits, in this order:

| Ordinal | Submitted change | Protected original operand |
| --- | --- | --- |
| 0 | `list.insert parent/[clips]`, new right ID, `after_id=p1-chain-source` | `before=absent`, `order_before=[p1-chain-source]`; new row at 2, hold 6, original app data retained |
| 1 | `set parent/[clips,id:p1-chain-source,hold]` to 2 | `before=present(8)` |
| 2 | `set parent/[clips,id:p1-chain-source,label]` to derived media display name | `before=absent` |
| 3 | `set parent/[config,output,file]` to `output.mp4` | `before=present("out.mp4")` |

The offline witness uses the original source's mp4 seed branch, so its display name is `p1-video.mp4`; the harness also has a webm branch. Dynamic scope/media/publication IDs in the witness are deterministic placeholders, not recovered live credentials or pins.

All **13 original request reads remain**: selected raw id, track, at, clipType, hold, from, to, speed, asset; raw output fps; the selected raw registry entry at normalized `config/registry/assets/p1-video`; collection members/order `[p1-chain-source]`; and absent `config/pinnedShotGroups`. Request reads are captured once at batch entry. The provider gets past every read and every protected before/order comparison in the original witness.

After ordinal 0, both collections contain `[source,right]`. After ordinals 1 and 2, the native primary source has `hold=2` and the display label, but the stored config mirror source still has `hold=8` and no label; the new right row remains equal in both collections. Each clip change's local temporary root is mirrored for validation, but `Closure.install` drops that local mirror when it selects just `parent/clip:<id>` for installation. At ordinal 3, its own `before=out.mp4` still matches. The unrelated output change does not repair clip mirrors, so line 415 passes the inconsistent root to line 264. There is **no membership/order difference** here: IDs/order match; the two copies of existing item contents differ due to this transaction's own writes.

The pure `_commit_errors.failure` projection yields the exact retained public status/code/path/hint even with `base == current`, because `identity_conflict` is not classified as invalid-at-base and has the generic hint. No HTTP call was made.

## Minimal correction direction

**Agent owner:** keep all physical representations of a logical parent clip synchronized at each successful sequential change, within the existing authoritative recorder, before the next change reads or validates the bundle. Repair the id-addressed leaf installation/mirror timing seam; retain initial contradictory-mirror validation, previous-value checks, complete collection guards, exact physical closure bindings, authentication and final Runtime checks. Deferring synchronization to command completion is insufficient. The exact recorder representation and Runtime authentication/undo consequences require implementation review and main-suite tests; no production patch is supplied or qualified here.

**App owner:** preserve original authored output and label provenance across the config-gesture serialization/rebuild seam. A split must not author rebuilt render defaults or asset-derived display names. Carry raw output through the local save mapping when serialization omits it, and keep authored/absent labels distinct from resolved display labels, including the new split row. Use the existing raw-authoring mapping; do not add another semantic executor. Retain D13's actual consulted reads and the original full-v2 accepted/merged/refused/invalid requirements. Fixing these unrelated operands can remove this immediate trigger, but does not fix Agent's general sequential-mirror defect.

Moving output changes first is only a diagnostic control, **not** a proposed workaround. Do not edit the fixture output to equal the default, weaken the original assertions, fabricate empty reads, force atomic/overwrite, or grant accepted/merged credit to a refusal.

## Commands, results, and limits

Scratch is the worker's assigned tmpdir target `/tmp/w-8d0bbceefd` (the assigned worker `tmpdir` file contains that path). No tracked worktree files changed. Exact decisive commands, run from the assigned App worktree:

```sh
node /tmp/w-8d0bbceefd/prepare.cjs
TSX_TSCONFIG_PATH=/tmp/w-8d0bbceefd/tsconfig.json node_modules/.bin/tsx /tmp/w-8d0bbceefd/probe.ts > /tmp/w-8d0bbceefd/app-probe.log 2>&1
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-pin-34eac004:/home/user/work/wt/agt-pin-f894c3c9 /home/user/work/venv-app2-native/bin/python -P /tmp/w-8d0bbceefd/provider_probe.py > /tmp/w-8d0bbceefd/provider-pinned.log 2>&1
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/runtime:/home/user/work/agent /home/user/work/venv-app2-native/bin/python -P /tmp/w-8d0bbceefd/provider_probe.py > /tmp/w-8d0bbceefd/provider-current.log 2>&1
```

`prepare.cjs` and final App probe exit **0**. The seed clip literal is extracted by TypeScript AST from the unchanged P1 source. Seven split helper declarations are extracted verbatim by AST from `editor-utils.ts`; its real duration helper and the real load/build, serialization, handoff and patch emitter modules execute offline. This avoids importing unrelated Vite virtual admissions. Both provider commands exit **2**, intentionally reporting the reproduced `identity_conflict` at `[clips]`. A nonmutating observer prints primary/mirror operands at the failing validation; no provider guard is changed.

For each mode below the exact command was:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-pin-34eac004:/home/user/work/wt/agt-pin-f894c3c9 /home/user/work/venv-app2-native/bin/python -P /tmp/w-8d0bbceefd/provider_probe.py MODE > /tmp/w-8d0bbceefd/MODE.log 2>&1
```

| MODE | Result |
| --- | --- |
| `order-control` | Exit 0, one recorded command; same four changes, IDs, values and 13 reads, independent output change moved first |
| `bad-previous` | Exit 2, `previous_value_mismatch`, source hold before 9 versus actual 8 |
| `bad-order` | Exit 2, `previous_value_mismatch`, original collection order changed |
| `bad-read` | Exit 2, `previous_value_mismatch`, selected declared hold read 9 versus actual 8 |

These are scratch diagnostic controls, not rewritten behavior tests or changed production requests. Python AST comparison using `git show`/`ast.dump(include_attributes=False)` passed all three selected module comparisons described above. `git diff --check` passed; `git status --short` is empty. There was no main-suite test run, test-service request, HTTP, browser/test-body execution, live service/socket, build, dependency/cache write, pin/schema/generated/ops/fixture edit, commit/merge/checkout, publication or release.

The first exploratory direct TSX import failed on `@astrid/packs/rendering/elements/catalog.ts`, then on Vite's `virtual:astrid-element-admissions`; the private AST extraction resolved that tooling limit without changing product source. An initial unsorted in-memory parent emitted output first and passed; switching the scratch document to Runtime's actual canonical key order exposed the failure. A first probe omitted load-time output defaults and failed the original-source check; the final probe calls the actual `withDefaultTimelineOutput` load path. None of these exploratory probes is counted as original P1 success.

Evidence limit: retained 20165 has summary/log/status/source identities and the two public diagnostics; its snapshot worktree, Playwright trace and temporary realm are no longer present. Therefore this is a source-derived causal reproduction, not a byte-for-byte replay of the deleted original request or independent reauthentication of its realm. The original run remains **2 failed in 93s**; no accepted split, merged trim, refusal rollback, lost-ACK/restart/retry, history or undo proof is newly claimed. Have independent review confirm the diagnosis and assign Agent/App corrections; only then consider manager-owned changed-evidence original P1 execution. H3 remains blocked.
