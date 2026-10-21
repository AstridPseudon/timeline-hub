# Agent transcript persisted-bundle carrier fix

## Result

Fixed the reviewed carrier mismatch in the Agent source operation
`transcript.associate`.

The operation now uses only the existing persisted App/Main carrier:

```text
parent.config.bundle.transcriptReferences
parent.config.bundle.itemsBySchemaRef["astrid.transcript_segment/v1"]
```

This matches the normal App serializer's `parent_composition.config.bundle`
wire path and its persisted `itemsBySchemaRef` spelling. The rejected
prototype's parent-level `transcriptReferences` / `sourceItemsBySchemaRef`
spellings are not read, migrated, or written. If they are present, the command
refuses before any write, so they cannot become an independent authority.

When the normal bundle is absent, the handler records the existing nested
`config.bundle` container creation and then writes the two bounded leaves. It
does not replace the whole config or bundle. Existing source-item retention,
opaque fields, exact new/prior `DocumentPin` dependencies, stable
media/source/segment/word IDs and order, and atomic caption/review refusal are
unchanged.

No Runtime, App, generated client, activation, pin, or schema-floor changes
were made. The current schema and all published compatibility floors remain
untouched.

## Evidence

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_film_transcript_association.py
=> 6 passed in 0.83s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_film_transcript_association.py \
  tests/sdk/test_timeline_current_union_schema.py
=> 41 passed in 205.83s

/home/user/work/venv-agent/bin/ruff check \
  astrid/sdk/timeline/native_transcript_association.py \
  tests/editing_conformance/test_recipe_film_transcript_association.py
=> All checks passed

git diff --check
=> passed
```

The focused tests now use a real nested `config.bundle` fixture and cover
normal canonical serialization/reload, nested-carrier change, inverse and
redo, missing-bundle container creation, legacy parent-level refusal, exact
prior-pin retention, and atomic caption/review refusal.

No full suite, live/browser/socket suite, Runtime suite, or App Vitest run was
performed. App source and fixture paths were inspected as the authority; no
dependency installation was attempted.

## Decisions and follow-up

- Chose the fixed nested `config.bundle` path and persisted
  `itemsBySchemaRef` field because that is the normal App save/read wire shape.
- Refused legacy carrier shapes rather than adding migration or fallback
  authority, because the prototype was never an accepted stored-film format.
- Kept the caption/review reconciliation path atomic-refusal-only; its native
  positive follow-up remains open as required.
- Independent review after integration should re-run the native App positive
  save/read witness and Runtime accepted-history/restart retention witness.

