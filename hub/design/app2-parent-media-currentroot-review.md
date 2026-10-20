# App2 parent media current-root source review

Verdict: **APPROVE source port** `cc8dece481bb96f462adad26210b7a20f45fb701` over
`05b6b488d1834650c459c5c565f2530d9bea20e9`.

Consumer activation: **HOLD separately**. This review does not qualify a
producer, commit-session adapter, Runtime durability, legacy-writer retirement,
browser journey, or shared wiring. The proposed shared artifact is correctly
documentation-only: the current producer does not expose the original closed
five-field media selection together with the detached Runtime-verified media
response. Adding a consumer hunk now would fabricate provenance.

## Source review

`parentClipAddCapture.ts` is source-only and uses the current-root
`MoveRecording`/`AuthoredBundle` primitives. The capture basis freezes a copied
bundle, command, and verified inputs; finish/retry re-executes that frozen basis.
The command preserves the caller-owned raw clip ID and asset alias, the complete
row, and the exact five selection fields (`asset`, `generation_id`, `variant_id`,
`object_id`, `catalog_digest`). Verified input must contain an identical
selection and unambiguous identical metadata, with positive size and image/video
type; video additionally requires positive intrinsic duration.

The executor records the expected current-root sequence: FPS/source reads,
parent ownership, track selection and binding, occurrence-lane guard, effective
registry selection and exact media dependency, then clip collection selection,
absence guards, writes, and derived compilation. Stable IDs reject path-like
aliases and occupied clip identities. Active visual output tracks are required;
occurrence-owned lanes, disabled/hidden/deleted tracks, divergent clip mirrors,
conflicting registries, malformed assets, unsupported timing/source fields, and
changed selections refuse before mutation. Opaque row/registry fields survive.

The repaired cases are correct and preserve Agent ordering:

- Equal parent/config registry mirrors without `assets` create one recorded
  effective-container write and materialize the binding in both mirrors.
- Equal empty parent/config clip mirrors receive the birth in both arrays and
  record the authoritative `parent.config.clips` derived write.
- Populated registry/clip mirrors preserve existing ordering and opaque data.

The focused tests cover the positive birth, detached retry after caller mutation
and JSON reload, both mirror repairs, stale track/owner/selection refusal, and
missing/fabricated provenance refusal. No source, test, shared integration,
generated, pin, dependency, or consumer files were changed by this review.

## Evidence

Focused current-root tests:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/media.test.ts src/tools/video-editor/commands/runner.test.ts
→ 3 files, 26 tests passed
```

Static checks:

```text
node_modules/.bin/eslint src/tools/video-editor/commands/parentClipAddCapture.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts --max-warnings 0
→ passed
git diff --check
→ passed
```

Independent actual-TS-to-Agent-310 probe, using the private frozen source tree
and `/home/user/work/venv-app2-native` only:

```text
node --import tsx /tmp/ap2_parent_media_currentroot_ts_probe.ts > /tmp/ap2_parent_media_currentroot_ts_probe.json
AG=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary
PYTHONPATH="$AG" /home/user/work/venv-app2-native/bin/python /tmp/ap2_parent_media_currentroot_agent_compare.py
→ all_passed: true for populated, opaque-registry-mirror, and empty-clips-mirror
→ command, records, authored projection, runtime projection, inverse, and replay all matched in every case
```

The temporary probe files were private evidence only and were removed after the
run. No old expected-only payload or stale temporary golden was used as native
proof.

Not run: full suite, Runtime durability/reload, localhost/live sockets,
browser/e2e, or actual App consumer acceptance. Those remain prerequisites for
the separate consumer activation decision.

## Recommendation

Merge/qualify this source port as an independent native helper. Keep the legacy
producer and manual recovery paths unchanged until an App-owned adapter has the
exact verified inputs and proves acceptance, reload, guarded undo/redo, lost-ack
restart retry, and zero legacy traffic through the existing session/outbox.
