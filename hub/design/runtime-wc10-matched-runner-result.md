# Runtime WC10 matched-runner result

Date: 2026-10-21. Analysis only; no Runtime, Agent, or fixture source was
changed.

The required no-socket preflight under the exact
`/home/user/work/venv-agent/bin/python` found all 54 declared closure
distributions and verified clean source identities:

- fixture `efd8e21347c90cd03bf666bf1c8752fa7b14e595`, tree
  `7ecac255c50d2935ddf9a37d3fc9ba0bda434b60`;
- Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`;
- normal Runtime/client `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`;
- reviewed launcher source `8f70a8184aca5bb61b2fcb133c5cedc3c6e0800a`.

One and only one central request then ran:

```text
request id: rt-m2-wc10-matched-runner-one-execution-0318-wc10-installed-launcher-integration-1021031824-22571
command: env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_wc10_installed_launcher.py::test_wc10_installed_normal_launcher_provider_bootstrap
result: exit=1; 1 failed in 31.26s
```

The private environment was created, all three expected product distributions
were installed, `astrid-runtime up --profile astrid` returned the `wc10` realm
and loopback door, status was healthy, and the isolated child authenticated
and passed `health()`. The project mutation completed in the Runtime realm;
the retained SQLite row and idempotency record exist.

The first failure was `tests/test_wc10_installed_launcher.py:471`,
`KeyError: 'project_id'`. The unchanged WC10 operation expects
`WorkspaceClient.create_project()` to return the project resource directly.
Agent `WorkspaceClient._call_generated` currently returns mutation results as
`{"data": resource, "receipt": receipt}`. The Runtime response/resource path
returns `project_id` inside `data`; the test never reaches later timeline or
provider assertions. This is the exact Agent-client/WC10 assertion-shape
mismatch surfaced by the installed run.

Provider bootstrap, canonical empty timeline read, `bootstrap` history head,
no-`publish_parent_composition`, and later custody assertions are unobserved.
No D13 render, whole-WC10 consumer, pin, publication, or integration-adoption
claim follows. The earlier deselected and missing-closure failures remain
preserved in `runtime-wc10-normal-launcher-proof.md`. No further run is
requested here.
