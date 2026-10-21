# App2 M2 selected 0342 result: startup boundary diagnosis

## Verdict

The sole authorized selected actual is **not qualified**. It failed at the
first unchanged startup assertion before the selected journey began, so no
legacy writer or row-local leaf is proven dead and nothing is cut.

Central result:

- Result ID: `ap2-m2-selected-approved-real-scope-one-case-0342-ap2-m2-selected-real-p1-history-fixture-fix-1021034300-18585`
- App source: `8e9975005d18c6278000ab4c8cc8b18291d03e12`, tree
  `87d2350417a876e14b81c58b64da29f1a30b35b6`
- Named suite: `ap2-m2-selected-real-p1-history-fixture-fix`
- Exit: 1; one failed test; 112 seconds
- Build: passed; collection was exactly one test in one file

## Exact first boundary

The first actual failure was the original mount assertion in
`tests/e2e/local/three-products.selected-param-dev.spec.ts:30`, called from
line 59:

```text
expect(page.locator('#root > *').first()).toBeAttached({ timeout: 20000 })
Error: element(s) not found
```

The page stayed on the App shell with `Loading project` and an empty `main`.
The preserved network trace records:

```text
GET http://127.0.0.1:37831/runtime-config/v1/workspace.json
HTTP 404
server: AstridRuntime/0.1 Python/3.12.3
```

This is an observed transport/source boundary, not an inference from the
later selected behavior.

## Smallest source diagnosis

The DEV harness starts Vite with `VITE_WORKSPACE_RUNTIME_URL` at
`tests/e2e/local/support/harness.ts:720-724`. The current App config then
declares this proxy at `config/vite/vite.config.ts:92-97`:

```ts
"/runtime-config/v1/workspace.json": { target: runtimeTarget, changeOrigin: true },
```

That forwards the browser's config request to the Runtime HTTP root without
rewriting it. The current Runtime integration route table
(`/home/user/work/runtime/runtime_protocol/door.py:151-193`) contains only
`/v1/...` workspace routes and no `/runtime-config/v1/workspace.json` route;
the Runtime server's route dispatch likewise starts with `/v1/...` handling.
The latest App hub integration checked by this worker is
`976e08c6c8fffd4ebb4e61e8fc1523685a330f87`; it retains the same proxy entry
at line 96. The Runtime integration checked is
`30413e3c3e6db027f450e864ea9cb4a07446475`, whose route table has the same
absence.
The observed Runtime-owned 404 is therefore the first boundary: the App's
same-origin runtime-config proxy points at a Runtime endpoint that does not
serve that path. `src/integrations/runtime/workspaceRuntimeConfig.ts:18-32`
expects that path to return the identity JSON, so the client retains its
loading/unconnected state when it receives the 404.

This report does not choose whether the config endpoint belongs in App Vite
middleware or in the Runtime contract. No cross-repo change is authorized by
this failed result.

## Assertion and change scope

Executed and passed before submission: all required identity/graph/argv/config/
isolation preflight checks, targeted Vitest controls (6 files, 71 tests), the
credential file test (4 subtests), exact one-test Playwright collection,
driver syntax check, and private workspace preflight. The central build also
passed.

Executed in the browser: DEV server startup, navigation, and the first mount
assertion only.

Not executed: seeded timeline opening, exact project/timeline identity, clip
selection, P1 commit, P2 admission, authored-source removal readback, refusal
and dirty-draft assertions, lost acknowledgement, restart/recovery, exact
retry body/key, undo, and zero-legacy-POST assertion.

No source, test, driver, shared file, pin, authority, bootstrap activation,
or legacy writer was changed. There are no live callers changed; the only
selected live caller remains
`tests/e2e/local/three-products.selected-param-dev.spec.ts`.

No test was launched or retried by this worker. The preserved central command
was the single authorized request/wait:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-selected-approved-real-scope-one-case-0342 ap2-m2-selected-real-p1-history-fixture-fix --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Preserved evidence is in the selected worker report and central result log,
including the Playwright trace and error context. Recommended next step is an
orchestrator-owned contract/source repair for the config route, followed by a
new explicitly authorized actual; this worker does not claim that repair or
any selected journey qualification.
