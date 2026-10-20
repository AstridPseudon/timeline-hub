# App private392 existing-native environment HTTP proof

## Result

Added the App-owned named integration lane `test:integration:private392-http`.
It delegates to the already source-approved
`scripts/testing/private392-http-runner.sh`; all checkout and interpreter
identity remains caller-supplied. The runner still owns the exact Agent,
Runtime, schema, manifest, bundle, component, driver, lock, clean-tree,
credential/project, outbox, and ambient-environment guards, creates only its
temporary blank listener index, runs one `--no-cache` Vitest selector, and
preserves child status plus EXIT cleanup.

No source pin, generated contract, schema, driver, shared environment,
checkout, package dependency, public lock, or guard was changed.

## Native qualification evidence

The caller-supplied values qualified for the exact pair were:

```text
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-1303ce6b
ASTRID_PYTHON=/home/user/work/venv-app2-native/bin/python
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-f8da4b6d
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-app2-native/bin/python
```

The interpreter is read-only and resolves to `/usr/bin/python3.12`, Python
3.12.3. It imported `astrid` and `astrid_runtime_client` only from the Agent
checkout and `runtime_protocol` only from the Runtime checkout. Additional
read-only imports passed for `runtime_protocol.server`, `runtime_protocol.door`,
`runtime_protocol.service`, `runtime_protocol.cli`, `astrid.sdk.client`, and
`astrid.sdk.timeline.commit`. Both `python -m runtime_protocol.cli --help` and
`python -m astrid --help` exited 0.

Exact source custody observed:

- Agent HEAD `1303ce6be32e7bd96ed5c6b35afcb15819e81b50`, parent
  `e010e6a3868e963471244491bb6672c3e4a5135e`, tree
  `2f2685d85c3f65b458795100a8045371eb19ee06`, clean.
- Runtime HEAD `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`, tree
  `8be43e13acb436120f8a63b1a178d64c49422461`, clean.
- Agent schema SHA-256 `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`.
- App driver SHA-256 `85a6f1b2caa7929fb4f6d29855529b6ff837a4ad293b85dd187d080e74d7b981`.
- App lock SHA-256 `3ee0aa69fbff9faeff76a44aedc4e7fb70a69970ceec25c0fde788dbdb37d873`.
- `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d` passed.

Ambient values `ASTRID_CHECKOUT`, `ASTRID_PYTHON`,
`ASTRID_RUNTIME_CHECKOUT`, `ASTRID_RUNTIME_PYTHON`, `ASTRID_PUBLIC_CHECKOUT`,
`ASTRID_APP_DIRECT_DIST`, and `PYTHONPATH` were unset during qualification.
No credentials or token values were recorded.

The native environment contains the declared Agent/Runtime requirements used
by this proof (`pytest`, `jsonschema`, and `PyYAML`). Optional packages such as
`fastapi`, `uvicorn`, `httpx`, `pydantic`, `cryptography`, and `typer` are not
installed, but the exact Runtime server/door imports and CLI probes pass; no
blind substitution or installation was made. If the central harness reports a
real missing dependency, use its documented private child-environment
provisioning path and preserve the same caller-supplied interpreter seam.

## Checks run

```text
sh -n scripts/testing/private392-http-runner.sh                         PASS
node --check scripts/testing/private392-http-runner.test.mjs             PASS
node --test scripts/testing/private392-http-runner.test.mjs              PASS (1 test)
git diff --check                                                         PASS
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d
                                                                         PASS
node_modules/.bin/eslint tests/integration/runtimePrivate392Consumer.test.ts config/testing/vitest.runtime-restore.integration.config.ts --ext ts --max-warnings 0
                                                                         PASS
node_modules/.bin/tsc --noEmit --pretty false                              PASS
```

No local browser, hosted build, localhost/socket, Runtime process, HTTP/Door
request, or full suite was run.

## Blocker and exact next step

The required single live HTTP/Door proof remains **unverified**. Local socket
execution is prohibited, and the central `suites.conf` still exposes the old
private392 command (hosted build plus the absent `/home/user/work/venv-agent`
and `/home/user/work/venv-runtime` paths). Invoking that entry would violate
the settled no-hosted-build and native-interpreter decisions.

The central test service should register/invoke this App-owned lane exactly
once, with the already-qualified values above:

```sh
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-1303ce6b \
ASTRID_PYTHON=/home/user/work/venv-app2-native/bin/python \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-f8da4b6d \
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-app2-native/bin/python \
npm run test:integration:private392-http
```

That lane runs only
`tests/integration/runtimePrivate392Consumer.test.ts` with `--no-cache` and
retains all merge/replace/raw opaque/order/lostACK/reload/exactretry/rebase/
undo/stale zero-write/zeroLegacy assertions unchanged.
