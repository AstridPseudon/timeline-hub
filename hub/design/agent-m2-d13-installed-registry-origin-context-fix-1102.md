# D13 installed registry origin/context fix

## Scope and source

Implemented source-only on Agent worktree
/home/user/work/wt/agt-m2-d13-installed-registry-origin-context-fix-1102,
based at f4edcb4bce531be3ea8c6389069429175b048c2a. No commit, install,
profile rebuild, native/HTTP/render run, or D13 rerun was performed.

Changed source:

- astrid/core/rendering/remotion_runtime.py
- astrid/core/execution/generic_host.py
- tests/core/rendering/test_remotion_registry_context_key.py
- tests/test_generic_host.py

The live callers remain:

- astrid/sdk/host_bootstrap.py:776-790 —
  _host_render_environment removes ambient ASTRID_PACKS_PATH and, for the
  installed profile, PYTHONPATH; it already invokes the existing
  _installed_execution_origins guard.
- astrid/sdk/host_bootstrap.py:804-825 —
  _prepare_render_validation projects host and worker probe environments.
- astrid/core/execution/generic_host.py:1715-1834 —
  _launch_worker_probe_environments supplies the host baseline/native/
  command variants.
- astrid/core/rendering/remotion_runtime.py:685-740 —
  _registry_probe launches and validates registry discovery.
- astrid/core/rendering/remotion_runtime.py:743-825 —
  _settle_registries binds observations and, when needed, runs the
  existing generator carrier.

## Change

Installed registry discovery now uses the selected python with -I, a
resolved neutral temporary-directory cwd, and no checkout arguments or
injected PYTHONPATH. It refuses an installed probe environment carrying
PYTHONPATH or explicit ASTRID_PACKS_PATH, and validates that the returned
Astrid/runtime/generator origins are in the selected installed product tree,
that the executable identity matches, and that the probe cwd is neutral.

The observation imports the generator through the existing Remotion run
module's gen_effect_registry carrier. It no longer calls load_checkout_script
from the parent checkout. If the selected installed package lacks that
carrier, it fails with the precise
installed registry generator carrier is unavailable packaging-gap error.
When the carrier exists, installed settling executes its observed installed
origin from the neutral cwd; source mode retains its checkout behavior and
strict source-origin/sharing checks.

Installed worker projection now omits the extra pack-root and source
PYTHONPATH authority for baseline/native/command probe contexts. Explicit
manifest-configured foreign roots remain visible so the installed probe can
refuse them; source mode is unchanged. This makes host/native registry
contexts equal under the coherent installed assumption.

## Tests

Passed:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-m2-d13-installed-registry-origin-context-fix-1102-pytest-final tests/core/rendering/test_remotion_registry_context_key.py tests/core/rendering/test_remotion_registry_git_env.py tests/core/rendering/test_remotion_probe_diagnostic.py tests/test_generic_host.py -k 'registry_context or registry_probe or worker_projection or fixed_registry_selectors or command_projection'

    17 passed, 255 deselected in 17.24s
    git diff --check

The focused direct tests cover installed interpreter/neutral cwd, foreign
interpreter and cwd, foreign PYTHONPATH, unsupported explicit pack roots,
missing generator carrier, source-mode registry diagnostics, and installed
host/native context equality.

An additional targeted rendering selection reached 65 passing tests but had
three unrelated existing failures in
tests/packs/rendering/test_render_remotion_registry.py: this worktree has no
remotion/node_modules/@banodoco/timeline-composition/package.json, so the
pre-existing generator path raises its missing Composition-package error.
No shared dependency was installed or modified. Ruff was not a clean
repository gate: it reports many pre-existing findings in the giant host/test
files (including existing import/order and E402/BLE/E701/E702 findings); no
new source formatting error was acted on beyond the touched import ordering.

Independent SECURITY review is still required before merge or proof. No
installed qualification or actual D13 behavior is claimed.
