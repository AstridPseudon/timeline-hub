# D98a command-source classification

Input: `handoff-rt-D98a-32278-safe-observations.jsonl`, three records, 29 paths
per record. All three records have the same path set.

## Classification

For every record, `commands[0..2].command.authorship`, `bindings`, `expect`,
`intent`, `reads`, `resolved`, and `selections` are recorder-added/normalized
fields. They are absent from the submitted raw envelope and present in the
authoritative Agent record. Verdict: **YES EXACT D82**. Owner: the D82 test
assertion boundary (submitted envelope versus recorded command); no product
validation or authority change.

The `commands[0].created[0..3]` differences are string IDs in the submitted
command versus `{ref, kind, owner}` record facts. `commands[1].command.created`
and `commands[1].created` are omitted/empty normalization. These are recorder
shape/enrichment differences only. Verdict: **YES EXACT D82** for the record
shape comparison. Owner: the recorded-command expectation boundary.

The complete 29-path set, applied independently to each of the three records,
is:

| path | class | source proof | verdict / owner |
|---|---|---|---|
| `commands[0].command.authorship` | absent→object recorder field | `Recording.finish(capture=True)` derives authorship from writes | YES EXACT D82 / expectation boundary |
| `commands[0].command.bindings` | absent→object recorder field | recorder emits binding claims | YES EXACT D82 / expectation boundary |
| `commands[0].command.expect` | absent→object recorder field | recorder derives input guards | YES EXACT D82 / expectation boundary |
| `commands[0].command.intent` | absent→object recorder field | registered operation supplies fixed intent | YES EXACT D82 / expectation boundary |
| `commands[0].command.reads` | absent→array recorder field | recorder captures reads | YES EXACT D82 / expectation boundary |
| `commands[0].command.resolved` | absent→array recorder field | registered singleton resolves its target | YES EXACT D82 / expectation boundary |
| `commands[0].command.selections` | absent→array recorder field | recorder captures membership/order | YES EXACT D82 / expectation boundary |
| `commands[0].created[0]` | string→`{ref,kind,owner}` record fact | `Recording.create*` appends typed facts | YES EXACT D82 / expectation boundary |
| `commands[0].created[1]` | string→`{ref,kind,owner}` record fact | same | YES EXACT D82 / expectation boundary |
| `commands[0].created[2]` | string→`{ref,kind,owner}` record fact | same | YES EXACT D82 / expectation boundary |
| `commands[0].created[3]` | string→`{ref,kind,owner}` record fact | same | YES EXACT D82 / expectation boundary |
| `commands[1].command.authorship` | absent→empty object recorder field | `Recording.finish` materializes the field shape | YES EXACT D82 / expectation boundary |
| `commands[1].command.bindings` | absent→empty object recorder field | same | YES EXACT D82 / expectation boundary |
| `commands[1].command.created` | omitted→empty array | command finalization copies record facts | YES EXACT D82 for shape / expectation boundary |
| `commands[1].command.expect` | absent→empty object recorder field | same | YES EXACT D82 / expectation boundary |
| `commands[1].command.intent` | absent→empty object recorder field | operation/restore finalization supplies intent | YES EXACT D82 / expectation boundary |
| `commands[1].command.reads` | absent→empty array recorder field | same | YES EXACT D82 / expectation boundary |
| `commands[1].command.resolved` | absent→empty array recorder field | same | YES EXACT D82 / expectation boundary |
| `commands[1].command.selections` | absent→empty array recorder field | same | YES EXACT D82 / expectation boundary |
| `commands[1].created` | omitted→empty record array | record schema always carries `created` facts | YES EXACT D82 / expectation boundary |
| `commands[2].command.authorship` | absent→object recorder field | recorder derives authorship | YES EXACT D82 / expectation boundary |
| `commands[2].command.bindings` | absent→object recorder field | recorder binding capture | YES EXACT D82 / expectation boundary |
| `commands[2].command.created` | omitted→two-ID command array | `Recording.finish` derives IDs; Runtime auth compares this field | **NO** / command producer; strict Runtime guard |
| `commands[2].command.expect` | absent→object recorder field | recorder derives input guards | YES EXACT D82 / expectation boundary |
| `commands[2].command.intent` | absent→object recorder field | registered operation intent | YES EXACT D82 / expectation boundary |
| `commands[2].command.reads` | absent→array recorder field | recorder read capture | YES EXACT D82 / expectation boundary |
| `commands[2].command.resolved` | absent→array recorder field | recorder target resolution | YES EXACT D82 / expectation boundary |
| `commands[2].command.selections` | absent→array recorder field | recorder selection capture | YES EXACT D82 / expectation boundary |
| `commands[2].created` | omitted→two typed record objects | `Recording.create*` emits typed facts | YES EXACT D82 for record shape / expectation boundary |

`commands[2].created` is also a record fact enrichment (submitted absent versus
two `{ref, kind, owner}` objects), so that comparison is **YES EXACT D82**.
However, `commands[2].command.created` is a distinct authoritative guard
input: submitted is absent while the recorded command contains two created
IDs. Verdict: **NO — not a D82-only test assertion**. Runtime
`timeline_commit_auth.validate_claims` compares `submitted.get("created", [])`
with `record["command"].get("created", [])` and rejects this mismatch unless
the authenticated inverse-restoration or track-create exception applies. The
safe packet does not establish either exception. The exact owner is the
command producer/caller that submitted ordinal 2 without its genuine created
claim; the Runtime guard must remain strict. Minimal repair is to submit the
complete command emitted by the genuine registered capture for that caller,
preserving its IDs and all other fields. No guessed field, guard relaxation,
or test-only expectation correction is applied.

## Call trace

`TimelineSession._flush` serializes `state["pending"]` into the
`commitTimeline` body (`astrid/sdk/timeline/sync.py:534-547`). Runtime loads
the registered `astrid.sdk.timeline.commit.create_runtime_commit_service`
provider (`runtime_protocol/timeline_commit_provider.py:70-89`), calls
`provider.commit` through `timeline_commit_execution.py:229-235`, and the
provider executes Agent `commands.execute` before producing
`records.commands` (`astrid/sdk/timeline/commit.py:1331-1335,
1421-1434`). Runtime then invokes `validate_claims(request, records)`;
`timeline_commit_auth.py:316-326` checks core fields and the `created` claim.

The Agent `Timeline._append` path intentionally keeps the caller commands in
`self._commands` (`astrid/sdk/timeline/commit_session.py:120-123`) while using
local `execute` only for preview/state. Replacing that with a locally derived
record would cross the genuine registered-capture boundary and is therefore
not a faithful repair under this task.

No product or test file was changed.
