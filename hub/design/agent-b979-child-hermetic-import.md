# Gate7 hermetic installed-child diagnosis

Date: 2026-10-21  
Scope: only the installed-child CLI/doctor prerequisite; no package install,
build, daemon, socket, renderer, model, browser, or full-suite action.

## Finding

The b979 child is not a coherent installed Agent + Runtime pair. It contains
the installed Agent and its vendored `astrid_runtime_client`, but it does not
contain the Runtime's `runtime_protocol` package (nor `astrid_runtime`). The
normal help path works because it does not import the Runtime observer. The
normal doctor path cannot reach Runtime observation: its direct dependency
fails with `ModuleNotFoundError: No module named 'runtime_protocol'`.

This is an installed-child profile/provisioning gap, not evidence of a Main497
product regression and not an extrapolation to the continuing full21969
failures.

## Hermetic evidence

The existing environment was used read-only:

```
/home/user/work/venv-agent-child-published14-b9797941
Python 3.13.16
```

Each probe ran from `/tmp` with `python -I -B` and a clean environment
containing only `PATH`, `HOME=/tmp`, `LANG`, `LC_ALL`, and `TMPDIR`.

Module origins from `importlib.util.find_spec`:

| Module | Result |
| --- | --- |
| `astrid` | `/home/user/work/venv-agent-child-published14-b9797941/lib/python3.13/site-packages/astrid/__init__.py` |
| `astrid.core.gateway` | same child `site-packages/astrid/core/gateway/__init__.py` |
| `astrid.sdk.documents` | same child `site-packages/astrid/sdk/documents.py` |
| `astrid_runtime_client` | same child `site-packages/astrid_runtime_client/__init__.py` |
| `runtime_protocol` | not found |
| `astrid_runtime` | not found (`ModuleNotFoundError` from `find_spec`) |

Observed commands and results:

* `python -I -B -c 'import astrid, astrid_runtime_client; ...'`: exit 0.
  The installed client reports contract `0.2.14`, protocol `workspace.v1`,
  component manifest
  `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`,
  schema `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`,
  and 133 operations.
* `python -I -B -c 'import runtime_protocol'`: exit 1, exact traceback ends
  with `ModuleNotFoundError: No module named 'runtime_protocol'`.
* `python -I -B -c 'import astrid.sdk.documents'`: exit 1, at installed
  `astrid/sdk/documents.py:19`, with the same exact missing-module error.
* `python -I -B -m astrid --help`: exit 0 and prints the seven-family
  gateway help.
* `python -I -B -m astrid doctor --help`: exit 0 and prints the normal
  read-only doctor usage.
* `python -I -B -m astrid doctor --json`: exit 1. The public gateway reports
  an `UnboundLocalError` (`RuntimeCLIError` referenced before assignment),
  which masks the import failure while `astrid.core.gateway.diagnostics` is
  imported. A direct import of that module gives the underlying exact
  `ModuleNotFoundError` at `diagnostics.py:13`:
  `from runtime_protocol import platform`.
* `astrid-tools doctor --json`: same exit 1 and same masking wrapper output.

No daemon, bootstrap, or socket was started by these probes. The existing
central full21969 job was neither requested nor cancelled/rerun; its running
state was not used as product evidence.

## Source and contract comparison

Main497's source has the same dependency at
`astrid/sdk/documents.py:19` (`from runtime_protocol import platform`) and
`astrid/core/gateway/diagnostics.py:13`. The Agent project metadata at
`pyproject.toml:10-31` declares the normal Agent dependencies but no
`astrid-runtime`, `runtime_protocol`, or equivalent Runtime distribution. The
installed `astrid-0.1.0.dist-info/METADATA` confirms the same omission:
`importlib.metadata.requires("astrid")` has no Runtime/Protocol requirement.
That explains why an Agent-only child can import `astrid` but cannot import
Runtime-backed modules.

The client itself is coherent. Its installed
`astrid_runtime_client/contract_metadata.py` hash is
`cdedeb72880102ff6557320d908eac9068470b5088256c4441514e9d7db40514`, equal
to the current Agent copy and to the generated client at both immutable
Runtime refs:

* Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`;
* compatible Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d`.

Both Runtime refs have the same relevant generated metadata:
`workspace.v1`, schema digest
`sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`,
component manifest digest
`sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`,
133 operations, and identical `contract/artifacts.json` hash
`a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`.
The Runtime artifact version in both is
`sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.

## Existing minimal coherent-pair fixture recipe

If the manager elects one later profile, use the existing installed-artifact
recipe, not a new field or authority:

1. In a private disposable venv, install the exact noneditable Agent wheel
   for the Main497 Agent tree and the exact Runtime wheel from Runtime
   `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / artifact version above, with
   the Agent wheel's vendored client verified against the client hash above.
   Use the existing `docs/setup/release-recipe.md` wheel install shape
   (`pip install --no-index --no-deps`), and verify origins with its existing
   installed-artifact harness. Do not add a checkout to `PYTHONPATH`.
2. Retain the existing Runtime profile carrier at
   `<support-root>/runtime/source-profiles/astrid.json`, with the already
   defined `SourceProfile` fields: `profile: "astrid"`, absolute
   symlink-free `runtime_checkout` and `source_checkout` both pointing at the
   installed package root, `runtime_environment` pointing at that same venv,
   and `runtime_command: []`. Use the existing `protocol_version:
   "workspace.v1"` and `schema_version: "workspace-schema-v1"` values.
3. Keep the profile in the existing catalog/source-profile carrier. Runtime
   resolves `<source_profiles_dir>/astrid.json` (`astrid_runtime/bootstrap.py:
   253-257`), validates the absolute/symlink-free paths and compatible
   protocol/schema (`:341-361`), and launches the selected venv's Python
   (`runtime_boundary.py:244-258`). This is the existing authority boundary;
   no new field, scope, checkout, or ambient `PYTHONPATH` is needed.
4. Re-run only the same clean `-I -B` origins plus `python -m astrid
   --help` and `python -m astrid doctor --json` contract probes. A passing
   result requires `runtime_protocol` and `astrid_runtime` to resolve inside
   the selected installed environment and the doctor result to be a normal
   Runtime observation, not a wrapper traceback.

The existing Runtime Stage-1 fixture demonstrates the private-copy/build and
offline two-wheel pattern at `tests/conftest.py:111-180` in the Runtime
repository. This report does not run or modify that fixture, install any
package, or select a later profile.

## Tests / status

No repository test suite was run: this was a bounded diagnosis, and the task
explicitly prohibited a full/cancel/rerun. The worktree is unchanged. The
central full21969 run remains separate and unclassified by this report.
