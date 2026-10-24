Implemented F-authoring-ABA in two allowed files:

- `native_occurrence_media_commands.py`: coalesces identical scoped track observations within the write-free same-alias validation loop.
- `test_occurrence_media_binding_identity.py`: adds consumer, production-emitter and Runtime authority regressions.

Every consumer remains validated and read. Targets, effects, ordering and command boundaries remain intact. `_recording.py` and the original authoring test file are unchanged, including all 52 assertions in the original live test.

Actual provider-generated original and landing packets from a bounded fixture control contained duplicate `media.track` bindings: physical `internal-revision:internal-1`, revision `internal-1`, path `["tracks","id:picture"]`, owners `["occurrence:occ-a/shot"]`, command 1, step `edit`, input boundary, base `parent-1/bootstrap`. Both captured digest `sha256:f579c1ef3548804d91bdaedcd7acdca9af674baf2f458b74bc6606ffd7cce502`.

These were generated packets, **not packets observed from the original live test**. Exact-base execution failed with `sequential source binding is ambiguous`; repaired execution passed Runtime authentication. Complete packet/prepared comparisons differed only by the duplicate removals and resulting prepared digest.

The production chain is confirmed: publish → emitter → capture helper → `_swap` → `_clip` → recorder → private capture → Runtime authentication. Runtime authentication source is byte-identical to reviewed `8ea0766f`.

Validation used `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPATH="$PWD:/home/user/work/runtime"`:

- `python -m pytest -q -p no:cacheprovider tests/timeline/test_occurrence_media_binding_identity.py tests/editing_conformance/test_recipe_occurrence_media.py` — **87 passed**.
- `python -m pytest -q -p no:cacheprovider tests/timeline/test_authoring_media.py -k 'not real_runtime'` — **74 passed, 2 deselected**.
- Exact-base source overlay, two new regressions — **2 failed**, demonstrating RED.
- `ruff check --no-cache astrid/sdk/timeline/native_occurrence_media_commands.py astrid/sdk/timeline/_recording.py tests/timeline/test_occurrence_media_binding_identity.py` — passed.
- `mypy --follow-imports=silent` on both product files, with private caches — passed on current source and exact-base shadow source; no diagnostic identities.
- `git diff --check` and allowed-file/original-file identity checks — passed.

Synthetic corruption controls reject duplicate/conflicting bindings, foreign owners, different revisions, forged reads, reordered boundaries and ABA publication substitutions on both packet sides.

The original live test remains unrun: its reviewed `/home/user/work/wt/rt-pin-8ea0766f` environment is absent. The bounded authentication fixture omits shot mirrors; unchanged native fixtures separately verify their effects. Earlier broader controls encountered intermediate-image validation failures before reaching this duplicate guard.

Agent should qualify its managed Runtime environment, then submit the original node once through `bin/request-test … targeted --files 'tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba'`.

Commit message and `DONE` written. No Git writes, dependency changes or full suites.