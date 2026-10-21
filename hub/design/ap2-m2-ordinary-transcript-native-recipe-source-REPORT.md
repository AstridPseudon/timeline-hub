# AP2 M2 ordinary transcript native-recipe source

## Result

**Blocked on an Agent-owned native carrier; no App source change made.** The
one selected live transcript snapshot ingress is the film association in
`src/tools/video-editor/lib/project-transcript-host.ts:600-673` (`associate`).
It currently sends the whole `TimelineData` snapshot through
`commitData(next, { save: true, semantic: true })` after changing the selected
document association, replacing the asset's source-item collection, and
reconciling generated-caption provenance/review keys.

The current TimelinePatch consumer in
`src/tools/video-editor/hooks/useTimelineOps.ts:267-321` only sends a patch to
the generic native port when the complete batch is classified as supported;
otherwise it validates/compiles and reaches the existing snapshot writer.
There is no safe row-local App capture for this film mutation because the
exact Agent cohort has no command that writes the timeline-level transcript
association or source-item plane.

## Classification

- Project transcript document create/update (`importTranscript`, source text
  correction, undo/redo, and promotion) is producer/catalog state. It already
  uses the existing project-document CRUD surface and must remain there.
- `replaceTransient()` projections are derived and memory-only. They must not
  enter film history.
- `associate()` is film state: it changes `transcriptReferences`, selects the
  exact project document for an asset, and may rewrite generated caption
  identity/provenance. It must be one guarded film edit when a native carrier
  exists. Unplaced catalog/document work must not be moved into this path.
- The transcript-lane source-review decision patch is separate extension
  project-data/catalog state (`project-data.write`); it is not a substitute
  for the film association and remains on its current project-data path.

The association path preserves the required semantics today: it carries the
document identity, keeps source-item order/opaque envelopes, and calls
`reconcileTranscriptReferences()` rather than guessing from text. A future
native migration must retain stable segment/word identity, exact document
pinning, original base/intent/grouping/opaque fields, explicit absence, and
atomic refusal for ambiguous mappings.

## Exact Agent finding

The source handoff pins Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`.
Its closed registry includes `clip.set`, `clip.set-params`, `shot.set`, media
carriers, and `timeline.restore`, but no timeline transcript-association or
source-plane replacement operation. The current integration Agent
`520fd21796f9a0480c1b5cc147fae10f4288444c` retains the same relevant closed
union. `source_mapping.pinned_documents` is an input/dependency capture used
by existing parameter/timing commands; it is not a command for selecting or
replacing `TimelineData.transcriptReferences`.

The related `timeline_reference` field in the later Agent carrier is limited
to an `occurrence.add-media` birth. It cannot update an existing media
association, carry the project transcript document pin, or replace the
source-item collection, so it is not a match for this ingress.

## One executable literal counterexample

This is the smallest existing-command-shaped attempt to express the live
association. Running it through the exact current Agent validator:

```python
from astrid.sdk.timeline.commands import CommandError, validate_command

command = {
    "schema_version": 1,
    "op": "clip.set",
    "version": "1",
    "select": "parent/clip:audio-a",
    "args": {
        "values": {
            "transcriptReferences": {
                "schema": "media.transcript.references/v1",
                "associations": [{
                    "assetId": "audio-a",
                    "documentId": "transcript:project-1:sha256:audio-a:source-1",
                }],
            },
        },
        "clear": [],
    },
}

validate_command(command)
# CommandError: Additional properties are not allowed
# ('transcriptReferences' was unexpected)
```

This is an atomic schema refusal before any capture or write. `clip.set` only
accepts its bounded raw clip fields; using `timeline.restore` would be a
whole-image bypass, and using project-data would put film state in the wrong
catalog namespace.

## Smallest Agent peer request

Agent should provide the smallest native film-source association recipe (or
extend an existing source-reference recipe if its contract genuinely fits)
and its Runtime-compatible schema/registry entry. The recipe must atomically:

1. guard the exact prior association for one asset and the exact immutable
   transcript document pin (`document_id`, version, content digest);
2. preserve and record source-item collection membership/order, opaque item
   envelopes, stable segment/word identities, and the original base/intent/
   grouping fields;
3. apply any unambiguous generated-caption identity/provenance and review-key
   reconciliation in the same film edit; and
4. refuse ambiguous/shared identity, missing/revoked pin, unsupported shape,
   or changed guard before capture/submit, with normal inverse, rebase, retry,
   and A→B→A protections.

Until that paired carrier is qualified, App must retain `associate()`'s
existing snapshot writer and the project-document CRUD positives. No App-only
DTO/op/store/framework, text-only inference, client rebase, sequential partial
submission, or activation guess is justified.

## Evidence

Passed:

```text
./node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/data/typed/importTranscriptIdentity.test.tsx \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx
=> 3 files, 60 tests passed
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent \
  /home/user/work/venv-app2-native/bin/python -m pytest -q \
  /home/user/work/agent/tests/sdk/test_timeline_current_union_schema.py
=> 24 passed; 2 existing PytestConfigWarning warnings
```

The direct Agent validator probe produced the refusal quoted above. `git diff
--check` passed and the assigned App worktree is clean. No browser, socket,
request-test, full suite, dependency/pin/schema/server edit, or App copy was
used. No native positive commands/records are claimed because the required
recipe is absent.
