# D136c validation

## Identity and source custody

- Final commit: `2f1fbb1fc2954dc54eda7f29656de8f15e38683a`.
- Final tree: `37cfcd4f6108c1fdda401e563e3674503bc328ef`.
- Base commit/tree: `f103bb46866999c961a8865636f2e66d544e0c9b` / `5d0cedf2e5134acf895e8d43191cc5fdc09f9883`.
- `git diff --name-status f103bb46866999c961a8865636f2e66d544e0c9b..HEAD`: exactly the two production files and one new test listed in `source-manifest.json`.
- `git status --short --branch`: clean at review.
- `git diff --check`: PASS.
- Immutable `ab1e` auth/store preimages equal `f103` exactly; see `ab1e-applicability.json`.

## Exact author commands, rerun on final committed source

1. `/home/user/work/venv-runtime/bin/python -m pytest tests/test_timeline_missing_observation_diagnostics.py -q -o addopts= -p no:cacheprovider` — **3 passed**.
2. `/home/user/work/venv-runtime/bin/python -m pytest tests/test_timeline_commit_redacted_diagnostics.py tests/test_timeline_commit_authentication.py::test_sequential_created_child_boundary_uses_the_native_birth_not_future_output tests/test_timeline_commit_port.py::test_provider_cannot_forge_preview -q -o addopts= -p no:cacheprovider` — **5 passed**.
3. `/home/user/work/venv-runtime/bin/python -m pytest 'tests/test_timeline_commit_authentication.py::test_native_record_assertions_and_additional_effects_on_a_real_film[False-False]' -q -o addopts= -p no:cacheprovider` — **1 passed**; genuine registered-provider native seed.
4. `/home/user/work/venv-runtime/bin/python -m pytest tests/test_timeline_commit_authentication.py::test_native_text_alias_refusals_are_atomic tests/test_timeline_commit_port.py::test_neutral_runtime_refuses_without_writes -q -o addopts= -p no:cacheprovider` — **4 passed**.
5. `/home/user/work/venv-runtime/bin/python -m pytest tests/test_timeline_missing_observation_diagnostics.py tests/test_timeline_commit_redacted_diagnostics.py tests/test_timeline_commit_authentication.py::test_sequential_created_child_boundary_uses_the_native_birth_not_future_output tests/test_timeline_commit_port.py::test_provider_cannot_forge_preview -q -o addopts= -p no:cacheprovider` — **8 passed**.
6. `/root/.local/bin/ruff check runtime_protocol/timeline_commit_auth.py tests/test_timeline_missing_observation_diagnostics.py` — **All checks passed**.
7. `/root/.local/bin/ruff check runtime_protocol/timeline_commit_store.py` versus the same stdin check on `git show f103bb46866999c961a8865636f2e66d544e0c9b:runtime_protocol/timeline_commit_store.py` — **10 baseline errors before and after; zero new**.
8. `/root/.local/bin/pyright runtime_protocol/timeline_commit_auth.py tests/test_timeline_missing_observation_diagnostics.py` — **0 errors, 0 warnings, 0 informations**.
9. `/root/.local/bin/pyright runtime_protocol/timeline_commit_store.py` versus the f103 worktree `/home/user/work/runtime/runtime_protocol/timeline_commit_store.py` — **52 pre-existing diagnostics before and after; no changed-line diagnostic**.
10. `PYTHONPYCACHEPREFIX=<private /tmp cache> /home/user/work/venv-runtime/bin/python -m py_compile runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_store.py tests/test_timeline_missing_observation_diagnostics.py` — **PASS**.

## Additional review checks

- Counterfactual production guard/serializer probe on both f103 and final source: after dropping only `details.safe_diagnostic`, canonical serialized refusals were byte-identical; see `refusal-equality.json`.
- Adversarial allowlist probe with sentinel identifier/path/content/URL/private-path values: **PASS**, no sentinel or unbounded value returned.
- AST call-site audit: `_safe_observation_diagnostic` has one call, at the 2209 guard; `safe_details` has no other caller; no new recorder/collector.

## Not run / limits

No full suite, broad auth family, original9, browser, localhost/live-socket, core/child/Store/profiling/WAL/SWAP/D130-body suite was run. The prior original9 result remains NO_GO/HELD (nine setup errors, zero pass/fail/skip). No source, protected test, generated, pin, kit, hub, Git-internal, credential, acquisition, or backport edit was made.
