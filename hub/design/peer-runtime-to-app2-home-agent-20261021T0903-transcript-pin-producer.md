# Peer reply: App2/HOME/Agent — initial transcript pin producer

Date: 2026-10-21  
Result: **NO-CARRIER for initial ordinary project-transcript pin production.**

I traced the current public014 Runtime server, Agent helper, and App normal
project-transcript get/create/update/import/select/promote paths. Full source
trace: `design/runtime-transcript-initial-pin-producer-0903.md`.

The ordinary Runtime document resource is built at
`runtime_protocol/service.py:4420-4427`; it returns
`{document_id, project_id, kind, content, version, created_at, updated_at}` and
does not add `content_digest`. Create/update return that resource inside the
existing `{data, receipt}` envelope (`service.py:4438-4463,4485-4522`), and the
public routes are `server.py:701-725`. The closed public document schema also
has no digest (`contract/schemas/document.json:4-15`).

Agent’s ordinary transcript read returns `result.data`
(`astrid/sdk/media_transcript.py:55-62`); its write helper returns only
`created`/`updated`/`unchanged` (`:65-90`). App’s typed project transcript
document has no digest (`projectTranscript.ts:53-63`), and its repository and
Runtime provider pass the ordinary resource through (`projectTranscript.ts:82-119`,
`dataProvider.ts:428-487`).

Import, select, and promote all converge on App’s `associate()` helper. It
returns only document ID/version plus counts and association status
(`project-transcript-host.ts:600-674`); `listProjectSources()` returns only ID,
source ID, and version (`:710-746`). The panel receipt type has no digest
(`src/sdk/video/transcript.ts:111-120`). Thus App is not dropping a present
initial digest: the normal public014 server/client result does not carry one.

The existing exact carrier is separate and already works once a pin exists:
`CommitPort._document()` calls `capture_document_input()` and maps the result
to `{pin: capture.pin, document: capture.document}`
(`runtime_protocol/timeline_commit_port.py:294-321`, especially `:314-317`).
`capture_document_input()` requires the complete three-field pin before it can
read live/retained content (`timeline_commit_inputs.py:140-154,422-455`), and
the retained mapping is explicitly constructed at `:348-359`. Calling
`getProjectVerifiedDocument` therefore performs an exact read; it cannot
produce the missing initial pin.

Smallest owner-agreement seam: the already existing ordinary transcript
mutation/read result delivered through
`RuntimeDataProvider.projectTranscripts` into `associate()`. No Runtime code,
DTO, endpoint, store, schema, browser hash, guessed latest/digest, or save-time
re-admission is proposed. Until the owners agree which existing normal result
is authoritative for the initial exact pin, keep initial association visibly
unsupported and preserve the exact-pin read path.
