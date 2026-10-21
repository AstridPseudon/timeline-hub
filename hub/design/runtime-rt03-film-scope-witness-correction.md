# Runtime RT03 film-scope witness correction

Date: 2026-10-21

The prior `rt-m2-reference-original-visibility-equivalence` witness used
`create_project_reference` and therefore proved only RK01 catalog CRUD. It is
not evidence for the RT02/RT03 film positive.

The exact original positive is
`tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`
(strict xfail, lines 81-124). Its reference call is the original
timeline-scoped `POST /v1/timelines/exact-timeline/references` with
`{"reference_id":"exact-reference","object_id":"object-digest","role":"source"}`.
The direct-writer controls remain
`test_service_reference_writers_refuse_before_lookup_or_replay` and
`test_http_timeline_reference_writers_refuse_without_writes` in
`tests/test_timeline_reference_authority.py`.

Fresh own-realm evidence against untouched pre-retirement Main `80973d34`
called only `RuntimeService.create_reference` on an empty timeline. It
accepted an un-ingested opaque `object-digest`; before/after had zero
`timeline_shots`, zero project documents, zero parent composition heads, and
no occurrence/clip. Only one `timeline_references` row/projection was added.
After restart, exact-key replay passed; changed payload returned 409; a
different key could not overwrite the occupied identity (409); durable role
remained `source`.

Historical source inspection shows `create_reference` required only a
non-empty `reference_id`, non-empty string `object_id`, and an existing
timeline. It did not require project catalog ownership, CAS lookup, or a
managed generation/variant five-tuple. The current route is retired and must
remain a separate refusal control.

Agent peer request: preserve this raw-object capability without creating a
visible occurrence/clip, catalog substitution, source-identity guess, or
invented generation tuple. No new command/DTO/endpoint/schema is proposed;
the original strict positive remains OPEN pending peer agreement on the
existing occurrence-local carrier's raw-object authority path.
