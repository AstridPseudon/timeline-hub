# WC10 installed-launcher fixture diagnosis

## Disposition

Diagnosis is complete. No proof rerun was made and no product source was changed. The four preserved runs do not establish a normal Runtime product defect. They establish an invalid installed-package fixture, an incomplete dependency closure, and an invalid credential-file/client contract. The last run reached a started Runtime before the fixture passed the credential JSON object as an HTTP bearer value.

The relevant source is Runtime `8f70a8184aca5bb61b2fcb133c5cedc3c6e0800a` (`fix(runtime): forward validated authoring profile on local launch`), with the installed Agent source pinned to commit `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`. The installed Runtime/client normal artifact evidence is the normal `95bd3c5` pair described by the R4 control documents. The 8f70 change is not implicated: its validated `astrid` profile forwarding is what allowed the later run to start the provider-backed daemon.

## Evidence from all four preserved runs

All four result directories used the same central command:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/test_timeline_commit_integration.py tests/test_wc10_installed_launcher.py
```

The installed-launcher failure in each run was:

| Run | Observed failure | Exact classification |
| --- | --- | --- |
| `30575` | `test_wc10_installed_launcher.py:110` compared the fixture's installed site-packages path under `/home/user/work/wt/.test-...` with the client parent under `/tmp/pytest-of-root/.../stage1-runtime0/venv/...`. | Setup/path-identity failure. The test constructed two different installation locations; this is not a Runtime import or launcher failure. |
| `3875` | Runtime startup exited with `No module named 'jsonschema'` in `runtime.log` at `test_wc10_installed_launcher.py:155`. | Import/dependency-closure failure. The wheel was installed with `--no-deps`, so a declared Runtime dependency was absent. The later `No selected runtime owner` cleanup error is secondary to startup never completing. |
| `29713` | Runtime startup exited with `No module named 'yaml'` at `test_wc10_installed_launcher.py:190`. | Import/dependency-closure failure. The first hand-added closure was still incomplete; PyYAML is an exercised Agent/provider dependency. This is not evidence of a normal Runtime defect. |
| `21154` | Startup succeeded, but the embedded client failed at `test_wc10_installed_launcher.py:241` with `Invalid header value b'Bearer { ... "token": ... }'`. | Fixture contract failure. Runtime's discovered `credential_file` is a JSON object; the fixture read and passed the entire JSON text as the bearer token. The installed client expects the decoded `credential["token"]` string. No HTTP operation was reached. |

The same command also selected two unintended old M1 nodes from `tests/test_timeline_commit_integration.py`. The named `commit-integration` suite is hardcoded in `suites.conf` to run that file, and the test service appended the requested installed-launcher file. Consequently every run was `test_timeline_commit_integration.py` plus the requested file. The two old M1 nodes failed their pre-existing baseline receipt assertion (`__runtime_idempotency_result_expired_v1` versus the stored baseline); they are unrelated to this fixture diagnosis and were not changed.

## Required installed package and dependency closure

The fixture must be one coherent, non-editable installation made from the exact Runtime/client and Agent wheels, not a wheel plus a sequence of guessed symlinks. Runtime declares `jsonschema>=4.18` and `referencing>=0.30`; its portable closure includes:

```text
jsonschema
jsonschema-specifications
referencing
attrs
rpds-py
typing-extensions  (for the supported-Python portability envelope)
```

The pinned Agent package declares the following direct dependencies and the fixture must include their complete transitive closure, including native extensions and package data where applicable:

```text
openai>=1.55,<3
scenedetect[opencv-headless]==0.6.4
anthropic>=0.40.0
google-genai>=1.15.0
filelock>=3.13
PyYAML>=6.0
jsonschema>=4.0
referencing>=0.30
pillow>=12.2,<13
python-dotenv>=1.0
fal-client>=0.7.0
xxhash>=3.4
PyJWT[crypto]>=2.8
```

For the exercised provider-backed empty timeline path, the observed import minimum is the Runtime closure above plus `yaml`/PyYAML and the corresponding Agent package modules. That minimum is useful as a preflight diagnostic, but it is not a valid substitute for installing the complete declared Agent closure. The old `_link_runtime_dependencies` approach was inherently incomplete: it added `jsonschema`, `referencing`, their selected companions, then YAML one package at a time, and selected a shared site using the ambient runner interpreter. It should be replaced by one private fixture environment populated atomically from a wheelhouse or by a complete, prevalidated set of read-only links from the exact shared environment. Shared dependency files must remain untouched.

The required normal construction is:

1. Build the Runtime wheel, Runtime client wheel, and Agent wheel from the exact pinned source trees into a private wheelhouse. Do not use editable installs, `PYTHONPATH`, source-checkout overrides, or `--no-deps` unless the entire declared closure has already been populated in that same private environment.
2. Install the two Runtime packages, the pinned Agent package, and the full dependency closure into one private environment. Confirm that each imported package's resolved `__file__` is inside that environment and that its package metadata and data files are present. The shared venv may be a read-only source of bytes, but must not be modified.
3. Construct the normal profile manifest with `profile: "astrid"`, `runtime_environment` set to that private environment, and `runtime_checkout`/`source_checkout` set to the actual installed site-packages carrier accepted by Runtime's existing source validation. Those paths must be absolute and must satisfy the existing custody/source checks; do not add metadata, health, auth, or source overrides.
4. Launch through the existing normal command path (`astrid-runtime` with `--profile astrid`, the manifest, normal data root, and hosted origin). The existing 8f70 boundary then forwards `--authoring-profile astrid` to the fixed child command. Runtime's existing owner lock, bootstrap token, native custody, discovery, readiness, and fixed provider loader remain the authority. Do not copy a wrapper from another source tree.
5. At the client boundary, parse the discovered credential file as JSON and pass only its string `token` field to `WorkspaceClient`. The JSON file's actor, scope, version, and token fields are Runtime's existing credential contract; passing the serialized object as an HTTP header is invalid.

This construction addresses all four observed installed-fixture causes in a single setup. It does not require or justify changing Runtime product code.

Resolving the Agent requirements on the supported Python 3.13 environment,
including the `opencv-headless` and `crypto` extras, produced this
54-distribution closure in the shared dependency inventory:

```text
aiofiles, annotated-types, anthropic, anyio, asyncstdlib, attrs,
certifi, cffi, charset-normalizer, click, cryptography, distro,
docstring-parser, fal-client, filelock, google-auth, google-genai, h11,
httpcore, httpcore2, httpx, httpx-sse, httpx2, idna, jiter, jsonschema,
jsonschema-specifications, msgpack, numpy, openai, opencv-python-headless,
pillow, platformdirs, pyasn1, pyasn1-modules, pycparser, pydantic,
pydantic-core, pyjwt, python-dotenv, pyyaml, referencing, requests,
rpds-py, scenedetect, sniffio, tenacity, tqdm, truststore,
typing-extensions, typing-inspection, urllib3, websockets, xxhash
```

The complete installed carrier is therefore the three product distributions
(`astrid-runtime`, `astrid-runtime-client`, and pinned `astrid`) plus every
distribution in that closure, with exact versions selected by the approved
wheelhouse. This is a closure inventory, not permission to mix ambient
versions or omit packages that are not imported by the first preflight.

## Exact one-shot suite for the manager

Do not use the `commit-integration` suite. If the manager elects to perform the single corrected proof, the supported exact-one-node request is:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-wc10-installed-fixture-cause-only-0258 targeted --files "tests/test_wc10_installed_launcher.py::test_wc10_installed_normal_launcher_provider_bootstrap") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

That command is recorded for the manager only; this worker did not request or run it. It targets the explicit supported fixture node and contains no hardcoded M1 integration file.

## Verification performed here

Read-only inspection covered the plan, the stopped predecessor WIP and branch, all four preserved result summaries/logs, Runtime `8f70`, the pinned Agent metadata, the fixture source, and `suites.conf`. The current worktree remains clean at `8f70a81`. No launcher, socket, HTTP, pytest integration, full-suite, browser, render, or proof rerun was performed, and no test-service request was made.

