## Report

Implemented the four current native-checkout companions in:

- [native_checkout_current_fixture.py](/home/user/work/wt/app-D116-native-topology4-1644/tests/editing_conformance/native_checkout_current_fixture.py)
- [test_native_checkout_current_equivalent.py](/home/user/work/wt/app-D116-native-topology4-1644/tests/editing_conformance/test_native_checkout_current_equivalent.py)

Preserved all original fixtures/selectors; used the registered provider, transcript pin, exact media, timing, opaque values, CLI path, peer conflict, restart, undo, and Gate3 behavior.

Checks passed:

- `py_compile`
- Ruff
- mypy
- `git diff --check`
- Collection: exactly 4 new cases

Functional tests: `NOTRUN`. Local free space was below the required 5 GB floor. The central targeted run also failed before collection because its isolated checkout lacked `runtime_protocol`.

Evidence and commit message were written under the assigned worker directory. Independent protected review remains required before merge.