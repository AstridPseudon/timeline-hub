# AP2-M2 selected after handshake: causal source report

## Result

The first causal refusal after the bridge 503 repair is a canonical project-pack resolver invocation failure in the selected DEV fixture. The Runtime and Astrid bridge negotiation succeeded; the App then attempted exact pack admission with a malformed native resolver argv.

The smallest repair is in the existing selected DEV harness only:

```text
before: [python, "-m", "astrid.core.element.cli"]
after:  [python, "-m", "astrid.core.element.cli", "project-pack", "resolve"]
```

The Vite host already appends the scoped exact-ref flags. An offline regression now locks the command prefix in `selected-param-credential.test.ts`. No product API, DTO, store, authority, catalog, or source fallback was added.

## First refusal evidence

Retained real-gate trace:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/`

The failing request was:

```text
POST http://127.0.0.1:43617/api/astrid-element-admissions
status: 409 Conflict
body: {"projectId":"7e4646cd9ddc4b28b9acc05721ab3f88","refs":[{"id":"selected_param_fixture","kind":"effect","packId":"project_6b796af66e11c1421ee3","revision":"sha256:4d324e87e1bafe8a2fbe4e926ecc67bb30da94069a188da0eb34ca84ae11e464"}]}
```

Response body:

```text
{"error":"Error: Canonical element resolver failed: usage: python3 -m astrid elements [-h] [--project-root PROJECT_ROOT]
                                  [--pack-root PATH]
                                  {list,ls,search,inspect,validate,project-pack}
                                  ...
python3 -m astrid elements: error: argument command: invalid choice: '956895ca96d74936b35b1e8d55daa613' (choose from 'list', 'ls', 'search', 'inspect', 'validate', 'project-pack')
"}
```

This is a source-module/canonical resolver failure, not another timeout: the CLI received the realm as its command because `project-pack resolve` was omitted.

Actual caller chain:

1. `src/tools/video-editor/contexts/VideoEditorProvider.tsx:268-271` sets the selected exact ref scope and calls `refreshAdmittedElements()`.
2. `src/tools/video-editor/runtime/admitted-elements.ts:57-78` POSTs that scope to `/api/astrid-element-admissions`.
3. `config/vite/astridElementAdmissions.ts:177-189` parses the scope and calls `selectProjectElements`.
4. `config/vite/projectElementSelection.ts:72-75, 102-108` calls the configured `resolveRecord` for the exact ref.
5. `config/vite/vite.config.ts:102-107` runs `execFile(command[0], [...command.slice(1), '--realm', ..., '--project', ..., '--pack', ..., '--element', ..., '--kind', ..., '--revision', ...])`.
6. The selected harness supplied the incomplete command at `tests/e2e/local/support/harness.ts:751`; the repaired harness now supplies the `project-pack resolve` prefix.

## Boundary checks

- The earlier `GET /api/astrid/v1/health` 503 (`astrid_bridge_auth_not_configured`) is repaired by the preserved four-line bridge env change from `1d9299867`.
- In the retained gate, bridge health and handshake were 200; Runtime health, handshake, realm, project, timeline, inspect, revision, and task reads were also 200.
- The normal P1 seed succeeded before the UI attempt: the retained Runtime history contains the native `clip.set-element` and `clip.set-params` operations and the exact P1 `selected_param_fixture` ref/document pin.
- The selected UI journey remained unverified: the prior gate stopped on the missing `[data-testid="runtime-connection-status"]` connected pill after 20 seconds, while the editor was mounted. I did not change that assertion or invent a timeout; it needs a later real-gate rerun after this source fix.
- Source tuple `8130/2c4/public13` remains untouched and frozen. Existing P1/P2, refusal, draft, retry, and undo assertions remain untouched.

## Verification

Passed:

```text
node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts
# 1 test file, 1 pass, 0 fail

npx eslint --no-cache tests/e2e/local/support/harness.ts tests/e2e/local/support/selected-param-credential.test.ts
# passed
```

No browser journey, central request-test, full suite, or live-socket rerun was performed after the source review, per task instructions.
