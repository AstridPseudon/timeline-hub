## Report — F-D32-render-wire

No tracked files changed. `DONE` and commit message were written.

### Classification

All six failures share the same producer/result-path cause:

- `test_conformance.py:86–100` invokes the SDK wrapper through `CommandTransport`, expecting `workspace/result.json`.
- `sdk_render.py:44–48` calls `astrid.sdk.rendering.renderer_main`.
- Render path imports `atomic_io` at `astrid/sdk/rendering.py:294`; support path does so at line 467.
- `atomic_io.py:16` imports `runtime_protocol`.
- Sanitized child policy excludes `PYTHONPATH` and `ASTRID_RUNTIME_CHECKOUT` (`subprocess_env.py:57–72, 90–122`).
- The child exits before writing any result. `CommandTransport` then reports exit 1 before its result read (`transport.py:327–344`).

A bounded synthetic probe reproduced this for both `render` and `support`: `ModuleNotFoundError: runtime_protocol`, return code 1, requested result path absent. Supplying the Runtime source root in a separate synthetic pack-root run produced a result successfully.

This is an Agent execution/host child-environment issue, owned by the existing `agt-F-env-cohort-2356` / Runtime OPS boundary. No renderer, Composition, result contract, or assertion defect is evidenced. The minimal repair is to qualify the managed child environment with the exact Runtime import root/package while preserving installed-profile and source-custody controls.

### Evidence and limits

- Relevant files are identical between current `b61cebe8` and retained source `c36ca8c94`.
- Retained remote child stderr/cwd for these six is unavailable; the named qualified environment brief is also absent. Therefore remote qualification remains unverified.
- No original six-case replay, full suite, browser, HTTP, provisioning, or product edit was performed.
- Real production path: `RenderService._run_command` (`service.py:1905–1946`) owns the authoritative result path and calls `CommandTransport`; these six specifically exercise the public SDK wrapper via the conformance harness.

### Checks

- `git diff --exit-code` — PASS
- `git diff --check` — PASS
- AST parse of conformance, transport, environment, atomic I/O, SDK renderer, wrapper, and fixture source — PASS
- Bounded synthetic probe, timeout 10s — reproduced the missing-result failure

No new typecheck/lint scope applies because no tracked files changed.

Recommended next step: obtain the exact qualified Agent/Runtime child environment, apply the environment-owner repair, then run the six original nodes once.