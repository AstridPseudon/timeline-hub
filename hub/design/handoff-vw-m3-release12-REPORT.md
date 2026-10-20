# Composition 0.0.12 release report

## Scope

Changed only:

- `package.json`: `0.0.11` -> `0.0.12`
- `package-lock.json`: root and package-root versions -> `0.0.12`
- `README.md`: literal introductory version -> `0.0.12`

The source behavior is unchanged from the approved final-theme-render-consistency base.

## Artifact

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-release12/artifacts/banodoco-timeline-composition-0.0.12.tgz`

```text
sha256  0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3
sha512  490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==
bytes   58444
files   77
```

The safe sorted member manifest, bare SHA-256, and metadata JSON are beside the tarball in the worker artifact directory. Repeated `npm pack` produced byte-identical tarballs.

## Checks

All commands used Node `v20.19.4` and npm `10.8.2`, with the existing read-only graph at `/home/user/work/composition/node_modules`; no install or network was used.

- `/tmp/vw-m3-agent-gate-node20.19.4/bin/npm run build` — PASS.
- `/tmp/vw-m3-agent-gate-node20.19.4/bin/npm run gen-registry:check` — PASS.
- `/tmp/vw-m3-agent-gate-node20.19.4/bin/npm run build:test && ... --test typescript/test-dist/tests/*.test.js` — 9 suites PASS, 0 fail.
- `npm test` — 9 suites PASS, 1 failure: `scripts/gen-registry.test.mjs` cannot spawn its pinned child process under this sandbox (`EPERM`). No test was weakened or skipped.
- `node scripts/check-agent-default-theme.mjs /home/user/work/agent /home/user/work/venv-agent/bin/python` — PASS; actual Agent schema and built package root/theme-api are deeply equal.
- `npm pack` twice with a writable temporary npm cache — PASS; byte identity confirmed.
- Fresh extraction — PASS: 77 safe members, direct package ESM imports, SSR with navy default root canvas, and strict NodeNext typecheck.

No full suite, browser, live socket, renderer, pixel/audio parity, or coordinated Agent/App adoption was run or claimed.
