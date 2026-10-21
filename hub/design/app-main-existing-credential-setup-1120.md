# App Main existing product-credential setup

## Result

Use the existing `DirectHarness.provisionCredential` path in the Main-owned
fixture process. It creates the ephemeral Runtime realm first, starts that
realm's Runtime, provisions a real non-owner product credential through
`POST /v1/credentials`, and writes the credential file privately. The setup
must use `{ seed: false }`; this creates no project, film, media, or browser
activity. Keep the harness alive while Main performs its list phase and the
manager-approved actual phase, then use the existing `harness.stop()` cleanup.

The App helper had one contract defect: it wrote `{token, actor_id}`. The
successful App suite `1c896d690f1e829290d5e3b0745a18240740649c` (the
automatic normal-credential/ACP fixture repair) uses the established
versioned shape. This worker applied that exact minimal correction:

```ts
writeFileSync(
  path.join(this.tmp, file),
  JSON.stringify({ version: 1, scope: 'astrid', token, actor_id: actorId }),
  { mode: 0o600 },
);
```

No token value is printed or copied. The owner credential is read only inside
the helper to authenticate the Runtime provisioning request; it is never the
product credential and is never exported. The product actor remains the
existing `PRODUCT_ACTOR` (`astrid-e2e-product`), not `owner`, `worker`, or an
Agent pack-host actor.

## Exact source and ordering

- `tests/e2e/local/support/harness.ts:32`: existing product actor.
- `tests/e2e/local/support/harness.ts:461-479`: `DirectHarness.start()`.
  `createRealm()` runs before `startRuntime()`, then `provisionCredential()`
  runs before optional seeding. Passing `{ seed: false }` stops before
  `seedRuntime()` and therefore performs no project/film write.
- `tests/e2e/local/support/harness.ts:507-509`: existing Runtime CLI realm
  creation under the harness-owned `<tmp>/realm`.
- `tests/e2e/local/support/harness.ts:516-520`: existing Runtime start using
  that realm and the existing door credential-file path.
- `tests/e2e/local/support/harness.ts:572-588`: existing helper. It reads the
  private owner token, sends the normal Runtime provisioning request with
  `{ actor_id, credential, scope: 'astrid' }`, and persists only the product
  file. Runtime is the issuer; the actor and realm are the values used in
  that request and the just-created `<tmp>/realm`.
- `tests/e2e/local/support/astrid.ts:133-136`: the Agent CLI helper uses the
  same provisioning path. Do not use its `ASTRID_ACTOR` as Main's product
  file; Main must retain `PRODUCT_ACTOR`.
- `/home/user/work/runtime/tests/door_helpers.py:109-115`: corroborating
  Runtime test helper. Its `DoorWorld.provision()` performs the same owner-
  authenticated Runtime route and writes the same version 1/scoped/mode-0600
  product file. It is evidence of the established private helper, not a new
  App API.

The credential JSON has no invented expiry or project fields. Runtime keeps
the issuer/actor/scope and realm binding in its credential store; project and
timeline identity are bound by the normal project API only after the normal
fixture creates its own project. Do not add credential metadata, a new
authmode, API, DTO, or token format to manufacture those bindings. The
`{ seed: false }` setup intentionally leaves project creation to Main's
existing normal path and makes the setup itself non-writing with respect to
film data.

## fa20 guard contract

`scripts/testing/current013-parent-split.mjs:38-49` is the unchanged guard.
It requires `WORKSPACE_RUNTIME_TOKEN_FILE` to be an absolute physical file,
mode exactly `0600`, with JSON fields `version === 1`, `scope === 'astrid'`, a
nonblank actor other than `owner`, `astrid-pack-host`, `admin`, or `worker`,
and a nonblank token. Its error is deliberately generic and does not expose a
secret. The helper correction above is the smallest way for the normal
fixture path to satisfy it; do not weaken this guard.

## Main command and hook

Use these exact pinned checkouts and installed interpreters in Main's existing
runner. The setup hook is intentionally shown as an inline Node command so it
cannot be mistaken for a new product helper. Main must run the list/actual
driver from the same parent process while `harness` remains alive; running
this snippet as a detached preflight and then allowing it to exit deletes the
ephemeral realm and credential during normal teardown.

```bash
APP=/home/user/work/wt/app-m2-main-existing-credential-setup-r69
AGENT=/home/user/work/wt/agt-pin-6efc8150
RUNTIME=/home/user/work/wt/rt-pin-95bd3c5f
AGENT_PY=/home/user/work/venv-agent/bin/python
RUNTIME_PY=/home/user/work/venv-runtime/bin/python

cd "$APP"
ASTRID_CHECKOUT="$AGENT" \
ASTRID_RUNTIME_CHECKOUT="$RUNTIME" \
ASTRID_PYTHON="$AGENT_PY" \
ASTRID_RUNTIME_PYTHON="$RUNTIME_PY" \
node --import tsx --input-type=module <<'NODE'
import { DirectHarness } from './tests/e2e/local/support/harness.ts';

const harness = await new DirectHarness().start({ seed: false });
// Pass these non-secret values to the existing Main list/actual driver in this
// same process. Never print harness.productToken or read the file contents.
process.stdout.write(`${JSON.stringify({
  realm_id: harness.realmId,
  runtime_instance_id: harness.runtimeInstanceId,
  credential_file: harness.credentialPath,
})}\n`);
// Main invokes its existing list/actual phases here, with
// WORKSPACE_RUNTIME_TOKEN_FILE=harness.credentialPath and its existing
// realm/actor/project carriers. Finally call await harness.stop().
await new Promise(() => {});
NODE
```

The shell values are exact Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`
and Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` source pins. The
current split driver independently enforces those values at
`current013-parent-split.mjs:69-95`, and its normal list invocation is
`current013-parent-split.mjs:103-118` (`npm run test:e2e:three-products --
--config playwright.parent-split.config.ts --list`). Main should preserve
that driver and pass only the helper-produced physical credential path; it
must not replace the list/actual path with a direct Playwright or Runtime
request.

## Evidence read and limits

- `fa20fae65fa46b6c81d5c0483e14b33248e4698c`: guard hardening that requires
  trimmed actor/token values and rejects owner/worker-style actors.
- Successful App repair `1c896d690f1e829290d5e3b0745a18240740649c`: exact
  version/scope/mode-0600 persistence correction used here.
- Published013 PASS `1021015715-27912` and native Main95 PASS `7782`: reviewed
  successful App-suite examples; neither authorizes a new credential source
  or bypass of the normal fixture path.

Worker verification, deliberately bounded:

- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts` — passed.
- `node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts` — passed.
- `node --test scripts/testing/current013-parent-split.test.mjs` — not runnable in this image: Node 22.22.0 does not export `SourceTextModule` from `node:vm`; this is an environment failure, not a product assertion failure.
- `git diff --check` — passed.

No daemon, browser, socket, full suite, install, graph, or actual run was
performed by this worker. Main owns the live setup and must report the
resulting list/actual evidence separately.
