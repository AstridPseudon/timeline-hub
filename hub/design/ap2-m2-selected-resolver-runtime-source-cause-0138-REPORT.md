# AP2-M2 selected resolver/runtime source-cause report

## Result

No App fixture or environment correction is justified. The selected-element
producer completes successfully in the retained gate, and the Vite child
imports the frozen Agent 8130 and Runtime 2c4 source trees. The missing
`runtime-connection-status` is not a resolver failure.

The exact first failed request in gate 0128 is:

```text
2026-10-21T01:33:16.255Z
GET http://127.0.0.1:40165/runtime-config/v1/workspace.json
404 Not Found
```

This request repeats. The next distinct failures are the ACP bridge requests
(`GET /api/astrid/acp/agents` and project chat), both 500. They are unrelated
to the selected-element admission. No gate was retried.

## Selected producer trace

The retained fixture helper starts Vite with the private qualified fixture
environment and passes these source/runtime controls to the child:

- Python executable: `/home/user/work/venv-app2-native/bin/python` from the
  qualified central runner (`ASTRID_PYTHON` and `ASTRID_RUNTIME_PYTHON`).
- Agent source: the per-run frozen checkout at `sources/agent`, verified at
  commit `8130a401bf44a518d5a40ae274d398b8c560be55` and tree
  `236c3e57e...`.
- Runtime source: the per-run frozen checkout at `sources/runtime`, verified
  at commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a` and tree
  `7ab412cc...`.
- Vite resolver environment: `ASTRID_CHECKOUT` points to frozen Agent,
  `ASTRID_RUNTIME_CHECKOUT` points to frozen Runtime, and
  `ASTRID_ELEMENT_RESOLVE_COMMAND` is the JSON argv prefix below.
- The helper's effective child `PYTHONPATH` is the frozen Runtime root followed
  by the frozen Agent root; the central runner also supplies Runtime's
  `packages/python` root before the helper's explicit runtime environment is
  applied.
- Realm, project, endpoint, and credential-file environment are all supplied
  by the existing selected fixture helpers. The selected Agent child uses the
  private selected credential file through `ASTRID_RUNTIME_CREDENTIAL` and
  `ASTRID_TIMELINE_EVAL_CREDENTIAL`; the Vite Runtime client uses the private
  product credential file. No token is put in an argv, URL, browser field, or
  report.

The actual resolver invocation assembled by the Vite admission route is:

```text
<python> -m astrid.core.element.cli project-pack resolve \
  --realm <fixture-realm> --project <runtime-project> \
  --pack <admitted-pack> --element selected_param_fixture \
  --kind effect --revision <admitted-revision>
```

The Vite route executes that command, parses its JSON, reads the bound Runtime
document with `AstridRuntimeClient.getDocument(projectId, elementId)`, and
validates the returned immutable snapshot. In the retained trace:

- `/api/astrid-element-admissions` returned 200 with a digest and virtual
  module URL, rather than the prior resolver 409.
- Runtime health, handshake, realm, project, timeline, revision, object,
  commit, and inspect requests returned 200.
- The inspect response contains the selected P1 exact element reference.
- The selected Agent and Runtime imports were independently checked from
  private archives of the two frozen commits; `astrid.__file__` and
  `astrid_runtime.__file__` resolved inside those archives.
- No selected source module request failed. Vite stderr contained only
  non-fatal bundler warnings; no Vite/module import error was present.

## Why the status element is absent

The selected DEV child does not set `VITE_RUNTIME_ORIGIN`. The current
`RuntimeConnectionProvider` therefore treats this as same-origin DEV mode,
does not gate the children, and does not render the hosted
`runtime-connection-status` pill. Adding a forced state, changing the product
bootstrap, or changing the assertion would violate the task constraints and
would change the intended hosted-vs-DEV connection semantics.

The first 404 is the direct Runtime's missing `/runtime-config/v1/workspace.json`
route through the Vite proxy. It is the first failed request, but it is not a
selected-element producer failure: the subsequent direct Runtime path is
healthy and the selected admission succeeds.

## Verification

Passed:

```text
node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts
  1 test passed
npx eslint --no-cache tests/e2e/local/support/harness.ts tests/e2e/local/support/selected-param-credential.test.ts
  passed
git diff --check
  passed; worktree unchanged
```

Offline frozen-source checks passed with private temporary archives of Agent
8130 and Runtime 2c4:

```text
import astrid, astrid_runtime
  resolved to the private frozen Agent/Runtime archive roots
python -m astrid.core.element.cli project-pack resolve --help
  passed
full resolver argv composition check
  passed, including realm/project/pack/element/kind/revision arguments
```

No source files were changed. The existing credential controls and all P1/P2,
refusal, draft, retry, reload, and undo assertions remain untouched.

## Recommended next step

Treat `/runtime-config/v1/workspace.json` as the next integration issue if a
workspace-config response is required. Separately, the selected DEV journey
needs a DEV-appropriate connection-status expectation or an explicitly gated
hosted configuration; this worker did not alter either because that would be
a product bootstrap/assertion change, not a resolver or fixture correction.
