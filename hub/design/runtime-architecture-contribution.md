# Runtime architecture contribution

## Current Main boundary

Runtime is the neutral, durable acceptance boundary; Agent (the `sdk`) supplies
timeline meaning. The only edit path is `POST
/v1/projects/{project}/timelines/{timeline}/commit`. There is no semantic side
route or gateway. At startup the daemon loads the optional `astrid` provider
before readiness and checks its `astrid-v1` ABI, interface, contract digest and
synchronous `commit(context, port)` method. Without that provider, neutral
Runtime stays usable but semantic commit is unavailable. The authenticated
Runtime actor remains the publisher, and route, body, project, timeline,
invocation path and idempotency key must agree.

Integration is Runtime `9d1c43c`, still the public 0.2.13 line; its published
producer and 75 artifacts remain unchanged. Corrected Main014 is the separate,
unpublished candidate `6e845a187684919c162b29568496c015bda1a591` (tree
`7f11d7e159d46a88a22111c414aa7bdf7b599d9d`), carrying Main health, service and
client changes with the frozen ordinary semantics (55 definitions and 29
operations, 76 generated artifacts). Future private392 and voiceover work are
not public capability or a consumer pin.

## Reads, custody and acceptance

The request supplies API version, project/timeline identity, base revision and
publication pins, and an `EditCommand` batch. The provider works through a
request-bound port that permits only exact declared reads: head/history,
pinned parent/shot/internal-timeline closure, selected media, text and
narration selections, transcript/config/project-pack documents and objects, and
a settled producer attempt. Captured values are re-read before acceptance.
Runtime retains the accepted immutable closure, media and Document/input pins,
recorder and `id_map`, publication/history edge, head and producer checkpoint;
the recorder preserves writes (including unchanged values), reads, selections,
bindings, created IDs, dependencies and derived writes. Agent owns command
semantics, rebase, timing and inverse construction; Runtime owns authority,
exact reads, atomic publication, history and retry identity.

Acceptance is ledger-first: exact `(scope, idempotency key, request hash)` replay
is resolved before provider work, and a changed payload under a used key is
refused. One transaction then rechecks authority, ancestry and head, validates
the candidate, persists closure and history, and returns the normal
`CommittedMutation` receipt. A retry returns the original result. Undo is a new
guarded reversing edit. Restore is a new sole-command commit naming an
immutable historical revision and guarding the current head/publication pair;
it records `restored_from` and never rewinds history.

## Boundaries and remaining adoption

History, selected-media reads and `dry_run` are revision-pinned advisory
surfaces. Composition, render and capture answer viewing questions separately;
they are not called by save and do not turn advisory findings into write
authority. Producers store immutable CAS output and proposals; only a settled,
guarded request may submit their commands through `/v1`.

The existing project-scoped reference/shot/text catalog, ordering and archive
operations remain a catalog boundary. They do not mutate accepted film state;
film placement, selection and timeline references remain guarded commands.
Main's existing door, store and catalog infrastructure is retained rather than
rewritten around this page.

The exact runnable command and result for corrected Main014 Gate 2 are in
[runtime-gate2-corrected014.md](runtime-gate2-corrected014.md).
The living deletion boundary is [deletion-ledger.runtime.md](deletion-ledger.runtime.md).
The remaining product prerequisite is coordinated App and Agent adoption of
the unpublished Main014 tuple, including removal or refusal of every legacy
writer and proof of retry, rebase and restore. This is not a serial-gate tail
or an M4-complete claim.
