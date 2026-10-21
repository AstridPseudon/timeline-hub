# Runtime D13 installed dependency authority

Status: bounded carrier identified; no Runtime product change made.

## Decision

Use one private, non-editable Python environment as the existing carrier for
both the Agent parent and Runtime child. The carrier is the environment's
selected executable and installed package tree, not
`SourceProfile.runtime_checkout` and not `ASTRID_RUNTIME_CHECKOUT`.

The exact profile shape remains the existing one:

```json
{
  "profile": "astrid",
  "runtime_environment": "/private/venv",
  "runtime_checkout": "/private/venv/lib/python3.13/site-packages",
  "source_checkout": "/private/venv/lib/python3.13/site-packages"
}
```

The two checkout values are retained provenance fields. They are not import
roots. The private venv must contain the exact Runtime, generated client, and
Agent wheels plus the complete declared dependency closure; do not populate it
with `PYTHONPATH`, editable installs, or links into a shared environment.

## Why this is an existing authority path

Runtime already selects the installed executable from `runtime_environment`:

- `astrid_runtime/runtime_boundary.py:180-207` validates the environment and
  treats the checkout as provenance; its docstring explicitly says an editable
  checkout is never an import or launch fallback.
- `astrid_runtime/runtime_boundary.py:244-258` resolves the environment's
  `python` and launches `python -m runtime_protocol start`.
- `astrid_runtime/runtime_boundary.py:440-446` launches that child with the
  existing environment unchanged; it does not construct `PYTHONPATH` from a
  checkout.
- `astrid_runtime/runtime_boundary.py:626-642` imports the generated client
  normally, with no path mutation.

Runtime's child then uses the existing fixed provider seam. The low-level CLI
defaults to neutral at `runtime_protocol/cli.py:62`; when the existing approved
product-profile forwarding is present, `runtime_protocol/cli.py:376-394`
passes the explicit profile to `RuntimeDaemon`, which loads the fixed Agent
factory at `runtime_protocol/timeline_commit_provider.py:70-93` before
readiness (`runtime_protocol/daemon.py:235-258`). Timeline creation installs
the authoritative bootstrap publication at
`runtime_protocol/service.py:1697-1743`.

Upstream Main's installed Agent parent has the matching no-source-import
boundary:

- `astrid/sdk/host_bootstrap.py:691-727` selects the `installed` execution
  profile, probes the selected interpreter with `-I` from a temporary cwd, and
  requires host/child/action/client/sdk origins to be real files beneath the
  selected installed product root with no symlinked path component.
- `astrid/sdk/host_bootstrap.py:733-748` removes `PYTHONPATH` for that profile.
- `astrid/sdk/host_bootstrap.py:854-864` repeats the same origin check for a
  parked/ordinary child launch and removes `PYTHONPATH` there too.
- `astrid/sdk/autobootstrap.py:125-138,455-482` invokes the installed
  `astrid-runtime` command and carries only the existing Runtime identity and
  credential fields. It does not need a Runtime source-root field.

The executable discriminator is therefore the existing selected venv Python,
not a socket or a path supplied by the caller: Agent's `-I` origin probe and
Runtime's `platform.venv_python(...)` selection must resolve the same private
environment. The child inherits no checkout-derived import path.

## Current fixture gap and smallest remedy

Runtime's existing installed fixture at `tests/conftest.py:112-180` builds and
installs only the Runtime and generated-client wheels. It is a valid Runtime
installed fixture, but it cannot qualify D13 because it has no installed Agent.
The available shared environments confirm the gap: `venv-runtime` and
`venv-agent` have no installed `astrid_runtime`, `runtime_protocol`, client,
or Agent package under isolated import; `venv-agent-child-s2` has Agent and the
client from a different revision but no Runtime.

The smallest owner-owned fixture correction is one private wheelhouse and one
atomic installation of the exact Runtime, client, and Agent wheels with the
full declared Agent closure. The separate WC10 fixture diagnosis records the
observed incomplete-closure failures (`jsonschema`, then `yaml`) and the
credential-file mistake; it also lists the Agent metadata dependencies. Do not
repeat its guessed dependency symlink approach. The fixture must instead prove
that every imported product/dependency origin is inside the private venv and
then use the existing normal launcher command:

```text
astrid-runtime up --profile astrid --data-root <support-root>
```

The client must parse the existing discovered credential JSON and pass its
string `token` member. No bootstrap JSON field, DTO, token, environment map,
ABI, framework, metadata override, or new Runtime source-selection mechanism
is needed.

## Important current-tree hold

The current Runtime integration tree is `be8d254`, whose
`astrid_runtime/runtime_boundary.py:244-258` still emits the neutral default
argv without `--authoring-profile`. The already-reviewed owner change is
`8f70a8184aca5bb61b2fcb133c5cedc3c6e0800a` (its fixed boundary maps the
validated `astrid` profile to the existing `--authoring-profile astrid` CLI
option, while preserving neutral low-level defaults). The installed D13 proof
must run only after that existing Runtime launch precondition is present in the
integration tuple; the fixture carrier does not repair provider selection.
This is a landing/integration hold, not a request to promote
`runtime_checkout` or to add a new carrier field.

## Evidence

Focused no-socket Runtime checks on the current worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_zero_shim_boundary.py::test_connect_uses_installed_client_without_mutating_import_path \
  tests/test_zero_shim_boundary.py::test_start_does_not_inject_checkout_into_child \
  tests/test_runtime_boundary.py::test_worker_profile_is_validated_through_installed_source_boundary \
  tests/test_runtime_boundary.py::test_startup_admission_budget_is_validated_and_forwarded
```

Result: **5 passed in 0.43s** (the start test is parametrized for Linux and
Darwin). No socket, HTTP, browser, renderer, full, or native run was made.

The rejected Agent proposal remains rejected: an ambient
`ASTRID_RUNTIME_CHECKOUT` can be foreign, nonexistent, or symlinked and must
never become child `PYTHONPATH`. No part of this remedy uses it.

