# BLOCK — Runtime c9 visibility receipt-provenance review

Date: 2026-10-20 UTC  
Candidate: `c9deaa5` (`ca1f1b6` .. `c9deaa5`)  
Scope: independent review of the new security/data-safety receipt-provenance delta only; no product edits.

## Decision

**BLOCK.** The pre-replay gate fixes the previously reported current-target
legacy receipt replay, but it does not positively identify a well-formed new
visibility event. Any JSON object payload without `target_version` is accepted,
including corrupt `{}` facts.

## Concrete finding

`runtime_protocol/service.py:3922` accepts a receipt when all of the following
hold:

- the first `event_ids_json` entry resolves to a timeline event for this
  timeline;
- its kind is `timeline.recovered`; and
- its decoded payload is any `dict` without `target_version`.

That is weaker than the requested positive provenance check. A corrupt event
payload such as `{}` passes the predicate and reaches `_command_replay`, which
returns the stored result as if it were a current visibility receipt. The
focused probe below injected only an existing ledger receipt and event helper,
then retried the exact request:

```text
PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python - <<'PY' ...
```

Result:

```text
CORRUPT_EVENT_REPLAYED False timeline.recover
NO_WRITE True
```

The no-write result does not make this safe: the operation returns stale or
untrustworthy receipt data instead of the required 410 refusal with
`reason=timeline_restore_required` and `replacement=timeline.restore`.

## Branch review

- No-receipt absent and current-target requests proceed through the existing
  visibility-only mutation path; the new guard is before ordinary replay.
- No-receipt non-current-target requests refuse with the existing
  `timeline.restore` guidance.
- Exact genuine new visibility receipts replay after a later catalog-version
  advance; the added test covers this and checks no write.
- Original legacy film recover receipts carrying `target_version` refuse before
  replay; the added current-target regression covers this and checks status,
  replacement guidance, and no write.
- Missing event evidence and malformed JSON/IDs fall through to refusal, but a
  syntactically valid corrupt object is incorrectly accepted as shown above.

## Source/current compatibility and diff audit

- Current tree: `c9deaa5`; reviewed source is
  `runtime_protocol/service.py`, with tests in
  `tests/test_timeline_legacy_authority.py`.
- The existing `POST /v1/timelines/{timeline_id}/recover` shape is retained.
  No new DTO, table, endpoint, event kind, or stored marker was added; the
  implementation uses the existing command ledger and timeline event.
- The c9 test change adds focused assertions; it does not delete or weaken
  prior assertions. The new tests cover current-target legacy evidence,
  missing event evidence, and genuine replay after catalog advance, but not a
  corrupt object payload.
- `git diff --check ca1f1b6 c9deaa5`: passed.

## Test evidence

- Candidate evidence in the supplied provenance-fix report:
  `env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_runtime_domains.py tests/test_timeline_legacy_authority.py`
  — **62 passed, 3 xfailed**. I did not rerun the 65-test/provider suite per
  the review instruction.
- Independent focused corrupt-event probe: **replayed incorrectly**, with
  `NO_WRITE True` as recorded above.
- No full suite, broad actual-provider/publication suite, or new API test was
  run.

## Required next step

Keep the existing-event-only design, but make the event proof structurally
positive: reject malformed payloads and mismatched project/version facts (and
any other malformed receipt/event linkage) before `_command_replay`, returning
the existing `timeline.restore` refusal. Add one focused regression for a
corrupt object payload, then repeat this review.
