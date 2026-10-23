# Runtime G5 source-authority review (0827)

## Disposition

**PASS for causal SOURCE DISPOSITION: authenticated source-child inputs are
available through the current Runtime request-private port.** This is separate
from the known unsupported behaviors: full source-timeline import into an empty
destination and creation of a second occurrence referring to a copied shot.
Those behaviors remain unsupported; this review did not rerun their failing
Agent bodies and does not weaken their positive assertions.

The earlier 0822 handoff's broad `FAIL for current cross-timeline source-copy
support` is too broad as a Runtime source-authority result. Its narrower claim
that the current Runtime cannot supply a complete source parent timeline for
full import is correct. Its proposed ownership must be corrected: PLAN §1 puts
semantic edits in the Python Agent provider. Runtime may own the authenticated
source-input/verification seam and destination acceptance, but must not become a
new semantic executor.

## Trees and evidence origins

- Runtime under review: `a5d4258312c979024865ee704da2d632ca5b2730`
  (`tl/integration`, also `tl/rt-G5-source-authority-0822`).
- Agent peer/current integration: `e49a6e76b3ab363e312c55b313714af1f845f54b`.
- Agent independent G5 gap review: `1660d817a4ea883072ce7529e771da2c54493fbf`,
  `design/agent-G5-gap-review-0806.md`. It records the two preserved positive
  failures and is read-only evidence here.
- Frozen R4 SDK reference: `11caf1d9de291d76f491cf69f7942606b7471d7a`
  (`origin/codex/handover-timeline-r4-20261019-candidate-sdk`).
- Frozen R4 Runtime reference: `31c7ac3a00f7a205f507bf5bd4d4625628d429bd`
  (`origin/codex/handover-timeline-r4-20261019-candidate-runtime`).

## Causal Runtime trace

1. `runtime_protocol/timeline_commit_provider.py:16-18,55-93` fixes the
   mounted ABI to provider `astrid-v1`, interface version 1, the current schema
   digest, and synchronous `commit(provider_context, port)`. With the `astrid`
   profile, `runtime_protocol/daemon.py:235-256` loads and registers that
   provider before readiness. Runtime does not interpret command meaning.

2. The authenticated HTTP route is
   `runtime_protocol/server.py:294-319`; it binds the route/body project and
   timeline IDs, idempotency key, authenticated publisher, and authorization
   callback. `runtime_protocol/timeline_commit_execution.py:69-115` creates a
   request-private port, calls the mounted provider, verifies the outcome, and
   refuses non-preview outcomes without durable receipts.

3. `RequestCommitPort` stores the destination request scope at
   `runtime_protocol/timeline_commit_port.py:103-125`. Its
   `revision_closure(revision_id)` at `:223-249` permits the exact base,
   observed/ancestral, or explicitly declared revision, then calls
   `TimelineCommitStore.revision_closure` with the request's destination
   `(project_id, timeline_id)`. This is an exact authenticated destination
   closure, not an arbitrary database read.

4. `RequestCommitPort.shot_closure(shot_id, revision_id)` at
   `runtime_protocol/timeline_commit_port.py:251-266` requires the exact pair
   to be present in declared request objects or a captured closure. It calls
   `TimelineCommitStore.shot_closure`. The store at
   `runtime_protocol/timeline_commit_store.py:541-572` verifies the immutable
   shot revision and internal revision digests and pin relationship, finds a
   unique accepted parent manifest containing that exact shot/revision, then
   verifies the source parent's closure with its real timeline ID. The returned
   authenticated child input contains the shot image, internal image, and the
   source closure's exact `media` and `documents` manifest entries.

5. The input seam is request-private and rechecked. `selected_media` at
   `timeline_commit_port.py:268-275` requires an exact declared selection and
   uses `MediaReads.selected`; the five-field selection is checked against the
   Runtime-managed generation/variant/object/catalog authority at
   `:686-722,788-888`. `config_source`/`transcript_source` at `:316-346` and
   `timeline_commit_inputs.py:422-455` require exact document pins and
   registered/retained input provenance. Before acceptance,
   `RequestCommitPort.validate` at `timeline_commit_port.py:409-465` compares
   every captured closure, shot, media, raw-media and document input again and
   rejects candidate manifest entries not captured through the port.

Therefore a registered Agent semantic provider can legitimately copy one
source child by declaring its exact `(shot_id, shot_revision_id)` and consuming
the returned child plus its media/document inputs. The Runtime does not accept
caller-forged media metadata or unverified source bytes. The generic forgery
test remains useful evidence of this boundary: it passed all 28 cases.

## Exact missing fields and scope limits

The child authority is not a complete source-timeline authority:

- `RuntimeCommitPort.revision_closure` accepts only one `revision_id`, and the
  current port resolves it in the destination request's timeline. There is no
  current port method accepting an exact source `timeline_id`, source parent
  `revision_id`, and source `publication_id` together.
- `TimelineCommitStore.shot_closure` internally discovers `p.timeline_id` and
  `p.id` at `:564-570`, but drops those parent identifiers from its return at
  `:571-572`. It returns no source publication pin or source occurrence row.
  It also does not let the caller select among source timeline/publication
  rights; uniqueness of the accepted parent manifest is the available guard.
- Consequently, `shot_closure` supplies the child payload/internal timeline and
  the source media/document manifest, but not the source parent payload fields:
  occurrence IDs and ordering, track/placement/duration/source-window fields,
  parent config, parent registry, parent clips, or the source parent revision /
  publication pair. Those fields are required to reproduce a complete source
  timeline, including repeated occurrence rows.
- The destination request does have an exact base revision/publication pair,
  destination head CAS, request hash/idempotency, provider-record
  authentication, and destination identity/allocation checks. Those facts do
  not grant rights to read a different source parent timeline.

This is the precise boundary behind the 0822 author handoff's full-import
failure. It is not evidence that Runtime lacks authenticated child media/source
inputs. A future full-import seam would need to authenticate an exact source
timeline/revision/publication (and return its complete closure) or otherwise
provide an equivalent verified source-parent capture. It must also preserve the
existing destination CAS, source/destination separation, manifest rechecks, and
allocation/managed-edge checks.

## Agent semantics versus Runtime authority

The current Agent registry in
`/home/user/work/agent/astrid/sdk/timeline/commands.py:29-96` registers
`occurrence.create`, `occurrence.duplicate`, `occurrence.fork`, media commands,
and `doc.patch`; it has no current full timeline source-import operation. The
current handlers show the separate known behavior:

- `native_occurrence_create.py:15-50` always creates both a new shot and a new
  occurrence.
- `native_occurrence_duplicate.py:11-55` copies one occurrence into a fresh
  shot and fresh occurrence.
- `native_occurrence_fork.py:23-43` changes one existing occurrence's shot
  link; it does not create a second occurrence around an already copied shot.

This is a missing registered Agent semantic, not proof that Runtime must
execute a new semantic command. The current command envelope permits finite
JSON `args` and an operation-shaped `op`:
`edit-command.schema.json:843-944` says unknown operations pass the envelope
but require an installed registered schema/handler. Thus a future Agent
semantic command can use the existing commit carrier; do not conflate that with
inventing a new Runtime wire schema. Runtime should only add/extend the
request-private authenticated source-parent input and verification seam if the
orchestrator approves it.

The frozen R4 SDK evidence is historical only. Its
`commit.py:_load_duplicate_source` at frozen candidate-sdk lines 490-508
accepted an exact source timeline/revision/publication ref through an older
`timeline.duplicate` path. That proves the former design's intended authority
shape, not current support. It does not authorize restoring the detached writer
or making Runtime a semantic executor.

## Known behavior disposition and preserved controls

The two original Agent positives remain unsupported in the current integration,
as recorded by `design/agent-G5-gap-review-0806.md`:

1. Empty-destination chapter-film duplication still lacks a complete source
   parent import and fails before acceptance at the Agent media/input boundary.
2. Repeated-shot copying still reaches `occurrence.create` for a second row and
   collides with the copied shot identity.

Those are not converted into refusals by this review. Required negative controls
remain: exact source pair/digest checks, foreign/outside/stale source rejection,
source/destination separation, forged media rejection, occupied-ID and
managed-edge rejection, ordering/sharing preservation, idempotency, undo, and
archive cleanup. The existing orchestrator decision remains
`agent-20261023T0816-G5-duplicate-authority.md`; this review creates no duplicate
escalation.

## Verification

Executed locally on Runtime tree `a5d425831` (not a central cached result and
not a full/duplicate suite):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_authentication.py::test_forged_provider_records_are_rejected_without_writes
28 passed in 5.54s
```

After the report-only documentation changes, `git diff --check` passed. Ruff
and Pyright were not applicable to this read-only review. No product code,
tests, generated clients, pins, branches, or integration refs were changed.

## Owner handback

Keep the causal source disposition **PASS** for authenticated source-child
inputs. Keep the broader full source-timeline duplication behavior **unsupported**
until the existing orchestrator decision resolves the source-parent authority
seam and Agent semantic registration. If approved, Runtime owns exact
source-timeline/revision/publication admission and revalidation plus destination
acceptance; Agent owns the semantic copy, field mapping, repeated-sharing
behavior, and provider-derived records. No Runtime semantic executor or second
escalation is warranted by this review.
