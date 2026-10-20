# Selected PARAM: accepted selection authority (owner12:16)

The next selected-pack `clip.set-params.args.schema_source` is the exact
DocumentPin of the accepted effect that most recently established **this raw
target's element/params selection at the captured accepted publication**.
PARAM preserves that selection; it cannot choose another admitted pin.
`clip.set-element` is explicit reselection and may establish another pin even
when its `elementRef` write has identical before/after JSON. An ordinary PARAM
then records that same pin, including unchanged values, clear-only and empty
writes. No unique qualifying pin means visible refusal with the draft retained.
An empty or singleton manifest does not establish a selection.

This is the rule/fixture handoff, not a claim that enforcement is wired. The
native provider currently validates the caller's exact pin but does not compare
it with accepted selection authority. Two strict expected-failure probes keep
those missing behaviors visible without changing any passing behavior test.

## Existing association and order

For a direct single-target PARAM or element selection, require one consistent
triple in `HistoryEntry.records.commands[ordinal]`:

```text
command.select = R
command.args.schema_source = P
dependencies[key=params.schema, kind=source, policy=exact].pin = P
dependencies[key=params.snapshot, kind=entity, policy=exact].pin =
    {source:P, element:E, object:O}
bindings[key=params.element, policy=fixed].ref = R
bindings[key=params.element].dependencies = [params.schema, params.snapshot]
```

Require the complete DocumentPin `{document_id,version,content_digest}`, exact
element `{packId,id,kind,revision}`, and admission `snapshot_object` O. Resolve
P through `config_source(P)` / existing VerifiedDocument reads and O through
`document_object(P,O.object_id)`. Existing native admission validation checks
realm/project/pack, the unique admission, its immutable portable bytes and
descriptor. Neither element revision nor object/snapshot digest is P's digest.
A conflicting/duplicate/missing triple does not authorize a selection.

Scope is `(realm_id,project_id,timeline_id,owner,rawClipId)`, where owner is
`parent` or an explicit `occurrence:<id>`. Match the raw accepted element using
the existing `elementRef`/`element_ref` precedence. Never match display suffixes,
clip JSON equality, element revision alone, or another occurrence's equal clip.
Use the accepted closure's `source_mapping.placements` / `shots` and existing
`scalar.owner`, `scalar.target` / `scalar.images` when resolving occurrence
ownership. Main's verified compiler materialization (`State.matches` and its
exact `_authoring_shot_id` relationship) preserves identity; arbitrary source
replacement, reused raw IDs or a matching string prefix does not.

Order publications by their verified `previous:{publication_id,revision_id}`
chain ending at the captured HeadPin, then records by `ordinal` within each
publication. These are not timestamps, author order, project sequence numbers,
or the order of a manifest. Use scoped `history_entry`, `history` pagination and
`revision_closure`; check every page head, predecessor pair, cycle and scope.
An incomplete relevant suffix cannot prove which effect was most recent. A
newer unrelated record does not replace the target's association. A later
relevant legacy/root write without recoverable association stops resolution;
do not scan past it to resurrect an older pin. An earlier legacy/bootstrap edge
does not poison a later complete explicit selection.

## Effects other than a direct PARAM/element record

| Accepted effect | Authority for the resulting target |
| --- | --- |
| PARAM | Previous authority P must equal requested P; record the direct triple even for unchanged/clear-only/empty writes. Missing history cannot be repaired by supplying an arbitrary P to PARAM. |
| Explicit element reselection | Native-verify supplied P/E/O; direct triple establishes P even if authored JSON is unchanged. The admission producer may use its existing authenticated `resolve_admitted_element(...).binding` to choose this **new explicit** selection; never use that current binding to infer an old selection. |
| Birth / imported legacy clip | `created` and whole-row `writes` establish identity, not a pin. Missing source remains unavailable. A producer with an explicit admission selection records it using existing `clip.set-element` in the same birth batch (same E is allowed); no new `clip.add` argument is needed. |
| Occurrence duplicate | Use `duplicate.owner`, command `args.occurrence_id/shot_id`, `created`, and the exact copied internal clip identities to carry each source target's authority at the duplicate's input stage to the distinct new occurrence. Equal sibling content alone is insufficient. Missing source authority stays missing. A producer may append explicit `clip.set-element` records for each copied selected target using those inherited pins. |
| Inverse, including redo / deletion restoration | Follow existing `records.undo_of` and command `args.publications` to authenticated targets and their exact `previous` boundaries. Reverse their selection effects in the same stages as guarded authored writes: restore each affected target's **before-selection authority**, not the pin the inverse consumed. Recursing through an inverse target restores its input authority again. Check original inverse guards and relevant intervening selection changes; unresolved lineage refuses. An inverse of an unchanged reselection still reverses the selection effect. |
| Revision restore | `records.restored_from` is only `{revision_id,content_digest}`. Resolve that exact revision identity against accepted source publications preceding this restore, then resolve each target's authority there. Accept a pin only if all qualifying source publications resolve to one identical P and none is missing/ambiguous. Different P values (or missing history) leave future PARAM unavailable. Restore itself still restores the exact authored revision; it need not fail because a future PARAM lacks authority. |

