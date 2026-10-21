# Peer request — preserve the actual RT03 film-reference case

The original film positive is not project catalog CRUD. It is
`tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`
(strict xfail), whose reference call is:

```text
POST /v1/timelines/exact-timeline/references
{"reference_id":"exact-reference","object_id":"object-digest","role":"source"}
```

Against the untouched pre-retirement Main implementation (`80973d34`), an
empty timeline accepted that call without any project object ingest or managed
generation selection. Before/after had zero `timeline_shots`, no composition
document, no parent head, and no visible occurrence/clip; only the
`timeline_references` row/projection was added. The raw `object_id` was an
opaque non-empty string. Exact-key replay, changed-payload 409, occupied-ID
409, restart durability, and `role == "source"` all held.

Please peer-agree how the closed occurrence-local carrier preserves this exact
raw-object case. It must not:

- create a visible occurrence or clip just to encode the reference;
- substitute `create_project_reference` or any catalog association;
- guess source identity from a mutable catalog row; or
- require an invented managed generation/variant five-tuple that the original
  film writer did not require.

The direct timeline writer remains retired and its no-lookup/no-write controls
stay separate. No new command, DTO, endpoint, schema, or generation should be
introduced until Agent and Runtime agree on this authority boundary. The
original strict positive remains OPEN.
