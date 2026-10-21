# D13 exact Sol sourcefix: independent final process-custody review

**APPROVE — exact source `89a5bb654bdcdd7e3f555c3645f3fc8bcf7824f1`, tree
`f1cb55e3baf1c2119f04761c05b3c2e431df39d0`.** The manager is authorized to
stage this exact source in the manager-selected coherent installed Agent /
Runtime / client environment. This is source and installed-origin approval
only; it is **not live qualification**, and it does not authorize a native,
socket, renderer, 688, or full-suite run.

## Review result

The prior concrete positive-control failure is fixed. The isolated installed
probe now calls `PathFinder.find_spec()` with each leaf module name and its
explicit parent search path. This avoids dotted parent lookup consulting
unloaded product-package state while retaining the no-product-import boundary.

The probe still checks exactly these eight origins:

```text
host, child, action, client, sdk,
runtime_protocol, runtime_protocol.platform, astrid_runtime
```

It retains the exact source-file, `SourceFileLoader`, package-search-location,
selected-tree, and symlink-component checks, including the Runtime package
symlink scan. The AST control confirms the probe imports only
`importlib.machinery`, `json`, `pathlib`, and `sys`; it contains no product
import, `ImportFrom`, dynamic import, or code-loading call.

The trust scope is coherent and bounded: the selected interpreter and its
immutable, non-editable installed Agent/Runtime/client tree, entered through
the trusted controller. Checkout fields remain provenance, not import
authority. This review makes no unsupported claim of active pre-entry byte
attestation, protection from a same-user replacement before controller entry,
or authenticated source bytes beyond the existing origin/closure and child
startup guards.

## Preservation

`89a5bb654` has parent `d803c7c48` and changes only
`astrid/sdk/host_bootstrap.py` (two insertions, one deletion). The original
positive, substitution, ambient-runtime, symlink, missing-runtime, and
isolated-agent assertions are byte-identical to the parent. `git diff --check`
passes; no current preservation files or tests were dropped.

## Evidence

From the exact source tree, this bounded run covered only the requested 18
controls: six compact bootstrap controls, the complete real installed-origin
control file, and the retained publication/refusal neighbor:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-d13-real-positive-leaf-fix/pytest-installed-origin-2 \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_strips_source_pythonpath_and_probes_selected_interpreter \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_refuses_checkout_origins_from_isolated_probe \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_does_not_use_ambient_runtime_checkout \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_origin_probe_resolves_without_product_imports \
  tests/sdk/test_host_bootstrap_source_identity.py::test_python_source_loader_can_read_cache_before_bytecode_write_policy \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter \
  tests/sdk/test_installed_runtime_source_identity.py \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_legacy_assembler_admission_refuses_before_execution_and_keeps_artifacts
```

Result: **18 passed in 8.91s; exit 0**. The real installed pair passed, all
four post-probe Runtime substitutions were fenced at child import, and the
original symlink/ambient/missing-runtime assertions passed unchanged.

Additional source checks passed:

```text
git diff --check d803c7c48 HEAD
git diff --exit-code d803c7c48 HEAD -- tests/sdk/test_host_bootstrap_source_identity.py tests/sdk/test_installed_runtime_source_identity.py
```

No full suite, 688 suite, native, live Runtime, socket, renderer, or browser
qualification was run or claimed.
