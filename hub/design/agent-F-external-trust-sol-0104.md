**BLOCKED — missing Runtime source authority.**

Published [evidence/early-interface.txt](/home/user/work/wt/agt-F-external-trust-sol-0104/evidence/early-interface.txt). Neither qualified Runtime `8ea0766f` nor current integration Runtime `458595850c` supplies a Runtime-owned external-pack inventory/capture to the worker. Local state, CLI identity and admission mappings remain caller claims. The retained verified loader authorizes the host installation.

Product and tests are unchanged; neither failed ancestry was ported.

Validation used the brief’s qualified environment:

- `timeout 45 /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider` with these nodes: **12 passed in 35.24s**:
  - `tests/test_generic_host.py::test_admitted_definition_and_source_are_fenced_before_child_dispatch`
  - `tests/test_generic_host.py::test_external_pack_import_root_is_fenced_before_direct_command`
  - `tests/core/execution/test_generic_host_actions_v3.py::test_whole_pack_mutation_invalidates_admission`
  - `tests/core/execution/test_generic_host_actions_v3.py::test_admission_identity_is_required`
- Independent source probes: **6/6 reached the intercepted launch seam**, covering forged roots, descendant symlink, three package collisions and mutation after validation. No child executed.
- `ruff check --no-cache --output-format=json astrid/core/execution/generic_host.py`: **101 diagnostics**, exact parent identities; zero additions/removals.
- `/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --cache-dir=/tmp/w-218b61fdb3/mypy-cache --no-pretty astrid/core/execution/generic_host.py`: **139 diagnostics**, exact parent identities; zero additions/removals.
- `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004`, `scripts/artifact_manifest.py --check`, and `git diff --check`: **passed**.

The Runtime owner must provide the private authenticated source-capture handoff before implementation can proceed. Candidate installed-positive qualification remains unverified; all original full-suite failures remain open. No full suite or unchanged original-positive retry ran.

Created the required `BLOCKED` marker and conventional commit message. No `DONE` marker.