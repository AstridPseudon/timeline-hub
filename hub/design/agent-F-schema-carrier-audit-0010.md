# Report

Read-only audit completed. No product, schema, test, generated, client, or pin files changed. `DONE` and commit message were written.

Findings:

- Agent schema and frozen Runtime 8ea schema are byte-identical: SHA-256 `d106dfe8…7d46357d`.
- Both retain 58 definitions and 30 explicit `EditCommand.allOf` branches.
- Runtime’s generic `EditCommand` carrier accepts qualified operation names with opaque finite-JSON `args`; only listed operations receive allOf-specific validation. Runtime does not reject the five unlisted operations at the envelope layer.
- Agent `validate_command()` performs the required internal registry lookup and validates each operation’s closed parameter schema.

All five current provider-registered operations can use the existing full v2 carrier:

| Operation | Internal closed args | Wire status |
|---|---|---|
| `occurrence.fork` | `{shot_id}` | Existing opaque carrier |
| `occurrence.place-shared` | `{occurrence_id, on}` | Existing opaque carrier |
| `timeline.duplicate` | `{source_ref, shots, occurrences}` | Existing opaque carrier |
| `timeline.restructure` | `{}` | Existing opaque carrier |
| `clip.duplicate-media` | `{id, old_media, media}` | Existing opaque carrier |

`timeline.restructure` is emitted by the real publisher caller and `clip.duplicate-media` has a real capture helper; neither is a transport consumer blocker.

The prior SDK report’s “genuine schema omission” conclusion was therefore too strong. The actual failure is stale Agent test inventory: the tests recognize only the earlier three provider-only operations, while current `operations()` contains 33 entries. Smallest test-only oracle adaptation: extend `PROVIDER_ONLY_ARGS` and `provider_only` with `timeline.restructure` and `clip.duplicate-media`, using their existing closed parameter schemas. Do not add a public tuple, regenerate the schema, change pins, or relax validation.

Commands/results:

- Source inspection with `sed`, `rg`, `git show`, `git log`, `git hash-object`, and JSON parsing: completed.
- Tests/pytest/client/provider/full suite: not run, per READONLY instruction.
- Worktree: clean.
- Retained full evidence remains unchanged and is not newly claimed: 17,159 passed, 262 failed, 5 errors, 4 skipped; exact sole full remains FAIL267.