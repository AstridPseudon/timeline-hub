# A3 shared physical-image fork carrier — Agent answer

**workerreport: PASS — existing carrier found; A3 shared family remains OPEN.**

Date: 2026-10-23 04:18Z  
Agent SHA: `f894c3c9dda25ab03527eeb7f52da5da31d627c1` (`tl/agt-A3-shared-fork-carrier-0418`)  
Producer tuple: unchanged/frozen (`normald106` / Runtime `34e`).  
Scope: read-only source answer; no product code, schema, DTO, pin, or route changes.

## Existing executable carrier

The current registered semantic operation is `occurrence.duplicate`, not a new
fork name:

```python
from astrid.sdk.timeline.native_occurrence_duplicate import (
    capture_occurrence_duplicate,
)

fork_command = capture_occurrence_duplicate(
    bundle,
    "occurrence:" + selected_occurrence_id,
    new_occurrence_id,
    new_shot_id,
)
```

For the bounded witness (`selected_occurrence_id="occ-0"`,
`new_occurrence_id="occ-copy"`, `new_shot_id="shot-copy"`), the executable
command shape is:

```json
{
  "schema_version": 1,
  "op": "occurrence.duplicate",
  "version": "1",
  "select": "occurrence:occ-0",
  "args": {
    "occurrence_id": "occ-copy",
    "shot_id": "shot-copy"
  },
  "intent": {"ownership": "occurrence"}
}
```

After native capture/recording, the command has these authoritative claims:

```json
{
  "created": ["shot:shot-copy", "occurrence:occ-copy"],
  "expect": {
    "shot:shot-copy::": {"state": "absent"},
    "occurrence:occ-copy::": {"state": "absent"}
  },
  "authorship": {
    "shot:shot-copy::": "direct",
    "occurrence:occ-copy::": "direct"
  },
  "bindings": {
    "collection.owner:collection.clips": "occurrence:occ-0",
    "collection.owner:collection.tracks": "occurrence:occ-0",
    "duplicate.owner": "occurrence:occ-0"
  }
}
```

The recorded created rows are exactly:

```json
[
  {"ref": "shot:shot-copy", "kind": "shot", "owner": null},
  {"ref": "occurrence:occ-copy", "kind": "occurrence", "owner": "parent"}
]
```

The operation is registered in `commands.operations()` with
`OccurrenceDuplicateArgs`, `occurrence_duplicate`, `OCCURRENCE_INTENT`, and
`singleton=True`. Its production execution path is
`RuntimeCommitService.commit()` → `commands.execute()` → that operation
registry, so the carrier is not test-only. The capture helper is at the same
module's `capture_occurrence_duplicate()`.

## Read and ownership shape

The operation is explicitly occurrence-owned (`intent.ownership="occurrence"`)
and requires a single `select` matching `occurrence:<id>`. Its authoritative
read sites are captured from the selected occurrence and its source; values are
the exact tagged states at capture time, not caller-supplied claims:

```text
parent                         [config, pinnedShotGroups]
occurrence:<source>            []
occurrence:<source>/shot      [shot_id]
occurrence:<source>/collection:clip   []  (collection shape)
occurrence:<source>            [occurrence_id]  (selection guard)
occurrence:<source>/collection:track  []  (collection shape)
occurrence:<source>/source    []  (complete internal payload)
occurrence:<source>/shot      [payload]  (complete shot payload)
shot:<new-shot>                []  (absent allocation guard)
occurrence:<new-occurrence>   []  (absent allocation guard)
```

The two selection records retain the exact source clip/track members and order.
The handler also checks: no legacy `pinnedShotGroups`; source and destination
identities differ; copied item IDs do not collide with existing allocations;
and `create_entity()` validates the shot/occurrence root allocation and
records ownership.

## Shared-image witness

The bounded probe used the existing native provider on a document where both
`occ-0` and `occ-1` pointed to `shot_revision_id="shot-1"`, and `shot-1`
pointed to the same physical `internal-1`. It produced:

```text
before: occ-0 -> shot-1 -> internal-1
        occ-1 -> shot-1 -> internal-1
after:  occ-0 -> shot-1 -> internal-1
        occ-1 -> shot-1 -> internal-1
        occ-copy -> fresh shot revision -> fresh internal revision
```

The old shared `internal-1` remained reachable/retained. The new roots were
`shot:shot-copy` and `occurrence:occ-copy`; the generated revisions were
`authoring-shot-revision-*` and `authoring-timeline-revision-*`. A later sibling
edit remains isolated from the copied occurrence in the existing conformance
witness.

The normal generation dependency is already present in
`compile_authoring_candidate()`: `authoring_shot_id != source_shot_id` forces a
fresh internal revision and shot revision, with the new child timeline ID set
to the parent timeline ID. This is normal generation, not a new operation or
caller-controlled pin. `_commit_patch.materializations()` records authenticated
same-occurrence pin turnover; a new-root duplicate is an allocation/fork and
does not need to masquerade as a continuation of the old shared root.

## Limits / handoff

`occurrence.add-media` and `occurrence.swap-media` remain separate registered
semantic commands. Their existing `_exclusive()` guard refuses a shared
authored placement, so the valid isolation sequence is: accepted
`occurrence.duplicate` first, reload its canonical landed closure, then issue
the existing media command against the new occurrence. This report does not
claim that App's selected ADD/SWAP caller already performs that sequence, nor
that a full shared ADD/SWAP acceptance has passed. No TS executor, HTTP body,
new op/DTO, or doc.patch edge mutation is proposed.

Files inspected:

- `astrid/sdk/timeline/commands.py` (operation registry)
- `astrid/sdk/timeline/native_occurrence_duplicate.py` (capture, handler, owner,
  allocation)
- `astrid/core/timeline/schema/edit-command.schema.json` (current v1 args and
  ownership schema)
- `astrid/core/timeline/authoring_bundle.py` (normal fork/materialization
  generation)
- `astrid/sdk/timeline/_recording.py` (reads, selections, bindings, created
  IDs)
- `astrid/sdk/timeline/_commit_patch.py` (authenticated materialization
  records)
- `astrid/sdk/timeline/native_occurrence_media_commands.py` (ADD/SWAP shared
  ownership guard)
- `astrid/sdk/timeline/commit.py` (production execute caller)
- `tests/editing_conformance/test_recipe_occurrence_duplicate.py`
- `tests/sdk/test_timeline_selected_param_authority.py`

No v2 request/reply fields were changed or dropped; the existing commit path
continues to carry the full contract request and `{data, receipt}` replies.

## Evidence

PASS — exact bounded native probe over the registered provider: shared source
fork generated fresh shot/internal revisions and preserved the shared source.

PASS — targeted existing witnesses:

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/python - <<'PY'
# install the test suite's in-process runtime_protocol ABI stubs, then:
pytest.main([
  '-q',
  'tests/editing_conformance/test_recipe_occurrence_duplicate.py::test_shared_source_copy_and_later_sibling_edit_are_isolated',
  'tests/sdk/test_timeline_selected_param_authority.py::test_occurrence_materialization_and_duplicate_have_explicit_identity_links',
])
PY
```

Result: `2 passed in 4.24s`.

An initial direct pytest collection without the in-process ABI stub failed
before test execution because this Agent-only environment has no installed
`runtime_protocol` module; the rerun above uses the existing test fixture's
ABI shape and did not alter product files.

No full suite, browser, HTTP, native14, or heavy/farm run was requested.
