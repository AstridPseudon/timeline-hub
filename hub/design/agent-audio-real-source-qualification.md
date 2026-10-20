# Agent M2 audio real-source qualification

## Exact source

The qualification adds `tests/editing_conformance/test_commit_runtime_parent_media.py`.
Its `tiny_wav()` helper creates a valid 8 kHz mono PCM WAV with 2,000 frames. The
existing main settlement fixture is used unchanged as the admission boundary:
`test_generation_publish_v1_settlement._fixture`, `_settle`, and `_output`.
The normal private generation settles three managed `audio/wav` outputs with
`duration_seconds: 0.25`; the test obtains the exact five-field selections from
`get_project_media_selection`, then sends the normal Agent provider
`clip.add-media` command.

The producer row is deliberately the main audio shape: `clipType: "media"`,
`track: "voiceover"`, `from: 0`, `to: 0.25`, and `hold: 0.25`. The setup creates
that explicit audio track through `capture_track_create`. The test also reads
the settled CAS bytes as a WAV, reloads Runtime, retries the exact request,
then performs guarded undo and redo. It does not add a schema, operation,
DTO, proposal API, import path, SQL write, or metadata override.

## Runtime and selection authority

Runtime's `runtime_protocol/timeline_commit_port.py:79-86` recursively walks
all dictionaries and lists with `objects()`. `RequestCommitPort.__init__` at
`:124` stores those objects in `__declared`; `selected_media()` at `:267-274`
requires exact dictionary membership and then reconstructs the verified record
from managed generation/variant/object authority. The Agent provider currently
calls `selected_media` only for media-bearing operation arguments at
`astrid/sdk/timeline/commit.py:876-887`.

## Duration and historical carrier investigation

Agent trim already handles a missing registry duration without a new wire field.
`astrid/sdk/timeline/_trim_commands.py:25-48` requires an exact matching
Runtime-verified media record, checks MIME family and size, and uses the server
carried `duration_seconds`. It records that complete verified record inside the
existing accepted dependency at `:123-127` as
`dependencies[].pin.source` plus `dependencies[].pin.verified_media.selection`.
The existing pure test `tests/editing_conformance/test_recipe_m2_clip_trim.py:71-82`
proves the carrier and inverse/replay semantics.

The historical pre-cut film is a separate counterexample. Its original
`music-bed` registry entry is `type: audio` with an object identity but no
duration, and its object has no managed generation/variant tuple. Therefore no
valid five-field `MediaSelection` exists for that old object and Runtime
`selected_media` cannot establish authority for it. This is the distinct
unregistered-object gap; fabricating generation/catalog adoption would violate
the M2 boundary.

## Remaining gap and smallest peer proposal

The real managed authoring capability is qualified by the new integration test.
The historical original-audio trim journey remains unqualified. The smallest
Runtime/Agent coordination proposal is to have the Agent provider, only for a
`clip.trim` record whose existing `trim.source` dependency contains an exact
five-field `verified_media.selection`, collect that declared selection and call
the actual `port.selected_media` before semantic execution. Runtime already
accepts recursively declared selections; no DTO or public wire change is
needed. The provider must rebuild duration/MIME/size from that server response,
never trust forwarded metadata, and guard the original asset/object, the whole
selection, source range, speed, and frame/interior rounding. This proposal is
not implemented here because the exact carrier/API decision belongs with the
Runtime peer. It also cannot solve the old `music-bed` case until that object
has a real managed tuple.
