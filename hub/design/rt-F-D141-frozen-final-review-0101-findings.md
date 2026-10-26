# D141 frozen ordinary Farm review

Verdict: `PASS_SOURCE`; readiness: `NOT_READY`.

## Scope result

The actual 0055 candidate (`1b709a796`, tree `040c1772`) was compared with
ordinary 0032 (`ba8bec724`, tree `dfd5cbf8`). The diff has exactly four paths:

- `receive-farm.sh`: D141 comment, frozen Agent/Runtime/App commit/tree pins,
  and the Agent runtime-lock blob/SHA;
- `README.md` and `commands.md`: source-custody and frozen-tuple prose;
- `test_recipe.py`: current tuple assertions, explicit absence of obsolete
  `41ad`/`f103`/`569` receiver pins, and current lock assertions.

No `receipts.py`, D139a maker/requester/checker, D131 registration/provision
logic, ownership, ordinary route logic, policy, C0 schema/client, D134, or
D124 selector source changed. Old tuple IDs occur in `test_recipe.py` only as
negative assertions; they are absent from production receiver source.

## Findings, one pass

`D140-APPLICABILITY-010` remains closed from independent0049: ordinary D139a
installed-schema admission is the default, and `FARM_REQUIRED=1` retains the
strict special branch.

`D140-FINAL-TUPLE-011` is closed. Receiver lines 15–22 bind the exact current
Agent `28e56cac`/`2ebe2ddf`, Runtime `6a011d58`/`ac5b8627`, App
`867cb273`/`2b44a46c`, and Composition `635f4de0`/`5ab5191a`. Lines 116–145
check exact clean checkout, object, tree, and origin; lines 353–360 check the
lock, client, schema, launcher, and suite blobs/SHA-256 values.

`D141-FROZEN-LOCK-012` passes. The Agent lock blob is `2d4d12a1…` with SHA
`0cc3ba73…`, declares Runtime source `6a011d58`, has 15 entries, and every
entry's source hash matches the exact Runtime tree. The C0 commit schema SHA
`3654ca3c…` is byte-identical between Runtime `f103` and `6a011`; no request,
reply, authority, or wire shape changed.

`D141-PRESERVATION-013` passes. The existing ordinary 97-test result is reused
as directed. This review reran only four bounded controls: current/old tuple
binding, no-request check-only census, import-failure stop ordering, and the
exact unfiltered 22-root selector.

`D141-VENUE-014` remains open as an external input status. The source-only
check-only run supplied exact clean local tuple checkouts and returned 66
checks, 24 PASS and 42 non-PASS, `NOT_READY`, exit 1, with every side-effect
flag false. It did not create a child, queue, import census, control, Store,
package, service, or core result. This is not a source failure.

## Source custody notes

The expected received kit is the existing `make-child-venv` source at
`fd83c9e2017f75fb0d76a2d633d4a63aed090df37c4d7417b03152e7a4fc22b5`, 111171
bytes, mode 0755. That is an authenticated expected operational source, not a
received Farm kit receipt; the venue path is still unbound. The historical
`4c/ab1e` 1,146-row census remains supporting-only. No fictional Farm receipt,
current census, child, or body result was invented.

The named remote frozen-reference refs were read for context, but their local
tips are not the authority here: the task's exact commit/tree tuple and the
clean exact checkouts are the binding. No source checkout was retargeted or
modified.

