Implemented the bounded A2 parent-after-anchor VIDEO caller. **HOLD MERGE** pending Agent2304’s independent review, the provider’s owning merge, and independent App Luna review.

Changed six production files plus the existing mounted-save test: **205 insertions, 48 deletions; no files deleted**.

- [ShotTimelineMediaControls.tsx](/home/user/work/wt/app-A2-video-caller-sol-2314/src/tools/travel-between-images/components/ShotTimelineMediaControls.tsx): adds the VIDEO-after-selected-clip action and authenticates the source through the existing Runtime selector using actual registry generation/variant metadata.
- [media.ts](/home/user/work/wt/app-A2-video-caller-sol-2314/src/tools/video-editor/commands/media.ts) and [useTimelineCommandsService.ts](/home/user/work/wt/app-A2-video-caller-sol-2314/src/tools/video-editor/hooks/useTimelineCommandsService.ts): carry the original selection through the prepared command.
- [useTimelineCommit.ts](/home/user/work/wt/app-A2-video-caller-sol-2314/src/tools/video-editor/hooks/useTimelineCommit.ts): retains semantic capture when the VIDEO asset already exists. Testing exposed this necessary sixth seam.
- [timelineLocalSaveHandoff.ts](/home/user/work/wt/app-A2-video-caller-sol-2314/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts): emits the draft provider recipe from `02dea239e`, with exact selections, created references, collection membership/order, and complete source-row step reads.
- [localSaveSession.ts](/home/user/work/wt/app-A2-video-caller-sol-2314/src/tools/video-editor/commands/localSaveSession.ts): persists semantic reads, steps, rationale, and group identity.
- [useTimelineSave.test.tsx](/home/user/work/wt/app-A2-video-caller-sol-2314/src/tools/video-editor/hooks/useTimelineSave.test.tsx): exercises the mounted command → handoff → session → outbox → generated transport path.

Upstream preview behavior is reused; no Python timing or metadata semantics were implemented locally. IMAGE retains exact `intent: {}`. Missing source authority retains the local preview/message with no pending request or POST.

**Validation**

- **217 passed across 11 files**, including 20 mounted IMAGE/VIDEO transport cases.
- After tightening assertions, the entire mounted-save file passed again: **65 passed**.
- Root/App/Node TypeScript checks: **passed**, under `flock`, 4096 MB.
- Scoped ESLint `--max-warnings 0`: **passed**.
- `git diff --check`: **passed**.
- Captured VIDEO request validated against frozen bundles **34eac004** and **8ea0766f**; closed-envelope negative controls rejected unknown fields and body idempotency.
- Initial runner startup failed on `__dirname`; private `$TMPDIR` runner configuration corrected it. jsdom video metadata extraction is stubbed; command/save/transport wiring remains real.

Exact affected-test command:

```bash
NODE_OPTIONS="--require=$TMPDIR/vitest-dirname.cjs" node node_modules/vitest/vitest.mjs run --config "$TMPDIR/vitest.config.mjs" --configLoader runner --no-cache --maxWorkers 1 src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/travel-between-images/components/ShotTimelineMediaControls.test.tsx src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/media.test.ts src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts src/tools/video-editor/hooks/useTimelineCommit.test.tsx
```

Final mounted-file command used the same flags/configuration with only `src/tools/video-editor/hooks/useTimelineSave.test.tsx`.

```bash
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 bash -c 'node node_modules/typescript/bin/tsc --noEmit -p tsconfig.json && node node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json && node node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json'

node node_modules/eslint/bin/eslint.js src/tools/travel-between-images/components/ShotTimelineMediaControls.tsx src/tools/video-editor/commands/localSaveSession.ts src/tools/video-editor/commands/media.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts src/tools/video-editor/hooks/useTimelineCommandsService.ts src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx --max-warnings 0

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$TMPDIR/validate-video-wire.py"
git diff --check
```

The captured full request below is a **transport fixture, not live Runtime authority or Python acceptance evidence**. Its generated transport header was `Idempotency-Key: e411af64-73e4-41af-9410-9a313e195e41`.

```json
{
  "api_version": 1,
  "project_id": "project-commit",
  "timeline_id": "timeline-1",
  "base_revision_id": "r0",
  "base_publication_id": "p0",
  "commands": [{
    "schema_version": 1,
    "op": "clip.duplicate-media",
    "version": "1",
    "select": "parent/clip:source",
    "args": {
      "id": "clip-0",
      "old_media": {
        "asset": "old-video",
        "generation_id": "generation-old",
        "variant_id": "variant-old",
        "object_id": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
        "catalog_digest": "sha256:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
      },
      "media": {
        "asset": "variant-new",
        "generation_id": "generation-new",
        "variant_id": "variant-new",
        "object_id": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "catalog_digest": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
      }
    },
    "intent": {"ownership": "parent"},
    "created": ["parent/asset:variant-new", "parent/clip:clip-0"]
  }],
  "label": "Add video after clip",
  "steps": [{
    "id": "6df9a4d3-bc8f-489c-8048-dfb895e1f482",
    "label": "Add video after clip",
    "intent": "Duplicate selected parent video",
    "tags": [],
    "command_ordinals": [0],
    "patch": [],
    "reads": [{
      "kind": "field",
      "ref": "parent",
      "path": ["config", "clips", "id:source"],
      "state": {
        "state": "present",
        "value": {
          "id": "source", "track": "V1", "at": 0,
          "asset": "old-video", "clipType": "media",
          "from": 1, "to": 5, "speed": 2,
          "transition": {"type": "crossfade", "duration": 0.5},
          "params": {"opaque": [null, false]}
        }
      }
    }]
  }],
  "merge": "fields",
  "reads": [{
    "kind": "collection",
    "ref": "parent",
    "path": ["config", "clips"],
    "members": ["later", "source", "unrelated"],
    "order": ["source", "later", "unrelated"]
  }],
  "dry_run": false,
  "source": {"via": "app"},
  "rationale": "Duplicate selected parent video",
  "group_id": "6df9a4d3-bc8f-489c-8048-dfb895e1f482"
}
```

Mounted controls cover canonical adoption, accepted/merged/rebased replies, structured conflict/invalid refusals, exact retry, dependent rollback, registered assets, and missing/mismatched/nonclosed source selections. Full accepted response/receipt storage remains intact.

Parent-only scope remains explicit. Child, replacement, new-track, and new-group recipes retain existing refusal/draft behavior. Dormant raw tests and the D31 transcript subset were untouched. No backend, browser, full suite, build, dependency, generated-schema, pin, or Git mutations were performed.

Commit message and `DONE` are written. Remaining work: independent reviews and a fresh Agent-owned same-alive Runtime witness; no live parity or new-recipe undo claim is made here.