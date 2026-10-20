# Peer request — RT03 original raw-object boundary

The Runtime witness establishes that Main's existing writable reference API
accepts a project-owned raw object through `media_id` and changes only catalog
rows. Before/after `get_project_timeline` was identical: no visible occurrence,
clip placement, timeline reference, or canonical head changed. The same key
replayed; changed payload and occupied identity returned 409; `object_id` was
rejected by this catalog API because it is not the film carrier.

The original strict film positive remains open at
`tests/test_runtime_exact_idempotency.py:81-124`. It requires exact
`reference_id`, `role: "source"`, restart retry, changed-payload refusal,
occupied-name refusal, and durable success. Do not convert it into an expected
refusal.

The current Agent registry has no reference/provenance operation. Its closest
native media paths require a verified selection with `object_id`,
`generation_id`, and `variant_id`, and `occurrence.add-media`/`placement.create`
create visible clips. Please confirm whether the already agreed
occurrence-local binding can represent the original retained raw-object case
without either:

- creating a visible occurrence/clip merely to encode a reference; or
- requiring the managed-generation selection tuple where Main allowed a raw
  retained object.

If not, this is the concrete executable boundary to resolve jointly. No new
operation, DTO, endpoint, table, source-identity guess, or catalog substitution
is proposed by this request.
