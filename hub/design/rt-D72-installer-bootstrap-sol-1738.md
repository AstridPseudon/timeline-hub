Added [one focused bootstrap-path test](/home/user/work/wt/rt-D72-installer-bootstrap-sol-1738/tests/test_installer_bootstrap_schema.py). **No product code changed.**

The remaining dependency belongs at the D67 environment boundary:

- Staging verifies Runtime’s canonical JSON, digest `4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd`.
- The render reader separately requires `banodoco_timeline_schema` Python models and verifies their origin.
- `_provision_render_runtime_env` is byte-identical across frozen R4, `origin/main`, and candidate `b4f79d12e0037f283ccc929f364f38d21dc50d4a`.
- Binding the JSON directory cannot satisfy that reader. Review1735’s proposed connection would require additional authority beyond D72’s local canonical-schema scope.

Exact symbol hashes and source locations are retained in [source-attribution.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D72-installer-bootstrap-sol-1738/evidence/source-attribution.json).

Validation:

```sh
PYTHONPATH=/home/user/work/wt/rt-D72-installer-bootstrap-sol-1738:/home/user/work/runtime:/home/user/work/runtime/packages/python PYTHONDONTWRITEBYTECODE=1 \
/home/user/work/venv-agent/bin/python -m pytest \
tests/test_installer_schema.py tests/test_installer_remotion.py \
tests/test_installer_sources.py tests/test_installer_bootstrap_schema.py \
-q -oaddopts= -pno:cacheprovider \
--junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D72-installer-bootstrap-sol-1738/evidence/result.xml
```

**51 passed; zero failures, errors, or skips.** An initial invocation without Runtime on `PYTHONPATH` failed collection.

Scoped Ruff found only the two inherited `I001` findings; base/candidate delta is zero. Scoped mypy passed for base and candidate; broader mypy still stops on the known 14 YAML/NumPy diagnostics. Compile and tracked/new-file whitespace checks passed.

The test exercises real staging, source-host provisioning, and schema readers while mocking acquisition, native tools, and JS installation checks. It **does not qualify installed origins or render readiness**. No product RED/GREEN correction is claimed.

Next step: retain D67’s genuine installed-tuple/model-package dependency; denied acquisition routes remain stopped. Contract, history ABI, and D62 behavior are untouched. Commit message and `DONE` marker written.