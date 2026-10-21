# App proposal: server-derived transcript `DocumentPin`

Status: unapplied App consumer proposal. No live callers were changed.

## Result

At the ordinary project-transcript read/write → `associate` boundary, carry the
exact `content_digest` returned by Runtime into the existing `DocumentPin`
shape. App must not hash transcript content and must not reread a mutable latest
document to manufacture a pin.

The proposal is intentionally limited to:

- `src/tools/video-editor/data/typed/projectTranscript.ts`: optional resource
  typing/validation and a small mapper to the existing `DocumentPin` type;
- the existing `RuntimeDataProvider.projectTranscripts` pass-through, which
  already sends list/get/create/update resources through
  `parseProjectTranscriptDocument` and therefore needs no live logic change;
- the exact caller site in `project-transcript-host.ts`'s `associate` flow,
  where a future native proposal would consume the returned resource pin.

There is no new DTO, endpoint, store, browser hash, latest-read admission,
generated-client mutation, or writer removal in this proposal.

## Proposed patch (not applied)

The resource policy would add the exact lower-case SHA-256 form while keeping
old immutable resources readable:

```diff
diff --git a/src/tools/video-editor/data/typed/projectTranscript.ts b/src/tools/video-editor/data/typed/projectTranscript.ts
@@
 import type { AssetRegistry } from "../../types/index.ts";
+import type { DocumentPin } from "@/integrations/runtime/timeline-commit-types.ts";
@@
 export const PROJECT_TRANSCRIPT_KIND = "media.transcript";
 export const PROJECT_TRANSCRIPT_SCHEMA = "media.transcript/v1";
+const documentDigest = z.string().regex(/^sha256:[0-9a-f]{64}$/);
@@
 export interface ProjectTranscriptDocument {
   readonly receipt?: unknown;
+  readonly content_digest?: z.infer<typeof documentDigest>;
@@
 }
+
+export function transcriptDocumentPin(
+  document: ProjectTranscriptDocument,
+): DocumentPin | undefined {
+  if (document.content_digest === undefined) return undefined;
+  return {
+    document_id: document.document_id,
+    version: document.version,
+    content_digest: document.content_digest,
+  };
+}
@@
 export async function parseProjectTranscriptDocument(
@@
   if (d.document_id !== await transcriptDocumentId(...)) throw ...;
+  documentDigest.optional().parse(d.content_digest);
   return { ...d, content };
 }
```

The real patch would retain the existing identity checks and use the full
existing call rather than the abbreviated diff above. The provider pass-through
has the required shape already:

```ts
listAll: async () => {
  // each raw Runtime item, including content_digest, enters the policy parser
  return rawItems.map((d) => parseProjectTranscriptDocument(d, this.projectId));
},
get: async (id) => parseProjectTranscriptDocument(await client.getDocument(...), projectId),
create: async (...) => parseProjectTranscriptDocument(await client.createDocument(...), projectId),
update: async (...) => parseProjectTranscriptDocument(await client.updateDocument(...), projectId),
```

No `dataProvider.ts` hunk is proposed: its current implementation already
passes raw Runtime resources to the parser, whose spread return preserves
unknown resource fields. The generated `ProjectDocument` declaration is also
left untouched by this unapplied proposal.

At the host's `associate` caller, the future native-proposal-only branch would
use `transcriptDocumentPin(document)` on the exact `ProjectTranscriptDocument`
already returned by `r.get`, `r.create`, or `r.update`. For a replacement, it
would pass the exact new and prior pins to the existing retained-read helper
(`readRetainedTranscriptSources`), then invoke the dormant association capture
only after both returned resources match those pins. The ordinary existing
`commitData(..., { save: true, semantic: true })` snapshot association remains
the live path.

Ordering requirement for a later activation:

1. Build the exact new/prior pin pair from returned resources; do not calculate
   a digest from `content` and do not perform a latest read.
2. Run retained-read verification and the existing atomic association capture
   before `commitData` or any outbox mutation.
3. If the digest is absent on an old resource, visibly refuse only the native
   proposal (`missing_document_digest`-style refusal), preserve the draft and
   outbox, and leave the current successful snapshot association available.
4. If caption/review reconciliation or another unsupported carrier is
   rejected, refuse atomically before snapshot/outbox mutation; do not strip or
   partially rewrite caption/review data.

The host's current association/import/promote writer is not changed or removed.
`transcript.associate` is not activated.

## Evidence and source mapping

- Runtime `4e1133fb` (`rt-m2-document-digest-source-independent-review-0946`,
  following the owner-approved `09:44` source) derives `Document.content_digest`
  from canonical content, adds the optional exact-SHA schema field, and tests
  create/read/update/retry behavior.
- Agent `abe0fd6f` / merge `b3c96a7` preserves an optional server pin in
  transcript result metadata. It does not derive a pin in the consumer.
- App `b3d9658e` provides the dormant retained-source helper that reads exact
  new/prior pins and refuses a returned resource whose pin does not match.
  Existing dormant capture tests cover the no-asset caption/review
  reconciliation boundary and atomic refusal behavior.
- Current App `projectTranscript.ts` and `dataProvider.ts` show that the
  ordinary repository boundary already returns the complete parsed resource;
  only the optional field policy and future host caller mapping are missing.

The initial-pin carrier investigation is deliberately not repeated here.

## Activation prerequisites

Before applying this proposal, the following must be true and explicitly
qualified:

1. Runtime's digest-bearing ordinary `Document` resource is in the released
   contract and active Runtime build (including list/get/create/update).
2. The App generated/runtime contract release is pinned to that resource shape;
   this proposal does not mutate generated files or widen private017.
3. The Agent public successor exposes the exact result pin needed by the
   producer/read boundary, and the existing retained-read helper is connected
   to the authorized Runtime client.
4. The native gate is explicitly enabled only after the retained new/prior
   reads and atomic caption/review refusal tests pass. Until then, ordinary
   snapshot association and the existing writer remain authoritative.
5. A prior pin is available through the already-agreed carrier for replacement;
   no new carrier is invented by this proposal.

## Offline validation

One private copy of the App was made under `/tmp`, patched with the proposed
resource field/mapper, and removed after the run. Dependencies remained the
shared read-only App install; Vitest used a private cache directory.

Exact command:

```sh
./node_modules/.bin/vitest run --config vitest.proposal.config.ts --no-file-parallelism
```

Result: 1 test file passed, 2 tests passed, exit 0. The tests covered:

- missing digest accepted for old resources, valid digest preserved, malformed
  digest refused;
- exact `document_id` + `version` + server `content_digest` preserved through
  repository list/get/create/update, with no content hashing.

The live App suite, browser journeys, localhost/live sockets, full suite, and
native `transcript.associate` were not run because this task is an unapplied
proposal and explicitly excludes those runs.

## Limitations

This report does not prove a live Runtime/App wire exchange, public native
proposal admission, initial-pin recovery, or the future outbox integration.
Those remain activation work after the prerequisites above are satisfied.
