# D13 real source-context security review

## Verdict

**REJECT — concrete executable source-authority counterexample.** Reviewed
candidate commit `6c37224ed18fdbb3d90ae5f472629205ba9b6d5c`, tree
`36e9bc966687c41dd49aa3f271789bc46da37aec`.

The new Runtime import-root propagation trusts the caller/host environment's
`ASTRID_RUNTIME_CHECKOUT` directly. It does not require that path to be the
Runtime checkout selected by the supported bootstrap, does not require it to
exist, and does not reject symlinked source authority. `Path(...).resolve()`
only canonicalizes the path; it is not an authority or ownership check.

## Reproduction

Bounded probe, with no product edits:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python - <<'PY'
from pathlib import Path
from astrid.core.execution import generic_host
attacker = Path('/tmp/d13-review-attacker-runtime')
variants = generic_host._launch_worker_probe_environments(
    (Path.cwd() / 'astrid/packs/rendering',),
    {'HOME': '/tmp', 'PATH': '/usr/bin', 'LANG': 'C.UTF-8',
     'ASTRID_RUNTIME_CHECKOUT': str(attacker)},
    remotion_only=True,
)
assert any(str(attacker) in v.get('PYTHONPATH', '').split(':') for v in variants)
PY
```

Observed: `worker_probe_accepts_nonexistent_runtime=True`; the attacker path
was included in every native/command probe `PYTHONPATH` variant.

The renderer transport is independently exploitable through its public
`CommandTransport.run(..., env=...)` overlay. This executed successfully with
a temporary package under the caller-selected path:

```text
from astrid.core.rendering.transport import _build_environment
child_env = _build_environment({'ASTRID_RUNTIME_CHECKOUT': str(attacker_root)})
subprocess.run([sys.executable, '-c',
    'import runtime_protocol; print(runtime_protocol.ORIGIN)'],
    env=child_env, check=True)
```

Observed output: `symlink-attacker`, with `runtime_protocol.__file__` under the
attacker target. The configured checkout was a symlink; `_build_environment`
resolved it and imported the target. The same direct transport probe with a
nonexistent path returned `PYTHONPATH=/tmp/d13-review-attacker-runtime`.

## Why this is not proven by the supported bootstrap

The Agent bootstrap's launcher result forwards `source_checkout` and runtime
identity fields but not `runtime_checkout` (`astrid/sdk/autobootstrap.py`
around lines 295–307). `ensure_pack_host` then builds the host environment by
copying `os.environ` (`astrid/sdk/host_bootstrap.py` around lines 740–754).
Thus the new import root is ambient/caller-controlled at the point where the
candidate consumes it; the Runtime `SourceProfile.runtime_checkout` validation
is not bound into this Agent host launch projection.

This violates the requested condition that the exact Runtime root be selected
through supported bootstrap only, and permits a source tree outside the
validated source/lock/identity custody to become import authority.

## Exact production caller list

- `astrid/sdk/host_bootstrap.py:782` calls
  `generic_host._launch_worker_probe_environments(...)` during render
  readiness preparation.
- `astrid/core/rendering/transport.py:163` calls `_build_environment(...)`
  for every `CommandTransport.run` child; the candidate's new logic is at
  `transport.py:426–434`.
- The Runtime checkout is also consumed directly at
  `generic_host.py:7739–7743` (native readiness projection),
  `generic_host.py:8094–8106` (command child),
  `generic_host.py:8402–8406` (actual capability child), and
  `remotion_runtime.py:860–869` (registry generator child). The candidate
  adds the probe projection at `generic_host.py:1766–1800`.
- `astrid/core/subprocess_env.py:115` propagates
  `ASTRID_RUNTIME_CHECKOUT`, so the unbound caller value survives the child
  environment filter.

## Comparison fingerprints

| reference | commit | tree |
|---|---|---|
| candidate | `6c37224ed18fdbb3d90ae5f472629205ba9b6d5c` | `36e9bc966687c41dd49aa3f271789bc46da37aec` |
| ca2 | `ca2a625943b4750d3353cf938d26d321a2bb50e8` | `5b2f26b979bbdab0b75413dc4b17f20de672afb3` |
| 6b | `6b526a057cf4846f2e7a1d8c137837ed5fc188c6` | `f66b1dd13c470f4a8aca43972904384056312d53` |
| original approved 6ef | `6efc81500a0e0688c2bb41e736503f0fc3e04abb` | `2ed2b8a12b5b3391ca221ba6ff05390f71a73556` |

Candidate changes are limited to `generic_host.py`, `transport.py`, and the
native integration test. No source/lock/identity wait, census, custody,
credential redaction, active `host.discover` assertion, or non-ffprobe decode
claim was removed in the candidate diff. The readiness repair's cited central
`d13-native-positive-render-integration` result (`1021015920-10910`, 1 pass)
therefore remains useful positive evidence, but it does not exercise the
caller-controlled Runtime-root negative case above.

## Targeted evidence

- **PASS** — 12 selected GenericHost/transport/registry security tests in
  `tests/core/execution/test_generic_host_actions_v3.py`,
  `tests/core/rendering/test_remotion_registry_context_key.py`, and the two
  non-spawning transport tests: `12 passed`.
- **PASS** — selected strict Remotion readiness/source/custody tests in
  `tests/packs/rendering/test_render_export_task_adapter.py`: `36 passed,
  11 warnings` (the warnings are Python 3.14 tar extraction deprecations).
- **PASS** — selected supported-bootstrap/source-identity tests in
  `tests/stage1/test_cold_launch_autobootstrap.py`,
  `tests/stage1/test_host_bootstrap_manifest_luna.py`, and
  `tests/sdk/test_host_bootstrap_source_identity.py`: `14 passed`.
- **NOT PROVEN** — the two live transport child tests
  `test_environment_is_allowlisted_and_host_secrets_are_not_passed` and
  `test_pinned_renderer_runtime_is_propagated_to_protocol_child` failed before
  child launch because this sandbox lacks the required Linux pidfd custody
  primitives (`CustodyError: incarnation-bound kernel custody is unavailable`).
  They were not bypassed or weakened.
- No full suite, duplicate native/render integration, or blind baseline suite
  was requested or run.

## Required next step

Before approval, bind the selected Runtime checkout into the supported launch
projection and revalidate its exact canonical, non-symlink source identity at
the GenericHost/renderer child boundary. Add a permanent negative test proving
that a caller overlay, foreign JSON/path input, nonexistent checkout, and
symlink checkout cannot become `PYTHONPATH` import authority. Re-run the
original native positive node only after that narrow correction.
