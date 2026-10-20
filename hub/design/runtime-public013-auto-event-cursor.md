# Runtime public013 automatic event-cursor contract

Date: 2026-10-20  
Runtime source: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`  
App peer source: `693dc753f` (operation-bound readiness repair)

## Result

The normal Runtime producer already supplies the readiness primitive App needs.
The request is `GET /v1/events?limit=50&from=latest` through the existing
operation-bound transport. A valid HTTP 200 response is a page, not a
readiness signal by status alone. For `from=latest`, the page is deliberately
empty and carries a non-empty polling cursor:

```json
{
  "items": [],
  "next_cursor": "eyJrIjpbIjAiXSwibnVtZXJpYyI6dHJ1ZSwicyI6ImV2ZW50czoqIiwidiI6MX0"
}
```

The literal cursor above is the empty event-table case. It decodes to
`{"k":["0"],"numeric":true,"s":"events:*","v":1}`. If events already
exist, the same response shape contains the current newest matching event id
instead of `0`; App must retain the opaque returned string and must not decode
or manufacture it.

Polling that cursor before a new event is appended returns the same shape with
`items: []` and the same `next_cursor`. Once an event is appended, `items`
contains the ordered event objects and `next_cursor` advances. The cursor is
therefore the readiness/stream fence; the event list may legitimately be
empty at readiness.

## Exact public response contract

`GET /v1/events` is registered by `runtime_protocol/door.py:187` and served by
`runtime_protocol/server.py:1093-1096`. Its page body has exactly these top-
level fields:

```json
{"items": [], "next_cursor": "opaque-or-null"}
```

Each item is the closed `contract/schemas/event.json` object with these fields:

```json
{
  "event_id": "10",
  "sequence": 10,
  "cursor": "10",
  "event_type": "task.progress",
  "aggregate_type": "task",
  "aggregate_id": "task-id",
  "payload": {},
  "occurred_at": "2026-01-01T00:00:00Z"
}
```

The event item field values above are an illustration of the exact field
shapes; the page field names and item field set are not optional. The generated
client exposes this as `Page<Event>`, with `items` and `next_cursor` only:
`packages/typescript/src/generated.ts:60-62,251` and
`packages/python/astrid_runtime_client/generated.py:504-517,1351-1356`.

The `from=latest` request is exclusive with `cursor`; combining them is a
400. A cursor is scoped to the collection (`events:*` for App's global feed),
and a cursor from another collection is a 400. `limit` is an ordinary page
limit (1..200, default 50).

There is no public `has_more` field. `has_more` is only a local variable inside
`RuntimeService.events_page` used to decide whether a normal page needs a
continuation cursor (`runtime_protocol/service.py:8005-8014`). It is not a
wire promise and App must not wait for or inspect it.

## Initial stream, await, and cancellation

The producer is an immediate page operation, not a long-poll endpoint. The
service computes the newest matching event id and returns immediately for
`from=latest` (`runtime_protocol/service.py:7982-7986`). There is no Runtime
server-side await, timeout, cancellation token, or cancel endpoint associated
with this read. The generated clients expose a normal async Promise / Python
call; the request caller may use its ordinary transport cancellation, but no
additional Runtime event contract exists.

The App operation wrapper remains responsible for its local lifetime fence.
In the frozen App source, `AstridRuntimeClient.listEvents(cursor,
fromLatest)` maps `fromLatest=true` to the existing `from=latest` query
(`src/integrations/runtime/client.ts:780-783`). The operation host forwards
that read through the same operation transport and checks the binding before
and after each await (`src/integrations/runtime/operationHost.ts:176-196,
206-215`). Retirement therefore rejects a stale operation read after its
transport await; it does not make Runtime long-poll or cancel the HTTP request.

The task-event poller stops its local timers and marks its ambient readiness
promise resolved when inactive (`src/features/tasks/components/TasksPane/hooks/
useRuntimeTaskEvents.ts:124-154,170-198`). The operation-bound readiness path
also performs a direct `listEvents(undefined, true)` and must reject a page
whose `next_cursor` is empty (`.../useRuntimeTaskEvents.ts:227-240`). This is
the correct local admission fence. HTTP 200 alone is insufficient.

## Bounded evidence

Ran exactly one existing Runtime event test against the frozen source:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_cursor_pagination.py::test_events_latest_cursor_polls_forward_across_digit_boundary
```

Result: `1 passed in 0.72s`.

That test proves the relevant sequence: an empty `from=latest` page has a
cursor; an unchanged poll returns an empty page with the same cursor; a new
event is then returned and advances the cursor; the next event is also
observed; `from=latest` cannot be combined with a cursor. The source-level
response construction additionally establishes the exact field order and
cursor encoding above.

## App handoff and Runtime bug status

App can use the existing operation-bound call exactly as follows:

1. Call `operation.listEvents(undefined, true)`.
2. Await the Promise.
3. Require `page.next_cursor` to be a non-empty string; `page.items` may be
   empty.
4. Keep polling with that cursor. A repeated cursor with an empty item list is
   the normal no-new-event result, not a failure.
5. Let the existing operation retirement fence reject stale reads; do not
   invent `has_more`, a timeout-to-success path, or a new endpoint/field.

There is no executable Runtime counterexample here and no Runtime bug is
identified. The frozen Runtime source and the bounded test both provide the
required cursor for the exact `from=latest` producer. If App's captured
operation response is HTTP 200 with `next_cursor: null` or without the
`next_cursor` field, that is not the behavior of this producer and the next
diagnostic should preserve the exact request URL/query and response body at
the operation proxy boundary. It would not justify weakening readiness or
changing the public tuple.
