# App parent-track label handoff

Source branch: `tl/agt-m2-label-handoff`, based on `ceb2ab67` (`feat(timeline): add native track label and clip parameter commands`).

## Official shape

The existing native `track.set` operation already is the requested bounded
parent-track label handoff. It is a versioned, closed command:

```json
{
  "schema_version": 1,
  "op": "track.set",
  "version": "1",
  "select": "parent/track:picture",
  "args": {
    "values": {"label": "Picture é 🎬"},
    "clear": []
  }
}
```

`select` is the stable parent/track target identity. `values` accepts only the
string `label`; `clear` accepts only `label`; unknown argument keys, `null`,
missing required members, duplicate clear entries, and set/clear overlap are
refused by the closed schema. No new operation, rename operation, broad patch,
duplicate core, or group/root dependency is needed.

The authoritative Python capture is:

```python
capture_track_set(bundle, "parent/track:picture", values={"label": "Picture é 🎬"})
```

The full normalized command and full post-capture bundle are in
`tests/editing_conformance/fixtures/recipe_m2_app_track_label.json`. The
fixture uses the exact `parent-only` bundle from
`src/tools/video-editor/commands/fixtures/authoringBundle.json`, not a reduced
copy. `test_app_parent_track_label_capture_golden_is_exact_and_portable`
executes both the raw request and the authoritative native capture, then checks
the normalized command, after-bundle, inverse, opaque sibling, and exact source
pin closure.

## Semantics App must preserve

- absent label is distinct from `""` and from a non-empty string;
- `clear: ["label"]` removes the field, while setting `label: ""` stores an
  empty string;
- same-value writes remain recorded history edges and retain guarded inverse
  behaviour, including A-B-A refusal;
- parent label edits pass independently on the parent root and after a
  disjoint clip move; they do not depend on group/root work or staged data;
- missing, deleted, and duplicate track identities fail closed;
- opaque authored siblings and exact dependency pins survive unchanged.

The existing scalar conformance/provider coverage supplies the unchanged-write,
disjoint-move, same-path conflict, inverse/ABA, occurrence ownership, and
strict occurrence source-owner undo cases. The occurrence source-owner undo
case remains the known strict xfail and is separate from this parent-label
handoff.

## Status and boundary

This is a source-level Agent capture/portable-golden handoff for App native
browser parity. It is not a frozen Runtime wire pin, an official Runtime
artifact refresh, or actual browser proof. Runtime’s official artifact refresh
is still pending; App should consume the portable golden and retain its native
capture shape until that refresh. No product semantic or schema change was
made here.
