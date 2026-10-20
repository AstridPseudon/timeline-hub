# WC7 owned outbox integrity review — APPROVE

Reviewed `tl/agt-m2-wc7-owned-move-outbox` commit `dfb4748a` / tree
`0c68c122` against `f82da322`, limited to the five changed paths in that
delta. I found no concrete data-loss or retry-integrity counterexample.

## Findings

- **Ownership/isolation:** `AttachedCheckout.publish()` requires an explicitly
  supplied outbox path, rejects `force`, `restructure`, and a foreign client,
  and `_state()` rechecks realm, actor, project, and timeline scope. Thus a
  default/global or unrelated outbox is held and not discovered or consumed.
- **Bounded intent:** publication accepts exactly one pending `clip.move`
  whose selector is parent-scoped. Occurrence-scoped, ambiguous, and mixed
  batches remain held; detached checkout publication remains held through the
  unchanged detached path.
- **Atomic sealing:** under the outbox lock, the rationale is added before the
  existing `_flush()` write creates and persists the flight containing the
  exact serialized body, original base IDs, command guards, idempotency key,
  and fence. The request is persisted before transport.
- **Lost-ACK retry:** restart reopens the same explicit outbox. `_flight_body()`
  validates the stored body, command prefix, base IDs, scope, dry-run mode, and
  supplied key; mismatch is refused without replacement. `publish()` also
  refuses a changed non-empty retry rationale. No capture/rebase refresh is
  performed on retry.
- **Post-acceptance:** the existing acknowledgement path advances the outbox
  base to the accepted revision/publication and removes only the sent prefix;
  the attached checkout reloads from that state. The existing guarded undo path
  remains available.

## Evidence

Local focused regression run:

```text
PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_owned_move_publish.py
5 passed in 2.60s
git diff --check
passed
```

The supplied qualified HTTP gate report for the unchanged three Runtime cases
records `3 passed in 6.21s`, including disjoint rebase/reload/undo, lost-ACK
restart with exact request identity, and unrelated global-outbox non-consumption.
I did not rerun the HTTP/service or any full suite, per the task instructions.

This approval is only for bounded attached-checkout WC7 publication. Broader
detached WC7 behavior and AG01 remain open and are not certified here.
