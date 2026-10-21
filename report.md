# RT02/RT03 original film-reference scope correction

## Result

The prior `rt-m2-reference-original-visibility-equivalence` witness was not
the original film positive. It called `create_project_reference`, which is
RK01 project-catalog CRUD. The actual RT02/RT03 film case is the retired
timeline-scoped writer:

```text
tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting
```

The reference half of that strict-xfailed test calls:

```text
POST /v1/timelines/exact-timeline/references
{"reference_id":"exact-reference","object_id":"object-digest","role":"source"}
Idempotency-Key: exact-reference-key
```

The relevant RT03 refusal controls remain separate:

```text
tests/test_timeline_reference_authority.py::test_service_reference_writers_refuse_before_lookup_or_replay
tests/test_timeline_reference_authority.py::test_http_timeline_reference_writers_refuse_without_writes
```

RT02 is the direct FILM writer row; RT03 is the direct TIMELINE reference
writer row. RK01 catalog positives do not close either row.

## Fresh original-film witness

I extracted the untouched pre-retirement Main implementation at
`80973d34` into a disposable `/tmp` tree and ran `RuntimeService` directly on
an own ephemeral realm. No Agent fixture, project object ingest, generation,
SQL fabrication, or current product source change was used.

The probe created a project and empty `exact-timeline`, then called only the
historical `RuntimeService.create_reference("exact-timeline", reference,
idempotency_key="exact-reference-key")` with the exact body above. Before and
after state was:

| | Before | After |
|---|---:|---:|
| timeline version | 1 | 1 |
| visible `shots` | `[]` | `[]` |
| visible `references` | `[]` | `[exact-reference/object-digest/source]` |
| `timeline_shots` rows | 0 | 0 |
| `timeline_references` rows | 0 | 1 |
| `project_documents` rows | 0 | 0 |
| `parent_composition_heads` rows | 0 | 0 |

The writer therefore creates one film reference row and its reference/history
projection, but no shot, occurrence, clip, composition document, or
publication head. The object string was deliberately never ingested or
registered; the call still succeeded and durably stored `role == "source"`.

After closing and reopening the same realm, the probe also passed all original
reference obligations:

- same body and key replayed the identical result;
- changed `role` under the original key returned 409
  (`idempotency key was already used with different input`);
- changed `role` under a different key returned 409
  (`reference already exists`), with no overwrite;
- the stored role remained `source`.

## Exact source and authority classification

At historical Main `80973d34`:

- `runtime_protocol/service.py` `create_reference` validates only a non-empty
  `reference_id`, a non-empty string `object_id`, and an existing timeline;
  then it replays/records the request and inserts `timeline_references` plus
  `timeline_reference_state`.
- `runtime_protocol/server.py` dispatches the original HTTP writer at
  `POST /v1/timelines/{timeline_id}/references` to that method and requires
  the idempotency key.
- There is no project-catalog lookup, media ownership check, CAS lookup,
  generation/variant selection, or five-field managed media tuple in this
  original positive.

Current Main retains the route shape but `RuntimeService.create_reference`
now immediately calls `_require_timeline_command` (`runtime_protocol/service.py`
around lines 4194-4197), so the current route is a visible retired-writer
boundary, not a successful replacement.

## Agent handoff

The existing occurrence-local provenance carrier may remain the agreed scope,
but the exact original case exposes a concrete missing authority path: its
accepted source is an opaque raw `object_id`, with no occurrence/asset registry
or managed-generation tuple. Agent must not create a visible occurrence or
clip merely to encode the reference, guess source identity from catalog CRUD,
or require an invented generation five-tuple that Main never required.

The original strict positive must remain OPEN until a peer-agreed native
carrier and Runtime projection preserve exact `reference_id`, `role: "source"`,
restart replay, changed-payload refusal, occupied-identity refusal, and
durable success. No command, DTO, endpoint, schema, or generation is proposed
by this report.

## Evidence

- Pass — historical Main direct-service own-realm probe against `80973d34`:
  empty-film before/after, arbitrary raw `object_id`, restart replay, changed
  payload 409, occupied identity 409, and durable source role.
- Command shape: `git archive 80973d34 | tar -x -C "$probe_root"`, then from
  that extracted tree
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$probe_root/tests:$probe_root" /home/user/work/venv-runtime/bin/python -`
  with the inline own-realm probe described above. Result: exit 0 and all
  assertions passed.
- Pass — `git diff --check` on this worker tree.
- Pass — source inspection of the historical HTTP route and
  `RuntimeService.create_reference` implementation described above.
- No full, broad target, socket/browser/renderer test, owner film, public pin,
  generation, product/schema/test-assertion change, or current positive claim.