Inverse dependencies `params.schema` / `params.snapshot` currently enumerate
inputs consumed to check the inverse; they lack `params.element` bindings and
can describe the reversed selection rather than the restored one. Do not take
their first/last dependency as the result's source. A whole-timeline inverse
uses its target's exact accepted **before** boundary, including inverse of a
restore; it does not choose a publication by equal revision bytes. Structural
delete/recreate boundaries and actual occurrence-source replacements must be
accounted for before inheriting a target association. Unknown producer shapes
refuse instead of inventing an association.

Renderer meaning remains determined by the revision's element ref and authored
params. P determines reproducible validation for a subsequent edit, not a new
render interpretation. Restore never gets a new publication selector DTO.

## Capture, rebase, retry, and the bounded implementation seam

Capture raw R/E, accepted HeadPin and P together. Hold them across reads and
retain the exact command/request/outbox retry identity across restart. A fresh
load resolves from that accepted history, never a browser cache. Exact retry
uses Runtime's existing idempotent result; it does not reselect a source. For a
new commit/rebase, resolve authority at the real command stage and again at the
accepted head: another target or track edit is disjoint; a change to this
target's selected P/E/source identity must conflict/refuse with draft kept.
If P/E returns to the same exact selection and ordinary value guards pass,
PLAN's equal-state ABA policy remains; do not add a new publication guard to
ordinary PARAM. Guarded inverse retains its stricter intervening-write rules.

**Runtime review before wiring:** no additional Runtime port operation is
needed. Existing `RuntimeCommitPort.history_entry(publication_id)`,
`history(through,after_publication_id,cursor,limit)`, `revision_closure(revision_id)`,
`config_source(pin)` and `document_object(pin,object_id)` contain the inputs.
The smallest additive Agent-internal helper has this shape:

```python
resolve_selected_param_source(port, *, realm_id: str, project_id: str,
                              timeline_id: str, through: HeadPin,
                              select: str) -> DocumentPin
```

It returns a pin or existing `CommandError` (`history_unavailable` for missing
lineage; `selection_changed` for a conflicting selection). Call it from the
provider's existing real-stage `_schema_resolver`; pass/compare its result to
the existing `_selected_schema` recorder, always resolving for selected PARAM
instead of the current changed-value shortcut. Within a batch, preceding
recorded effects supply the stage's selection. This helper is a proposed
internal seam, not implemented here and not a new history store/framework.

App already loads `TimelineCommandBasis`/HistoryEntry and captures raw identity.
Its existing authenticated provider needs complete relevant history through
that HeadPin plus the existing two exact VerifiedDocument/object reads. Use
the same rule and portable fixture to obtain P and pass the existing
`schema_source` field; native enforcement remains authoritative. A partial
history page is insufficient. Forward those reads through the existing session
client, as the prior App audit requests. No new endpoint, DTO field, browser
schema validator, accepted journal, table, manifest winner or local cache.

## Portable counterexample and executable evidence

`selected-param-original-pin-counterexample.json` in this directory contains
actual native record envelopes, two VerifiedDocument/object inputs, the common
input/output canonical documents and two cases:

```text
A: explicit select P1 -> PARAM seed9/P1 -> explicit select P2 (same E)
B: explicit select P2 -> PARAM seed9/P2 -> explicit select P1 (same E)
```

Both final **entire canonical documents** are equal, including revision IDs and
the two-pin manifest. The expected next sources differ: A=P2, B=P1. P1/P2 are
labels for exact pins, not document version numbers. Neither first/last sorted
manifest nor a canonical-only accessor can satisfy both. Explicit reselection
records an unchanged authored `elementRef` write. A repeated reselection after
both pins are retained can also leave the entire canonical document unchanged.

Repository probes: `tests/sdk/test_timeline_selected_param_authority.py` plus
the existing selected-schema/scalar suites. The portable fixture is generated
by `test_equal_json_opposite_pin_order_has_distinct_accepted_authority` under
pytest's private `tmp_path`; copy that JSON to this directory after a passing
run. It uses real admission/portable-snapshot/handler/recorder/compiler/provider
code with the existing in-memory DetachedRealm/DetachedPort and fake document,
media and build-verifier fixtures. Envelopes intentionally omit receipts and
their repeated results. This is portable diagnostic input, not authenticated
Runtime service evidence. Live custody, browser refusal/draft preservation,
Runtime idempotent retry/restart, and the proposed resolver are not qualified by
these tests. Strict xfails name the two enforcement gaps; no old test changed.
