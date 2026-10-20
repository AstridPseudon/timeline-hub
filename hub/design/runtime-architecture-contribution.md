# Runtime architecture contribution

Basis: published Runtime `2c4ac180` and reviewed S2 source
`f7081c14`, identical tree `7ab412cc` (`workspace.v1`, contract `0.2.13`). Runtime is the neutral,
durable acceptance boundary; Agent (`sdk`) supplies timeline meaning.

## One path and startup

The only edit path is `POST /v1/projects/{project}/timelines/{timeline}/commit`.
The daemon loads the optional `astrid` semantic provider before publishing
readiness. The startup ABI is `astrid-v1`, interface 1, the installed contract
digest, and a synchronous two-argument `commit(context, port)` method. Neutral
Runtime never imports Agent and returns unavailable for semantic commits when no
provider is mounted. The authenticated Runtime actor is the publisher; route,
body, project, timeline, invocation path, and idempotency key must agree.

Commit is ledger-first at the boundary: exact `(scope, idempotency key,
request hash)` replay is resolved before provider work, and a changed payload
under a used key is refused. Acceptance then holds one SQLite transaction:
recheck authority, base ancestry and current head; validate the provider’s
candidate; persist the immutable closure, publication/history event, head,
input links and producer checkpoint; and return a `CommittedMutation` receipt.
The provider cannot claim acceptance without that receipt. A retry returns the
original result; no renderer is involved.

## Exact semantic contract

The request contains API version, project/timeline identity, base revision and
publication pins, an `EditCommand` batch, and optional dry-run/source/label/
rationale/group metadata. Agent executes the deterministic commands and returns
a prepared candidate. Its closure includes the parent, shot and internal
timeline revisions plus the media and DocumentPin manifest. The request-bound
port permits only exact declared reads: head/history, revision/shot closure,
selected media, text/narration selections, transcript/config/project-pack
documents and objects, and a settled producer attempt. Every captured value is
re-read before acceptance.

The recorder is part of the accepted meaning, not a diff: per command it keeps
writes (including unchanged values), reads, selections, bindings, created IDs,
dependencies and derived writes, plus undo/restore metadata. Runtime validates
that recorder, closure, manifest and `id_map` agree before publication and
stores the accepted input pins. Agent owns command semantics, rebase, timing
and inverse construction; Runtime owns the port, authority checks, exact reads,
atomic publication, ledger/history and durable retry identity.

Undo is a new guarded reversing edit. Restore is likewise a new commit and must
be the sole command: it names an immutable historical revision while supplying
the current head revision/publication pair. Runtime verifies ancestry, closure
integrity and the unchanged current head, then records `restored_from`; it never
rewinds history or bypasses the current-head guard.

## Producers, pins and preview boundary

A producer authoring-proposal task writes immutable CAS output. A requester
commits that proposal through a leading `producer.guard` whose pin binds task, settled attempt,
executor, fence, Runtime epoch, admitted project/timeline/base pair and proposal
digest. Runtime verifies the exact JSON proposal, its commands and rationale,
output provenance, current attempt and one-shot consumption. Acceptance records
that authority and may create a separately pinned render handoff at the
accepted revision. Generation/variant records and media selections remain
Runtime-owned; a timeline command receives only verified immutable IDs/pins.

`dry_run` is semantic preview only: the same closure, guards and destination
checks run, but no ledger, history, head, input link or producer checkpoint is
written and the response has `receipt: null`. Runtime compares the provider’s
preview with its own validated candidate. Capture certification is a separate
boundary: a stored capture is authoritative only when the paired provider
projection and exact authoring preview agree; otherwise it remains CAS-only.
Neither commit preview nor capture certification claims Composition pixels,
audio, or renderer availability.

## Actual open gaps

- Capture provider pairing is not a neutral/native Runtime capability; the
  current certification hook still depends on the mounted provider’s
  `project_capture` method.
- Native text and native group semantics are not closed end to end. Runtime has
  exact text-object/binding checks and occurrence/shot guards, but not proof
  that all native text/group producers emit the canonical closure and recorder.
- Consumer migration is still open: every App/SDK writer must use this `/v1`
  route, with legacy/fallback writers rejected or removed and the journey
  proven across retry, rebase and restore.

## References and ownership

- `runtime_protocol/daemon.py:225-248` — Runtime manager: startup/provider readiness.
- `runtime_protocol/timeline_commit_provider.py:55-93` — Runtime manager: provider ABI.
- `runtime_protocol/server.py:294-319` — Runtime manager: `/v1` auth and route.
- `runtime_protocol/service.py:2336-2456` — Runtime manager: request context and dispatch.
- `runtime_protocol/timeline_commit_port.py:183-491` — Runtime manager: closure, pins, recorder/input checks, preview/accept boundary.
- `runtime_protocol/timeline_commit_store.py:636-701` — Runtime manager: preview and atomic ledger/publication.
- `runtime_protocol/timeline_commit_producer.py:224-285` — Runtime manager: proposal authority and settled pins.
- `runtime_protocol/capture_validation.py:65-150` — Runtime + Viewing owners: capture certification; Composition owns pixels.
