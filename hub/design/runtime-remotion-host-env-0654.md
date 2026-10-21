# Runtime Remotion host environment correction

Date: 2026-10-21

## Scope

Runtime-owned entries in `tests/suites.conf` were audited for command chains
that invoke Agent integration tests or a wrapper which can launch a Remotion
pack-host. The container exports `NODE_OPTIONS=--max-old-space-size=8192` and
`NODE_PATH=/usr/local/lib/node_modules_global`. Agent's existing
`remotion_runtime.probe_context` correctly rejects both values as unsupported
loader/interpreter overrides; the guard and product auth/custody code were not
changed.

## Before/after inventory

The following ten Runtime-owned entries changed. Every change removes only the
two variables immediately before the effective Python or shell target; all
other environment assignments, markers, selectors, source checks and custody
arguments are byte-for-byte preserved.

| line | suite | before | after |
|---:|---|---|---|
| 40 | `capture-legacy-integration` | `env ASTRID_CHECKOUT=...` | `env -u NODE_OPTIONS -u NODE_PATH ASTRID_CHECKOUT=...` |
| 44 | `capture-agentbb01-integration` | guarded `env ASTRID_CHECKOUT=...` | guarded `env -u NODE_OPTIONS -u NODE_PATH ASTRID_CHECKOUT=...` |
| 61 | `marked-integration` | `env ASTRID_CHECKOUT=...` | `env -u NODE_OPTIONS -u NODE_PATH ASTRID_CHECKOUT=...` |
| 72 | `capture-agent92427b3a-integration` | `env ASTRID_CHECKOUT=...` | `env -u NODE_OPTIONS -u NODE_PATH ASTRID_CHECKOUT=...` |
| 73 | `capture-agent92427-integration` | guarded `env ASTRID_CHECKOUT=...` | guarded `env -u NODE_OPTIONS -u NODE_PATH ASTRID_CHECKOUT=...` |
| 74 | `capture-agentcf7448-integration` | `env ASTRID_CHECKOUT=...` | `env -u NODE_OPTIONS -u NODE_PATH ASTRID_CHECKOUT=...` |
| 84 | `registered-assembler-canonical-target` | `bash run-registered-probe "$PWD"` | `env -u NODE_OPTIONS -u NODE_PATH bash run-registered-probe "$PWD"` |
| 86 | `text-native-private-pair-integration` | `... && env ASTRID_RUNTIME_CHECKOUT=...` | `... && env -u NODE_OPTIONS -u NODE_PATH ASTRID_RUNTIME_CHECKOUT=...` |
| 89 | `public-s2-literal-current-integration` | inline `env ASTRID_CHECKOUT=...` | inline `env -u NODE_OPTIONS -u NODE_PATH ASTRID_CHECKOUT=...` |
| 131 | `ordinary014-parent-agent7b3-integration` | `env ASTRID_RUNTIME_CHECKOUT=...` | `env -u NODE_OPTIONS -u NODE_PATH ASTRID_RUNTIME_CHECKOUT=...` |

The registered assembler script itself uses the same Agent Remotion test path,
so the suite-level `env -u` is placed around `bash` and reaches its `exec`
target without adding a wrapper framework. The text-native and broad
integration lanes retain their existing arguments and pytest selectors.

## Inspected unchanged scope

- D13 `d13-native7d-public13-integration` and `rt-wc8-current14-integration`
  already use `env -i`; they were left unchanged.
- `wc10-installed-launcher-integration` runs only Runtime's
  `tests/test_wc10_installed_launcher.py`; its installed Runtime bootstrap
  does not set `ASTRID_REMOTION_PROJECT_DIR` or launch a Remotion host, so it
  was left unchanged. No installed workflow was rerun.
- Historical immutable tuple lanes, including the raw27/catalog-era entries,
  were not replayed. Their historical lostpayload cause remains UNKNOWN and is
  not relabeled as an environment failure.
- App/Viewing Theme and cross-product suite lines are peer-owned and were not
  edited. Recommendation to those owners: apply the same child-process
  `env -u NODE_OPTIONS -u NODE_PATH` or existing `env -i` pattern at their
  actual Remotion-host target while preserving their own arguments and guards.

## Evidence

The retained startup evidence uses the exact error name
`runtime validation refuses unsupported loader/interpreter overrides`, which
matches the unchanged Agent guard. Negative `probe_context` checks that inject
unsafe `NODE_OPTIONS`/loader values remain in Agent tests; no guard bypass was
introduced.

Cheap validation passed for all ten modified lines: each command parsed with
`bash -n`, each contains exactly one `env -u NODE_OPTIONS -u NODE_PATH`, and a
no-host subprocess witness confirmed only those two variables were removed
while a sentinel environment variable remained. No product, schema, DTO,
auth, custody, version, pin, shared dependency, renderer, browser, native,
MP4, installed workflow or full-suite path was run.
