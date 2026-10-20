# Verdict: APPROVE

## Scope and source

- Composition source: `44e9de5ef8d0134ba07dbd51aebe34830a53b52e` (`tl/vw-m4-api-smoke-final-gate`).
- Source tree used by the central service: `a2b3734ff2b3d68c3f67851bd1012c23a2209649`.
- Comparison base: `5e06f40146573a529896cc812229eb890c53c81a`.
- The reviewed delta is one file, `scripts/smoke-package.mjs`, with `19` insertions and `3` deletions (`git diff --numstat 5e06f401..HEAD`).
- The brief's literal “21-line delta” wording does not match the checked-out physical diff count (22 changed lines); the actual content does match the requested legacy probes and two runtime registry assertions. This is reported as an accounting discrepancy, not a behavioral defect.
- Immutable package: `banodoco-timeline-composition-0.0.12.tgz`, SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, `58,444` bytes, `77` archive members.

## Delta review

The repair closes the prior gate defect. The strict NodeNext consumer retains the five legacy theme references (`composeAnimations`, `useTheme`, `EffectProps`, `AnimationReferenceList`, and `RuntimeTheme`) and references both `THEME_PACKAGE_CLIP_TYPES` and `THEME_PACKAGE_REGISTRY` as values. The runtime consumer now additionally asserts:

- the exact four clip types: `art-card`, `cta-card`, `resource-card`, and `section-hook`;
- exact registry key coverage;
- a function component and exact `themeId`/`source` metadata for every entry.

The existing ESM, SSR, evaluator, scoped host override, peer identity, generated-entry imports, and strict NodeNext checks remain present. No behavior test was removed, weakened, skipped, or converted to refusal. No package source, generated package bytes, version, dependency, renderer, browser, socket, or threshold code changed.

## Required central evidence

Exactly one central request was made:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m4-api-smoke-final-gate integration-viewing-public12-package-smoke`

Result: **pass, exit 0, 5 seconds**. This is `1/1` named-suite invocation passed. The harness `counts:` field is blank because this is a package smoke script rather than a test-runner suite; the script's ESM/SSR/scoped-registry phase, strict NodeNext `tsc` phase, `npm ls` peer check, and installed-package integrity check all completed successfully. Node was `/tmp/vw-m3-agent-gate-node20.19.4/bin/node` (20.19.4), with the suite-local `.npm-cache-viewing-package`; npm installed `18` packages into the script-created temporary consumer only. The exact supplied 0.0.12 tarball was the package source for imports and `tsc`; no aliases were used.

Central result ID:

`vw-m4-api-smoke-final-gate-integration-viewing-public12-package-smoke-1020085340-3498`

The consumer reported integrity `sha512-490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==`, said installed files were unchanged, and cleaned `/tmp/composition-consumer-jWUYMM`.

## Runtime-export negative controls

Against a private extraction of the immutable tarball, using a private symlink to the read-only Composition peer tree, the same runtime assertion predicate produced:

- positive control: `PASS`;
- missing `THEME_PACKAGE_CLIP_TYPES`: `FAIL as expected`;
- missing `THEME_PACKAGE_REGISTRY`: `FAIL as expected`.

These controls changed only an in-memory namespace copy; the package extraction, source tree, and runtime package were not edited. This proves the added assertions fail closed for either missing runtime export rather than only checking declarations.

## Isolation and shared-write verification

The worktree had no `node_modules`. The central runner therefore created its documented App `node_modules` fallback symlink only in the disposable test snapshot. `scripts/smoke-package.mjs` has only built-in top-level imports; all package imports occur in generated files executed after the private consumer's install. Thus the polluted App fallback was unreferenced by the actual package smoke.

The suite command set `npm_config_cache` under the disposable snapshot, while the script's `npm install` ran in its own `/tmp/composition-consumer-*` directory. A post-run scan found no files under `/home/user/work/app/node_modules` or `/home/user/work/composition/node_modules` newer than the request start (`2026-10-20 08:53:40 UTC`). Shared worktree status showed Composition clean; App's pre-existing untracked vendor links were unchanged. No shared dependency, runtime, venv, or cache write was observed.

## Direct checks

- `node --check scripts/smoke-package.mjs` — passed.
- `git diff --check 5e06f401..HEAD` — passed.
- `tar -tzf ...0.0.12.tgz | wc -l` — `77`; all members matched the package smoke allow-list.
- No full suite, second central suite, network run, browser, socket, render, install in a shared graph, or threshold change was run.

Logs:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-api-smoke-final-gate-central.log`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-api-smoke-final-gate-controls.log`
