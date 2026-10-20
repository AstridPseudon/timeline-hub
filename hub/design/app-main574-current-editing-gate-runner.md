# App MAIN574/public13 editing browser gate runner

Status: prepared only. The manager marker
`managers/app/notes/root-main574-public13-READY` is absent, so no browser,
build, Runtime socket, or central lane was invoked.

The App worktree adds `scripts/testing/main574-public13-editing.mjs` and its
offline node-test guard. The runner reads the manager marker as the sole
source authority. It requires literal `AppSHA/AppTree`, `AgentSHA/AgentTree`,
and `RuntimeSHA/RuntimeTree` values (with `RootSHA/RootTree` accepted only as
the marker's App aliases), then checks the live checkouts' exact HEAD/tree and
clean status before launching anything. It also checks the Runtime 0.2.13
75-artifact identity, App public13 archive `9412ae25...` with 77 regular
members, Agent's retained public12 archive, and the existing normal locks and
metadata. The old Root7413 result is not reused or relabelled.

The native lane delegates to the existing three-products M1/Gate-5 cases.
The separate `cold-open` lane delegates to the existing Unicode rename case;
the optional `labels` lane is available only if the manager determines the
MAIN574 Inspector join needs it. No assertions, fixtures, opaque settings, or
product/schema code were copied or changed.

After READY, the central worker must provide explicit absolute values for:

```sh
TIMELINE_MAIN574_PUBLIC13_RUN=1
TIMELINE_MAIN574_PUBLIC13_PRIVATE_ROOT=/tmp/<owned-run-root>
ASTRID_CHECKOUT=/abs/final-agent-checkout
ASTRID_RUNTIME_CHECKOUT=/abs/final-runtime-checkout
TIMELINE_MAIN574_PUBLIC13_RUNTIME_PRODUCER_CHECKOUT=/abs/final-runtime-checkout
ASTRID_PYTHON=/abs/final-agent-venv/bin/python
ASTRID_RUNTIME_PYTHON=/abs/final-runtime-venv/bin/python
```

The manager must register a new exact-source central suite for each required
lane, using the marker's literal identities in the command/cache identity.
Run native3 and cold-open1 separately; collect actual test counts. The
runner supplies exact bundle pins to the child and uses an owned temporary
`node_modules` overlay, `TMPDIR`, `XDG_CACHE_HOME`, npm/Playwright/Vitest
caches, and output directory. Shared dependencies and caches remain read-only.

Offline preparation evidence:

```text
node --check scripts/testing/main574-public13-editing.mjs       PASS
node --test --test-reporter=spec scripts/testing/main574-public13-editing.test.mjs  PASS (1 file-level test)
git diff --check                                             PASS
```

No browser, build, install, full suite, TypeScript check, frame/PCM parity,
or central test service request was made.
