# RT03: film-reference witness against untouched Runtime Main

Date: 2026-10-21 UTC

## Result

The exact current Runtime Main is
`b535646faaad2f8ae7968dfe0f4fa3057f960264` (`fix(windows): fence realm
storage and escape SQLite paths`). The immutable detached checkout used for
the witness was `/home/user/work/wt/rt-pin-b535646f`, at that exact SHA.

Untouched Main still has the old direct timeline-reference writer. In normal
authenticated API use it:

- accepts an unowned opaque `object_id` (unsafe input);
- accepts the equivalent project-owned raw CAS object;
- creates the reference on an empty timeline without placing a shot or
  changing the timeline's `shots` projection;
- durably replays the exact result after a daemon restart;
- rejects changed payload under the same idempotency key with HTTP 409; and
- rejects reuse of an occupied `reference_id` under a different key with HTTP
  409.

This means the prior `80973d34` witness behavior is reproducible on current
Main, but it is not a safe current-Main contract. The current integration
branch's `RetiredRouteError` behavior must not be attributed to untouched Main.
No refusal classification is applicable for unowned placeholders on this Main
SHA. No product change was made.

## Exact source identity

Compared only the timeline-scoped writer and route:

- `runtime_protocol/service.py:4233-4258`,
  `RuntimeService.create_reference`, decorated with `_durable_mutation`.
  It validates only object-body shape, non-empty string `reference_id` and
  `object_id`, and timeline existence. It hashes the timeline plus body for
  replay, uses `timeline.reference.create` / `timeline.references`, inserts
  directly into `timeline_references` and `timeline_reference_state`, maps
  SQLite identity failure to `ConflictError`, records timeline revisions, and
  returns the resource. There is no project-object ownership/CAS lookup.
  Its exact extracted method body matches the historical `80973d34` body
  (SHA-256 `8c32a3c2ff41c2cbb9d476ad1c07692f56b2744250bb113126d67e5e7854c923`).
- `runtime_protocol/server.py:430-436` handles
  `POST /v1/timelines/{timeline_id}/references`, requires authenticated
  `projects:write` and `Idempotency-Key`, and dispatches to that service
  method with HTTP 201.
- There is no dedicated `create_reference` store method on this Main. The
  service writes the store connection directly. The relevant store schema is
  `runtime_protocol/canonical_schema.py:121-124` and `:163-165`; the store's
  column declarations are `runtime_protocol/store.py:226-227`.
- `create_project_reference` remains a separate catalog API at
  `runtime_protocol/service.py:3521`; it was not substituted for the film
  witness.

## Normal-API witness

The central test used the detached Main source and a fresh `RealmStore` realm:

```text
request-test rt-m2-reference-current-main-witness-validation targeted --files 'witness_current_main_reference.py'
wait-test rt-m2-reference-current-main-witness-validation-targeted-1021001906-30555
=> 1 passed in 1.48s
```

The temporary witness imported Runtime and the generated client from the
detached pin, created one project and an empty timeline, then performed:

1. `GET /v1/projects/{project}/timelines/empty-film`: `shots=[]`,
   `references=[]`.
2. `POST /v1/timelines/empty-film/references` with
   `object_id=not-a-cas-object`: accepted; reference appears in the timeline;
   `shots` remains `[]`.
3. Normal project object ingestion of the bytes `project-owned raw CAS bytes`
   (digest `sha256:1e3443814259d42e4742167f3fac3a54cf37573ded6ec936935b3821d95288f`),
   followed by the same reference POST shape: accepted; `shots` remains `[]`.
4. Daemon stop/start using the same realm, exact retry of step 2: result is
   equal to the original.
5. Same key with `role=target`: HTTP 409.
6. Different key with the already occupied `opaque-reference` identity:
   HTTP 409; no overwrite; final `shots=[]` and two references.

The direct local attempt was blocked before execution by this sandbox's
localhost socket policy (`PermissionError: [Errno 1] Operation not permitted`),
so the central result above is the only counted live-door evidence. No broad
matrix, full, browser, renderer, owner-data, or product run was performed.
