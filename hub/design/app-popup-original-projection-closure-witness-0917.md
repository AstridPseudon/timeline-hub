# D01-app-popup-swap — original accepted projection witness

## Verdict

**UNKNOWN: no original Runtime-accepted popup SWAP closure is retained.**

The retained material is source-only. It does not contain the accepted
`CanonicalDocument` + publication/head pair needed to distinguish the local
projection from the accepted projection. D01-app-popup-swap remains OPEN;
the old popup writer must not be retired from this evidence.

## Exact retained source references

- Native source fixture at App ref `309cb7a463833126e3af730fb3c6ff536d9e457c`:
  `src/tools/video-editor/commands/fixtures/recipe_m2_occurrence_media.json`
  (SHA-256 `e30ed3303532e3d73adfd07670e04d1312003b7e10d2c5c008629b8b9bffad46`).
- Retained normal-graph source artifact:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-popup-analog-playable-vp8-native.json`
  (same SHA).
- Agent source/golden contract:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-popup-native-contract.md`,
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agent-expanded-recipe_m2_occurrence_media.json`.
- Viewing pure projection witness (not acceptance):
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-popup-original-document-pure-projection-witness-0827-REPORT.md`
  and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-popup-original-document-pure-projection-witness-0827-vectors.json`.
- App consistency limits:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-popup-projection-consistency.md`.

## Inspected source-only identity witness

The supplied `swap.output` has:

| Field | Inspected value |
|---|---|
| scope | `project-1` / `film` |
| source input parent | `parent-1`, digest `sha256:86c97a97fb837467f83918e31ce27d76c59740c83fec38a22562ce4d213c249b` |
| source output parent | `authoring-parent-revision-d35a5f7f583efa7dfd35b1d753cb32828cc5883957a1b396696c1e433871e09b`, digest `sha256:2ef8479aa665cdc745c75c23a615e0edae99235c3db7de6822b5715a38efd9b3` |
| manifest references | `chapter-shot/shot-1` → `sha256:f700f1f65d6111e008f10de355a74ab6b41b766f4ff4070bd62f97206a3f0775`; materialized shot/revision and internal-timeline/content digests retained in the source artifact |
| media references | old `sha256:111…111`; new `sha256:222…222` |
| raw swapped child | occurrence `occ-a`, raw child `clip-a`, `track=picture`, `at=1`, `hold=4`, `[from,to)=[2,6)`, `speed=2`, asset `reserved-new` |
| occurrence placement | `occ-a` starts `8000 ms`, stored duration `10000 ms`; `occ-b` starts `10000 ms` on the same `picture` lane |
| FPS | `{numerator:30000,denominator:1001}` |

The source output has no publication ID, accepted head, receipt, or accepted
HTTP response. Its dependency manifest is source data with `shots=2`,
`internal_timelines=2`, `media=2`, `documents=0`; it is not an acceptance
manifest. No accepted identity is inferred from the authoring revision.

## Projection handoff

The source-only pure projector comparison observes, for the unchanged raw
child, local/unbounded `to=6` versus default capped `to=4`; `occ-a:clip-b`
is present locally and omitted by the capped derived projection. This is not
an accepted SWAP vector. It is the existing App seam:

- accepted-path source: `src/tools/video-editor/hooks/useTimelineCommandSession.ts:81-95,107-115`,
  calling `projectCanonicalComposition(composition)`;
- cap: `src/tools/video-editor/data/shotCompositionProjection.ts:437-447`;
- local popup source: `src/tools/travel-between-images/components/shotTimelineDataProvider.ts:435-480`.

Agent compiler and Viewing must verdict this against one actual accepted
closure, preserving the raw child/source window and the exact scope, revision,
manifest, and media identities. Do not use the pure source output as accepted
authority, replay the edit, synthesize a publication/head, flip the global
clamp/default policy, or add a new carrier/compiler.

## Normal immutable-read paths inspected in the source-only transport

These are the exact normal GET shapes represented by the retained graph probe,
not proof that a live accepted realm still exists:

```text
GET /v1/projects/project-1/timelines/film/composition-revisions/<parent-revision>
GET /v1/projects/project-1/shots/<shot-id>/revisions/<shot-revision>
GET /v1/projects/project-1/timelines/<internal-timeline-id>/revisions/<internal-revision>
```

The source probe used the input IDs above and the materialized output IDs
retained in the source artifact. No authenticated live GET was attempted:
there is no retained authenticated realm/response to pin, and the historical
popup runs stopped before commit acceptance.
