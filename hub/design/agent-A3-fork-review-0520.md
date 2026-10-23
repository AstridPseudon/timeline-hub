# R1/A3 D15 independent review — PASS

Reviewed Agent `dc00a764c0c0acc9f613261060b4e5552dd0c1cc` against
`9cf0fde2f57603813d81733ee8b0f7117ffd634c`. Source manifest matches the
reviewed tree exactly; source-set SHA256 is
`e7c96edb911f6a1d89fb218cc951fea6094ee350f2ab62cbf039f951239e6830`.

## Result

**PASS for Agent provider source and real RuntimeService acceptance.** The
mounted App path and shared-physical-source RuntimeService seed remain
unqualified and are explicitly not claimed here.

`occurrence.fork` is registered in the existing generic semantic carrier with
no schema/client/pin change. Exact callable shape:

```json
{
  "schema_version": 1,
  "op": "occurrence.fork",
  "version": "1",
  "select": "occurrence:<existing-id>",
  "args": {"shot_id": "<fresh-reserved-id>"},
  "intent": {"ownership": "occurrence"},
  "created": ["shot:<fresh-reserved-id>"]
}
```

The provider captures the selected occurrence/source, complete clip/track
membership and order, payload, and absent destination root. It binds the
authenticated physical source and owner, creates one shot (owner `null`), and
replaces only selected ownership. Count/order/timing/identity, siblings,
opaque/raw source fields, stale/ABA/retarget/surviving-consumer guards, and
native created-claim checks remain strict. Shared-shot and distinct-shot cases
sharing an internal source both preserve the sibling through fork then edit.
Unknown generic operations remain unsupported without a registry handler.

Inverse source recovery is restricted to `AcceptedRecords`/authenticated
history boundaries, never caller-provided images. Public `timeline.inverse`
undo and native redo's explicit recreated-shot `created` claim were exercised.
The pre-existing Runtime inverse-created equality defect from the 48d/peer-0507
handoff remains separate and is neither waived nor called fixed.

## Commands/results

- Targeted conformance/provider/duplicate/delete/undo/timing/validation/vendor/
  artifact lane: **244 passed in 18.16s**.
- Runtime integration with
  `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=.:/home/user/work/runtime`:
  **1 passed in 2.77s**.
- Runtime checkout is clean at `6a6e97506409719b9d3c54984268e7c93c026efa`,
  with reviewed `be5848e17fbf68100286114883f5820fe4755911` as ancestor and no
  intervening `runtime_protocol` production files.
- Scoped Ruff PASS; scoped mypy PASS (10 files); normal Ruff PASS 2149/2149;
  vendor lock and artifact manifest PASS; diff check PASS.
- Normal mypy baseline comparison was environment-limited: the available venv
  lacks YAML stubs and has a NumPy-stub Python-version syntax error. No budget
  or baseline changed; the author's unavailable private environment reported
  1914/1914.

No source edits, deletions, ref changes, shared dependency writes, sockets,
browsers, or full/heavy suites were used. Next required proof is App A2
outbox/mounted production wiring plus shared-physical-source Runtime coverage.
