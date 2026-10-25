# D118a independent core/privacy review facts

- Verdict: **FAIL** for the requested real-rebind behavior; candidate remains HELD.
- Candidate: `f3a6a3884d6b7c3190d83b70c76afee55ff8d592`, base `cf7b8d7c2b4cb980de1d873f0498784d5210d508`.
- Allowed diff is contained to `astrid/sdk/timeline/native_text_binding.py` and additive `tests/sdk/test_native_text_binding_authority_fields.py`.
- Candidate source preserves a complete existing `binding_id`, `head`, and `event_stream_id` for same-value captures; new births do not fabricate them. The existing `DERIVED_FIELDS` already contained `event_stream_id` at base. Runtime pin source validates/returns `event_stream_id` as part of the registered binding identity.
- Parent assertion reproduction: loading the exact base native module in memory and running the same two original authority nodes produced `1 failed, 1 passed`; failure was the expected `KeyError: 'binding_id'` assertion, not ImportError/setup.
- Candidate additive test: `4 passed in 1.15s`.
- Existing relevant native/spike/script unit nodes: `52 passed, 2 deselected` (only integration-lane nodes deselected).
- Genuine provider qualification on immutable Runtime `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, clean checkout `/home/user/work/wt/rt-pin-42aad0e9`:
  - Candidate exact script-pin/rebind node: **failed** in `native_text_binding.py:69` with `dependency_changed`, because the authenticated existing row's media pin differs from the requested rebind text.
  - Parent native module under the same genuine-provider node: `1 passed in 1.72s`.
- Therefore the candidate proves only unchanged descriptor preservation. It refuses the intended changed-text native rebind before Runtime commit, so it cannot prove Runtime-derived authority reaches the script consumer for real rebind.
- Privacy/source checks: no `_runtime_document` or `source_mapping` in production source; no emitter, auth-guard, route, schema, cache, or Runtime changes. The additive test only checks private-data absence on the command.

## Checks

- `PYTHONPATH=$PWD:/home/user/work/runtime ... pytest -q -o addopts= tests/sdk/test_native_text_binding_authority_fields.py` -> `4 passed in 1.15s`.
- `... pytest -q -o addopts= tests/editing_conformance/test_recipe_text_binding_native.py tests/editing_conformance/test_recipe_text_binding_spike.py tests/sdk/test_timeline_script.py -m 'not integration'` -> `52 passed, 2 deselected`.
- Parent in-memory authority-node reproduction -> `1 failed, 1 passed`.
- Candidate genuine Runtime script node -> `1 failed in 1.86s`.
- Parent genuine Runtime script node -> `1 passed in 1.72s`.
- Ruff -> pass.
- Mypy `--follow-imports=skip` -> pass.
- `py_compile` for both changed files -> pass.
- `git diff --check` -> pass.
- Original relevant production/test files are byte-identical to base; candidate native SHA-256 is `b885711cecfa2bd92a7c0abb8e4464e1bb711fa838e6e13581cc58a9ad3bc3f2`, additive test SHA-256 is `7ae90e6d46a3c2960dd200073b64536aa02a048083b4978f9d8dc59ab8799fc0`.

## Boundary / next owner

The author must resolve the conflict between the required changed-text rebind and the new `authenticated text binding pin does not match the new text` refusal. Any repair must preserve the settled incomplete-authority, wrong-pair, no-write, and public/private-data guards and then be independently requalified against the same Runtime receipt. No product correction was made in this review.
