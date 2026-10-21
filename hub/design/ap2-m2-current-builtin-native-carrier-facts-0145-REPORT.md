# Current builtin native carrier fact

## Result

The current installed rendering pack does provide exact owner/id/kind/revision
facts in the generated Agent catalog, but it is not a no-pin authority for
`clip.set-element`.

One current builtin fact from Agent integration HEAD
`4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a` is:

```json
{
  "packId": "rendering",
  "id": "text-card",
  "kind": "effect",
  "revision": "sha256:6575848081267d8ac02b802f109dd8fedb4bddb94469b914190f83b2e73be56f"
}
```

The descriptor is in `astrid/packs/rendering/elements/catalog.ts`, generated
by `scripts/gen_element_catalog.py`, with `source: "pack:rendering"` and all
three renderability fields `supported`. The installed owner is defined by
`astrid/packs/rendering/pack.yaml` (`id: rendering`), and the element manifest
is `astrid/packs/rendering/rendering/elements/effects/text-card/element.yaml`.

## Native caller shapes

`clip.add` is a literal-row carrier. Its `ClipAddArgs.row` has the required
`id`, `clipType`, `track`, `at`, and `hold` fields but allows additional JSON;
`clip_add` does not inspect `elementRef` or add `schema_source`. Therefore this
shape is accepted and preserved exactly at clip birth, without a
`DocumentPin`:

```json
{
  "schema_version": 1,
  "op": "clip.add",
  "version": "1",
  "select": "parent",
  "args": {
    "row": {
      "id": "effect",
      "clipType": "text-card",
      "track": "picture",
      "at": 0,
      "hold": 2,
      "elementRef": {
        "packId": "rendering",
        "id": "text-card",
        "kind": "effect",
        "revision": "sha256:6575848081267d8ac02b802f109dd8fedb4bddb94469b914190f83b2e73be56f"
      }
    }
  },
  "intent": {}
}
```

This is preservation, not catalog validation: the native `clip.add` handler
does not prove that the caller's four values came from the installed catalog.
The catalog is the available trusted declaration; no handler-to-catalog
authority link was found.

`clip.set-element` has the corresponding exact ref shape, but a current
builtin ref necessarily has a truthy `packId`. The handler then calls
`_selected_schema`, which requires `args.schema_source`. The exact no-pin
caller shape is therefore refused:

```json
{
  "schema_version": 1,
  "op": "clip.set-element",
  "version": "1",
  "select": "parent/clip:effect",
  "args": {
    "elementRef": {
      "packId": "rendering",
      "id": "text-card",
      "kind": "effect",
      "revision": "sha256:6575848081267d8ac02b802f109dd8fedb4bddb94469b914190f83b2e73be56f"
    }
  }
}
```

Observed native refusal: `CommandError: selected project pack requires exact
schema_source` (`kind=invalid_edit_command`). This was a direct in-memory
probe of the current Agent `capture_clip_set_element`/`clip.set-element`
handler against an existing clip carrying the catalog descriptor.

The schema permits only the optional exact `DocumentPin` beside `elementRef`:
`{document_id, version, content_digest}`. With that pin, the current resolver
requires a verified `astrid.project-pack` document whose `content.pack_id`
matches the ref and whose admissions contain the exact id/kind/revision plus a
verified snapshot object. That is project-pack authority, not the installed
`pack:rendering` declaration. No supported no-pin `clip.set-element` carrier
exists in the pinned/current Agent code.

## HOME catalog scope

HOME's normal refresh is `scripts/astrid-landing/refresh-vendor.mjs`. It reads
the selected descriptors from the chosen Agent commit's generated
`astrid/packs/rendering/elements/catalog.ts`, selecting by `(packId, kind, id)`
and carrying the selected revision into `public-catalog.ts`. Thus a refresh
against the current Agent integration would supply a legitimate supported
descriptor; it does not create a project DocumentPin.

The checked-in HOME vendor is not that current descriptor: its lock is pinned
to Astrid commit `06dee36fbfa9d134a57b50536c045231e541b11e`, and its vendored
`text-card` and transition `fade` revisions differ from current Agent. No
refresh was performed.

## Verification

- Direct `clip.add` native probe: PASS; the exact `elementRef` was stored,
  `schema_source` was absent, and no pin was required.
- Direct `clip.set-element` native probe: PASS for the expected refusal; exact
  message was `selected project pack requires exact schema_source`.
- Read-only parser of current generated catalog: PASS; 45 descriptors, 10
  `pack:rendering` descriptors, all with supported preview/browser/worker
  renderability.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent python3 -B
  /home/user/work/agent/scripts/gen_element_catalog.py --check`: BLOCKED by
  the existing missing shared package
  `/home/user/work/agent/remotion/node_modules/@banodoco/timeline-composition/package.json`.
  No catalog refresh was attempted.
- No App production files were changed. No browser, full, localhost, live
  socket, or catalog-refresh suite was run.

## Smallest Agent peer question

For a current `pack:rendering` ref, is `clip.add`-only preservation intended,
or does an existing Agent installed-pack resolver already exist that
`clip.set-element` should use instead of the project `schema_source` path?

No decision was made beyond reporting this closed contract; no saved draft,
hosted SYSTEM revision, stale8e reference, or `builtin2a` value was used.
