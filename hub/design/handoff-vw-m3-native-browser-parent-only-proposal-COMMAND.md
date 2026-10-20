# Commands and results

All source changes were made only in a private archive overlay under this
worker's directory. The shared Agent worktree and shared dependencies were
read-only.

## Private overlay and patch applicability

```bash
worker_dir=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-native-browser-parent-only-proposal
overlay=$(mktemp -d "$worker_dir/archive.XXXXXX")
realpath "$overlay"
git archive HEAD | tar -x -C "$overlay"
git -C "$overlay" apply --check "$worker_dir/proposal.patch"
git -C "$overlay" apply "$worker_dir/proposal.patch"
```

Result: **PASS**. The overlay was a private real directory and did not resolve
into a shared node_modules, runtime, or venv path.

## Focused tests

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="$overlay" TMPDIR="$overlay/tmp" \
/home/user/work/venv-agent/bin/python -B -m pytest -q \
  -p no:cacheprovider --override-ini='addopts=' --tb=short \
  "$overlay/tests/core/test_subprocess_env.py::test_remotion_browser_executable_is_parent_owned_and_unlisted_env_is_dropped" \
  "$overlay/tests/core/execution/test_remotion_host_session.py::test_child_start_forwards_only_parent_owned_browser_selector" \
  "$overlay/tests/core/execution/test_remotion_host_session.py::test_child_start_environment_does_not_include_runtime_credentials" \
  "$overlay/tests/core/execution/test_remotion_host_session.py::test_task_cannot_modify_host_scope_inputs_or_escape_attempt" \
  "$overlay/tests/core/execution/test_remotion_host_session.py::test_unexpected_render_fields_refused_before_native_allocation"
```

Result: **9 passed in 0.66s**.

The test set included the existing parent-precedence/unlisted-env policy,
runtime-credential exclusion, the four existing host-scope refusal cases, the
two existing unsupported-render-field cases, and the new parent-forward test.

## Scope and non-runs

```bash
grep '^diff --git' "$worker_dir/proposal.patch"
```

Result: exactly:

```text
diff --git a/astrid/core/execution/remotion_host_session.py b/astrid/core/execution/remotion_host_session.py
diff --git a/tests/core/execution/test_remotion_host_session.py b/tests/core/execution/test_remotion_host_session.py
```

No full or central test-service suite was requested. No direct CLI backend
render test, Node/browser process, local server, install, network, or shared
cache/venv mutation was run.
