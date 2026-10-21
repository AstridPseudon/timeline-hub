# WC8 retained mixed-sheet independent review

Result: **APPROVE** the exact retained-mixed Agent candidate for the bounded
data-safety question. The review finds no loss of the documented mixed
text+duration positive and no retained-context fallback that can silently
mutate or lose the original intent.

## Exact source

- Candidate branch: `tl/rt-m2-wc8-retained-mixed-text-duration-0707`
- Candidate commit: `8abeae34414d9399b5d9d94150ba1f28519c89d7`
- Candidate tree: `a986c13718d94287ace384823c3fb5c0f4693552`
- Parent/base: `355522d5cfec20ab6dfb9363b4c3dd2025b8889b`
  (`tl/rt-m2-wc8-text-current-forward-0648`)
- Candidate diff: exactly two paths, `21` product-line changes and `41`
  test-line additions; no lock, schema, generated, pin, or Runtime files.

Changed paths and final file digests:

```text
3d3916ce33cf492e4173edaa35e60673ecce454a78aff5a8b334b5652e0c29d  astrid/sdk/timeline_sheet.py
829efe3eee7af36761a6ca48179e1b9da07de56149342ec4cf2a725eb6c6532e  tests/sdk/test_timeline_sheet_native.py
```

## Decision and safety boundary

The base implementation already supports the requested mixed positive. In the
base `_duration_sheet`, a row changing only literal `text` and static `for`
passes the semantic comparison after translating the duration to `hold` and
restoring the source-only fields, so `NativeSheet.preview` receives both
existing commands in order. The new test at
`tests/sdk/test_timeline_sheet_native.py:92-112` proves the same behavior on
the candidate as one retained pending batch:

```text
clip.set hold=2.0
clip.set-params text="CHANGED"
```

It also asserts the original retained bundle and
`{"revision_id":"r0","publication_id":"pub0"}` basis remain unchanged,
the Runtime mock receives no send, and the target row plus untouched sibling
retain the intended values. This is preservation, not a new migration claim.

The product delta changes only unsupported retained outcomes from `None` to
`SheetError` in `astrid/sdk/timeline_sheet.py:866-923`. This is necessary at
the explicit retained-target boundary: `_stage_sheet` calls the translator
before it writes `pending` or `edited` state (`astrid/sdk/timeline/checkout.py:
561-598`). Returning `None` would enter `apply_sheet`'s legacy
`_apply_parsed` fallback (`timeline_sheet.py:843-855`), changing the local
draft without a captured native command, original request identity, or
durable Runtime outbox representation. The new refusal preserves the draft
and outbox instead of allowing that false partial success.

The refusal is bounded. `_stage_sheet` still returns `None` when no retained
session exists (`checkout.py:566-568`), so the ordinary detached local
grammar, `merge_sheet`, and `Checkout.save` path remains live. The unchanged
local positive `test_detached_static_duration_keeps_the_original_local_grammar`
and the broader `tests/sdk/test_timeline_sheet.py` grammar tests passed.

## Checks made

- Structure/order: changed row-key membership or count refuses before staging.
- Stable identity: every changed retained row requires its existing binding;
  missing bindings refuse.
- Unsupported timing/shape: null/absent duration, non-static/non-`am-type`
  clips, `on`/`until`, and unsupported rows refuse. Explicit native
  presence/clear semantics are not guessed by this detached translator.
- Literal text: the existing JSON token replacement remains literal and
  callback-based; the prior `c723cbbd8ee51dde0a507cefd5a61ff62c957107`
  independent approval covers escaped backslashes, newlines, quotes,
  non-ASCII, and empty strings. That evidence was reused, not replayed.
- No partial state: the new regression at
  `tests/sdk/test_timeline_sheet_native.py:115-130` changes duration and text
  while also changing unsupported `size`; it expects `SheetError` and asserts
  the in-memory bundle, outbox bytes, original `hold`, original text, and
  send-call list are unchanged.
- Retained basis and refs: the unchanged duration neighbor covers export,
  reload, original basis, stable binding, exact pending intent, lost-ACK
  retry, same-row conflict draft retention, disjoint rebase, and guarded
  inverse/redo. The existing HTTP evidence `20600` (literal text) and `27413`
  (retained duration/current Runtime) was reused as directed and not replayed.

## Live callers and version scope

No live caller changed. The affected call chain is the existing detached
bridge `apply_sheet` -> `checkout._stage_sheet` -> `_duration_sheet`; the
change is limited to calls where the outbox contains an authenticated,
verified retained sheet target. No retained artifact schema, commit DTO,
Runtime route, generated client, lock, or pin changed. The normal local
caller remains on the existing legacy grammar, and the supported retained
mixed text/static-duration case remains on the existing NativeSheet command
path.

Whole WC8 remains open; this review approves only this two-file retained mixed
slice and does not claim deletion of the remaining legacy consumers.

## Evidence limits

Direct targeted command on the candidate:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_sheet_native.py tests/sdk/test_timeline_sheet.py
```

Result: **88 passed in 7.81s**. `git diff --check` passed.

No HTTP, full, browser, render, installation, or live-socket run was made by
this review, per the task. Prior c723/20600/27413 evidence is explicitly
carried rather than relabeled as a new run.
