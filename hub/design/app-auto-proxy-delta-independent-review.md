# App M2 automatic proxy delta independent review

## Verdict

**APPROVE the exact cumulative delta `29ca799583f66cf2a6338b0191a2c5618d1e6c0c` from `tl/app-m2-auto-current-root-proxy-gate` for the requested proxy/security scope.**

This approves the new credential parsing/startup/profile wiring, operation-handle lifetime and header/origin controls, and the strict test setup only. It does **not** approve automatic activation, task admission, placement completion, or retirement without the actual central gate.

## Review findings

- `scripts/runtime-discovery-proxy.mjs:66-85` uses `WORKSPACE_RUNTIME_TOKEN_FILE` for the product credential while retaining the discovery endpoint and realm identity. It requires version 1, `astrid` scope, a non-forbidden product actor, a non-empty token, a selected realm, a runtime instance, and a realpath-equal realm root. Explicit non-`astrid` `source_profile` values remain rejected. Allowing an absent `source_profile` is compatible with the current `runtime_protocol` catalog, whose realm rows do not publish that provenance field; it is not an origin or credential loosening.
- `createRuntimeOperationRegistry` snapshots endpoint, token, identity, and dispatch into each handle entry. Dispatch uses that frozen entry and does not reread discovery per request. `acquire(predecessor)` retires the predecessor before reading the replacement snapshot, so replacement failure cannot leave the old handle active. A replacement gets a new handle and identity snapshot; old in-flight work is cancelled.
- The operation Vite route has no startup bearer, rewrite, or ordinary cache policy. The middleware still enforces exact loopback same-origin origin/Host/Fetch-Site rules, strips browser credentials and nominated hop headers, and forwards the operation handle only to the credential-owning proxy. The proxy adds only the pinned upstream bearer and returns an allowlisted response-header set with `no-store`; no secret, operation, cookie, authorization, or hop header leak was found.
- The ordinary `/api/runtime` route continues its pre-existing per-request discovery behavior for non-operation consumers. Automatic operation requests are routed by the operation prefix/handle branch and cannot fall back to that path or rediscover on dispatch.
- The harness now passes the scoped product credential explicitly, uses a dynamic operation origin/port, isolates Vite cache output under the harness temp directory, and extracts the tracked Composition artifact only into that temp directory. The added diagnostics and UI setup preserve the original strict task/read-closure, reconnect, lost-ACK, exact body/key/receipt retry, reload, undo, operation-route, and zero-legacy-POST assertions. No original strict assertion was weakened; the local-mode readiness fallback is followed by event, task, operation, commit, and canonical-state assertions.

## Controls run

All controls were run against this worktree and passed:

```text
node --check scripts/runtime-discovery-proxy.mjs                         PASS
node --test --test-name-pattern='^pure:' scripts/runtime-discovery-proxy-operation.test.mjs
                                                                          PASS (exit 0; pure-only selection, no socket cases)
node --input-type=module <inline pure proxy/security assertions>         PASS
/home/user/work/app/node_modules/.bin/eslint --no-cache --max-warnings 0 \
  config/vite/vite.config.ts tests/e2e/local/auto-real-proxy.spec.ts \
  scripts/runtime-discovery-proxy.mjs config/vite/runtimeProxy.ts        PASS
git diff --check                                                        PASS
```

The inline pure probe covered exact origin/Host admission, path traversal rejection, product credential override, endpoint/token pinning, retirement before failed replacement, new-token rebind, and Vite operation-vs-ordinary proxy options. It used temporary files only and opened no sockets.

No full suite, browser/e2e run, live-socket test, TypeScript check, build, or install was run. The central previous gate failed at `taskEventsReady` before admission; the resume worker owns that fix and this review did not alter or duplicate it.

