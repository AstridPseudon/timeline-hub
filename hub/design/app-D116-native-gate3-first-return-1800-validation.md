# D116/G3 first-return source validation

Verdict: `SOURCE_DEPENDENCY`; no source edit was admissible.

Commands and results:

```text
PYTHONPYCACHEPREFIX=/tmp/app-D116-native-gate3-first-return-1800-pycache /home/user/work/venv-agent/bin/python [AST/compile for native_checkout_current_fixture.py and test_native_checkout_current_equivalent.py] -> PASS
RUFF_CACHE_DIR=/tmp/app-D116-native-gate3-first-return-1800-ruff-cache /home/user/work/venv-agent/bin/ruff check tests/editing_conformance/native_checkout_current_fixture.py tests/editing_conformance/test_native_checkout_current_equivalent.py -> PASS
/home/user/work/venv-agent/bin/mypy --cache-dir /tmp/app-D116-native-gate3-first-return-1800-mypy-cache --config-file pyproject.toml tests/editing_conformance/native_checkout_current_fixture.py -> PASS
git diff --check HEAD^ HEAD -> PASS
git status --short --untracked-files=all -> clean
```

The protected Gate3 node was not rerun here. No pytest, collection, Runtime/service/socket, native, browser, full/family, P2, P4, or other-three replay was run. The sole prior authorized Gate3 node already established `FAIL_SETUP` at fixture line 91.

The existing public route is finite and identified: `capture_occurrence_delete(authored, "occurrence:occ")` invokes `commands.execute`; after the occurrence is cleared, recorder compilation calls the word-anchor binding and raises `bound source occurrence/clip is missing or ambiguous`. A compliant fixture-only correction would have to remove or rebind the still-authored anchor, preserve the occurrence, or use an unsupported generic/private route. Each violates the brief, so no edit is applied.
