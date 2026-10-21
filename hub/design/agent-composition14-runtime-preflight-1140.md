# Composition14 Agent runtime preflight handoff

Status: **READY TO REQUEST, not requested**. This source-only handoff is for
the reviewed Agent pin. It does not build, install, launch, test, render, or
change any shared runtime/dependency. Independent pin review1137 remains the
adoption gate.

## Exact immutable request

Use this new immutable name; do not reuse an existing runtime directory:

```text
agent-remotion-composition14-255b6856
```

The exact request, to be run later by the orchestrator/dispatcher, is:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-runtime \
  agent-remotion-composition14-255b6856 \
  255b6856cc1c96f4d40ddac05d4e3d98bb81051c \
  b7c4ab2e3c3f466d9d1c0c8d7472a40101d37b6288d52b930067dc663a17feb0
```

Exact source identity:

| item | value |
| --- | --- |
| Agent commit | `255b6856cc1c96f4d40ddac05d4e3d98bb81051c` |
| Agent tree | `aed2ccf7596add9118b272afad831c214ede11fe` |
| `remotion/package-lock.json` SHA-256 | `b7c4ab2e3c3f466d9d1c0c8d7472a40101d37b6288d52b930067dc663a17feb0` |
| Composition artifact | `@banodoco/timeline-composition@0.0.14` |
| artifact SHA-256 | `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e` |
| artifact size/members | `72134` bytes / `80` regular members |
| lock integrity | `sha512-Bgf9lHdk3CJCTsA3Jbd5WW9UYCHEZQTF3VFM1YO6dimZ+q8bQ8cX6CZ4FCfClBNgg10DQ1bozGMqFCpkGNXvvw==` |

The source `runtime.lock.json` is unchanged and names Runtime
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`; the normal Runtime14/95 pin is a
separate prerequisite. Do not repoint it for this task. The existing C13
coherent-full target and its `/home/user/work/wt/rt-pin-9d1c43c6` pointer are
separate frozen evidence and must not be rewritten or used to lower its
storage floor.

## Dispatcher/runtime prerequisites

Before requesting, perform only these read-only checks against the Agent
source:

```sh
AGENT=/home/user/work/agent
SHA=255b6856cc1c96f4d40ddac05d4e3d98bb81051c
LOCK=b7c4ab2e3c3f466d9d1c0c8d7472a40101d37b6288d52b930067dc663a17feb0
test "$(git -C "$AGENT" rev-parse "$SHA^{commit}")" = "$SHA"
test "$(git -C "$AGENT" show "$SHA:remotion/package-lock.json" | sha256sum | awk '{print $1}')" = "$LOCK"
test ! -e /home/user/work/runtimes/agent-remotion-composition14-255b6856
```

The dispatcher-created runtime must be read-only and must retain the same lock
bytes and package artifact bytes:

```sh
R=/home/user/work/runtimes/agent-remotion-composition14-255b6856
test "$(sha256sum "$R/package-lock.json" | awk '{print $1}')" = "$LOCK"
test "$(sha256sum "$R/artifacts/banodoco-timeline-composition-0.0.14.tgz" | awk '{print $1}')" = "21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e"
test "$(tar -tzf "$R/artifacts/banodoco-timeline-composition-0.0.14.tgz" | awk '!/\/$/{n++} END{print n+0}')" = 80
```

For the generated named node suite, the minimum environment is the normal
template emitted by `make-runtime`:

```text
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-composition14-255b6856
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
```

If a later selected node crosses the Runtime boundary, use the already
qualified Runtime14/95 checkout instead of the stale integration alias:
`ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f` and
`PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f"`. Neither choice authorizes
changing `runtime.lock.json`; no C13 checkout is part of this request.

The dispatcher will derive the named suite
`agent-remotion-composition14-255b6856-nodes` from the existing
`remotion-0012-nodes` recipe. It must not be requested in this worker task.

## Minimal later acceptance nodes

Run only after the immutable runtime exists and the independent pin review is
closed. These are the smallest named checks for this handoff:

```text
tests/packs/rendering/test_composition_package.py::test_locked_release_is_built_and_requires_no_separate_schema_or_theme
tests/packs/rendering/test_composition_package.py::test_installed_package_refuses_incomplete_or_unsafe_built_exports[delete]
tests/packs/rendering/test_composition_package.py::test_installed_package_refuses_incomplete_or_unsafe_built_exports[missing]
tests/packs/rendering/test_composition_package.py::test_installed_package_refuses_incomplete_or_unsafe_built_exports[outside]
tests/packs/rendering/test_composition_package.py::test_launch_input_binding_reuses_built_package_readiness
tests/packs/rendering/test_composition_package.py::test_generated_custom_elements_reach_shared_render_and_scene_unchanged
tests/test_installer_schema.py::test_remotion_lock_pins_the_immutable_composition_public_entry
tests/core/timeline/test_clip_fields.py::test_render_status_defaults_to_pinned_union_composition
```

The custom-owner/theme node must preserve the exact assertions in
`remotion/tests/composition-package.mjs`: default `2rp` theme version `0.1.0`
and `art-card` resolve; an external theme does not; custom effect/animation/
transition owners resolve through generated host registries; built-in and
host registries remain distinct; unknown owners/elements refuse; SSR retains
the custom markup and opaque props; and host registry generation leaves every
installed package byte unchanged.

The built-entry/default checks must also retain all public exports under
`./dist/`, omit separate `@banodoco/timeline-schema` and
`@banodoco/timeline-theme-2rp` lock entries, and keep the explicit historical
compatibility lanes: 0.0.12 scene fixtures, 0.0.13 presenter/backend fixtures,
0.0.10/0.0.12/0.0.13 capture-label fingerprints, and explicit 0.0.7 clip
field behavior. The receiving default is 0.0.14 only.

## Scope and evidence

No source file was changed. No Runtime request, build, install, launch, test,
HTTP, render, browser, full suite, or shared dependency mutation was performed.
The source facts above were read from the qualified release14 handoff,
original1130 report, review1137, and Agent commit `255b6856…`.
