# App post-shot full source readiness

Status: **ready for one central postbatch full; not qualification evidence**.

## Exact source

- App worktree: `/home/user/work/wt/app-m2-post-shot-full-clean-source`
- Branch: `tl/app-m2-post-shot-full-clean-source`
- HEAD: `18becfbede00038830b97e63345445eeef54fa42`
- tree: `44d514b44c864ff9dbb3b99aba2b0a41891af83f`
- Source worktree status: clean.
- `/home/user/work/app` (`tl/integration`) matched the same HEAD and tree and was clean at the final pre-handoff check.
- No product, config, package, lockfile, pin, test, or snapshot files were changed. The only worktree change is the ignored `node_modules` symlink.

## Exact environment lease

- Worker dependency link: `/home/user/work/wt/app-m2-post-shot-full-clean-source/node_modules -> /tmp/app-m2-coherent-deps8/node_modules`.
- Physical dependency root: `/tmp/app-m2-coherent-deps8/node_modules`; the shared `/home/user/work/app/node_modules` root was not used.
- Composition: package `0.0.8`; archive `vendor/artifacts/banodoco-timeline-composition-0.0.8.tgz`; SHA-256 `93bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa`; 77 archive members and 77 installed files, all byte-equal.
- React/ReactDOM: `18.3.1`.
- Remotion, Player, media, and layout-utils: `4.0.509`.
- Historical-compatible Agent source lease, unchanged: `/home/user/work/wt/app-m1-full-agent-source`, HEAD `4a75f68f32049a69fd86135c645fa64c51175c14`, clean.
- Historical-compatible Runtime source lease, unchanged: `/home/user/work/wt/app-m1-full-runtime-source`, HEAD `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136`, clean.
- The Agent/Runtime pair is explicitly historical safety evidence only; it is not a current-pair qualification claim.

## Checks performed

- `git status --short --branch`; `git rev-parse HEAD`; `git rev-parse HEAD^{tree}`: exact source and clean status above.
- Integration HEAD/tree/status comparison: exact match above.
- `readlink`/`realpath node_modules`: exact declared physical root above.
- Archive SHA/member count, installed file count, and streamed `cmp` of every archive member: PASS (`77/77`, no missing or mismatched files).
- Read-only package manifest inspection: PASS for the required React and Remotion versions.
- Static `package.json` script inspection: `npm test` remains `npm run check:no-smoke-tests && npm run check:known-failures && vitest run --config config/testing/vitest.config.ts`; npm CLI arguments can be forwarded to the final Vitest command.

## Not run

No Vitest/npm test, central full request, build, browser/e2e, TypeScript check, install, or socket/live-service command was run by this worker. The manager should request exactly one central full after this handoff using the cache-free forwarded arguments, for example:

```sh
npm test -- --configLoader=runner --no-cache --maxWorkers=2
```

Keep the worker `KEEP` marker and App-manager lease until that full completes. This readiness report does not claim that the full is green.
