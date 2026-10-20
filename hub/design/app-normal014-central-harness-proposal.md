# App normal014 private central harness proposal

Status: **READY FOR MANAGER REGISTRATION; private runner preflights passed; central execution not submitted**.

This is a private same-cohort harness. It does not change the App lock, pinned
packages, generated client, shared schema, Runtime, Agent, producer, frozen
reference, release state, or activation state.

## Exact candidate

| input | identity |
| --- | --- |
| App candidate | assigned App worktree snapshot; its checked-in Runtime lock remains 0.2.13 |
| Agent source | `3c4f6de4fa777323b3386c01c7266b619b86af6d`, tree `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c` |
| Runtime candidate | `202074110717146fc7f08af2306a8dd7f695b0b1`, tree `ee39286bd0eb27d4075074cc4785d6d15e33f243` |
| immutable Runtime producer | `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476` |
| package/artifact | unpublished `0.2.14`, `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa` |
| Runtime manifest | `sha256:ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`, 75 entries |
| shared edit-command schema | raw SHA-256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Runtime wire digest | `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59` |

The private runner clones these exact commits with `git clone --shared` into a
per-run temporary directory. It verifies every manifest artifact byte against
the immutable producer, checks Agent/Runtime schema byte equality, and uses the
leased public13 graph only through a read-only symlink. No package manager
install or shared dependency/cache write is performed.

## Named central suites

The App2 manager should register these two new literal entries in the central
allow-list. Both entries are intentionally under App ownership even though the
first runner executes a Runtime test from its frozen Runtime source. Do not
reuse `full-e2e-three-products`, `e2e-m1-gesture`, or any 013/ordinary lane:
those do not bind this candidate and would produce the wrong qualification
identity.

```text
app normal014-integration-parent-media-accepted bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh run
app normal014-integration-e2e-gate5 bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh run "$PWD"
```

The names are part of the registration contract: both include `integration`,
and the browser lane also includes `e2e`.

The first suite runs exactly one Runtime test through the real Runtime service
boundary:

```text
tests/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_replaces_parent_media
```

It uses `--runxfail` only because the carried d05e test-only marker retains the
strict future-schema xfail around the complete positive body. The positive
assertions are unchanged. The marker's separate current-schema refusal is
present in the private overlay, but is not relabelled as 0.2.14 evidence.

The second suite makes a private App candidate by changing only the temporary
overlay lock selector, then invokes the existing real journey with the exact
selector `M2 real gate 5`. It sets `ASTRID_CHECKOUT` to Agent 3c4,
`ASTRID_RUNTIME_CHECKOUT` to Runtime 202, one private copied interpreter for
both Python entry points, both required `TIMELINE_BUNDLE_*_HEAD` guards, private
Playwright output/cache paths,
and the existing browser serialization lock. It does not use a fake provider,
client shim, or stale prebuilt distribution.

After registration, request each once through the central service and wait on
the returned ID. A cached result is valid only when the suite command and the
exact App snapshot tree are unchanged.

## Runner files

- `normal014-source-common.sh` — exact source, tree, ancestry, schema, manifest,
  and all-artifact byte verification.
- `normal014-parent-media-central.sh` — private Runtime/Agent parent-media
  accepted-positive runner with d05e marker carry, private Python setup, exact
  imports, and collection checks.
- `normal014-app-central.sh` — private App overlay, normal vendor-lock update /
  checks, generated-byte guards, locked public13 graph, private Python setup,
  provider-test and Playwright collection, browser-executable check, and Gate 5
  runner.

Both runners use a disposable copied-interpreter venv rooted below their
per-run temporary directory. It installs only `jsonschema>=4.18`,
`referencing>=0.30`, `PyYAML>=6.0`, `pytest>=8`, and `pytest-timeout>=2.4`;
Agent/Runtime source is supplied through `PYTHONPATH`. Node, Playwright, and
all Vite/Vitest/npm caches are private to the same run. The default trap removes
the complete run root; `NORMAL014_KEEP_TEMP=1` is the explicit diagnostic lease.

These files are external to the repositories and are safe for the central
service to call from its throwaway snapshot.
