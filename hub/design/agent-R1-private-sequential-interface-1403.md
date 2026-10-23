# R1 private sequential execution carrier (Agent 1403)

Agent implementation owner: `agt-R1-private-sequential-proof-sol-1403`, based on
`851439d95647820815e69b4d7163e179540f28db`. Runtime owns verification and the
request-scoped port implementation. No public request, PreparedCommit, generated
schema/client, or accepted-history continuation change.

## Exact call and custody

Add one private method to `runtime_protocol.timeline_commit_port.RequestCommitPort`
(and its private Protocol):

```python
def capture_sequential_execution(self, capture: dict) -> None: ...
```

Agent `RuntimeCommitService.commit(context, port)` calls it immediately before
the existing `port.preview(prepared)` / `port.accept(prepared)`, once per candidate
head attempt. Its return is ignored; it must raise on invalid proof. The port
must detach and retain the capture on this request instance, authenticate it
against its own context/captured closures/history, and join it to the EXACT
prepared candidate during preview/accept. Prepared fields alone confer no
authority. A stale attempt's capture must not authorize the next candidate.

The complete JSON shape (all keys required) is:

```text
capture = {
  "schema_version": 1,
  "context": CommitContext,  # exact provider context, including request,
      # invocation, idempotency_key, request_hash, realm_id, publisher
  "original": Execution,
  "landing": Execution,
  "replay_bindings": [ReplayBinding, ...],
  "prepared_digest": Digest  # Agent canonical _digest(entire prepared)
}
Execution = {
  "evaluated_head": {"revision_id": str, "publication_id": str},
  "commands": [CommandBoundary, ...],
  "records": CommitRecords  # full prepared_records, including undo_steps
}
CommandBoundary = {
  "boundary": {
    "base_revision_id": str, "base_publication_id": str,
    "evaluated_head": HeadPin, "step_id": str,
    "command_ordinal": int, "phase": "input"
  },
  "input": CanonicalDocument,
  "output": CanonicalDocument
}
ReplayBinding = {
  "command_ordinal": int,
  "kind": "patch" | "read",
  "change_ordinal": int,             # patch only
  "ref": str, "path": [str, ...],   # read only
  "phase": "input" | "batch-read", # read only
  "source": ReplaySource
}
ReplaySource = str | {
  "step_id": str, "source": ReplaySource,
  "owner": str, "owners": [str, ...]
}
```

`CommitContext`, `CanonicalDocument`, `CommitRecords`, `Digest`, and `HeadPin`
are existing Runtime shapes, not new caller inputs. `records.commands` includes
the full generated recorder: commands, ordinal, reads, selections, writes,
derived_writes, bindings, created, dependencies. `records.steps` includes full
id/label/intent/tags/command_ordinals/patch/reads/dependencies. In particular
doc.patch bindings retain change ordinal and exact before state;
commit.read retains phase and declared read; commit.materialization retains
physical_ref/revision_id/content_digest/owner/complete owners, successor,
edge_before/edge_after, step_id and boundary. Input/output canonical documents
provide successor exact revision/digest and complete closure images, including
intermediate command boundaries, not merely final bytes.

Example map entry for command 1 consuming command 0's materialized internal:

```json
{"command_ordinal":1,"kind":"patch","change_ordinal":0,"source":{"step_id":"first","source":"internal-revision:base-internal","owner":"occurrence:o/shot","owners":["occurrence:o/shot"]}}
```

This map is serialized from actual `rebase_patch` output, never derived from a
submitted claim. Agent captures original and landing boundaries inside existing
`CommitPatch.before/after/finish`, then serializes their generated plans in
`_commit_preview.py`; `commit.py` supplies exact context, base/current head,
replay map and prepared digest. Original evaluated head is the submitted base
pair; landing is the current observed pair. Original/landing boundary arrays
are ordinal ordered, with one entry per executed command, including explicit
step read boundaries. Ordinary ABI and non-staged paths remain usable on old
ports. A moved-head staged physical input requiring this proof fails closed
with `sequential_proof_unavailable` if the method is absent.

## Runtime verification required (Runtime owner)

Authenticate full context against the port's own context, request hash and
source-history; input 0 against its captured base/head; every later input against
preceding command output and actual recorded effects. Validate original sequence
against base plus preceding commands, landing sequence against current head plus
preceding landed commands. Recompute image digests; verify request command/step
and change ordinal, exact reads/patch-before, owner and complete owner set,
managed edges, dependencies/effects and unique source-to-landing correspondence.
Bind prepared_digest to actual prepared (all metadata included).

Reject missing/forged/different-request/ordinal/step/owner/digest/map proof,
future/self/ambiguous/cyclic/foreign/stale lineage, ABA and order/selection
changes, without writes. Do not treat the original unlanded alias as an accepted
publication successor; do not rewrite submitted refs, retarget by bytes, or
trust ordinals alone. This carrier supplies proof for independent verification;
its presence alone does not authorize an alias.

Runtime 859 has no matching method. Original nine-case qualification remains
held until a Runtime owner publishes an exact verifier pin. Agent source and
capture tests will be reported independently; no merge request is authorized.
