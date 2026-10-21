# Gate1 native frontend anchor carrier fix

## Scope

Private Agent normal14 source on the existing `786ee...`/fresh-gate base, with
the existing Runtime 3dca pin and normal client 95bd pin. No Runtime, schema,
generated-client, lockfile, public13, renderer, or browser changes.

## Carrier path

The CLI commands-file path now reaches the same `TimelineSession` native
capture boundary as Python. `TimelineSession._bundle(state, extra_commands)`
hydrates every `clip.anchor` choice through the existing
`materialize_transcript_inputs` helper, which reads and validates the exact
DocumentPin through the authenticated verified-document client before local
capture. Pending commands and the new batch are both included; no current-head
refresh or alternate word/source selection is introduced.

NativeSheet uses the same existing carrier shape in its existing `on=` cell:
`{field, declaration, choice}`. Its preview translates the parsed carrier with
`capture_anchor`, after exact source hydration when a session is supplied. Its
commit comparison ignores only read-only `source_mapping.pinned_documents`, as
the attached checkout already does; authored rows, opaque values, basis and
outbox guards remain compared exactly. Existing anchored clips export the same
carrier, while malformed carriers remain explicit errors.

Actual callers changed:

- `TimelineSession.queue_many` and `commit_many` now pass their batch through
  the existing source-input hydration boundary.
- `NativeSheet.preview`/`apply` now parse and commit the existing anchor carrier.
- The fresh Gate1 test activates CLI and sheet and supplies the exact carrier
  in the sheet cell; its base guard is advanced to this task's inherited
  fresh-gate test commit (`3d2eb...`).

## Verification

- Local neighbors with the 3dca Runtime pin:
  `tests/sdk/test_timeline_sheet_native.py tests/sdk/test_timeline_sync.py
  tests/editing_conformance/test_native_word_anchor.py` — **110 passed,
  54 deselected**.
- Central named `gate1-fresh-word-transcript-frontends` with Runtime 3dca:
  `test_fresh_word_transcript_frontends_exact_pin_roundtrip` — **3 passed in
  6.02s** (Python, CLI, sheet). The allow-listed named lane necessarily includes
  the Python control in addition to the two newly fixed frontend cases.

No full suite, browser, renderer, old seed, duplicate suite, or Python-only
qualification was run.
