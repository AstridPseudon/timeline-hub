# D10 installed-host failure classification

## Result

The two reported failures are a real product regression exposed by the D10
deletion. No product source or test was changed in this worker.

## Exact nodes and reproduction

The failures are both in
`src/tools/video-editor/compositions/TimelineRenderer.public-host.qualification.test.tsx`:

- V009 `preserves exact owner resolution and ownerless catalog order`, line
  341: `installedRenderingTextCard` is `undefined`.
- V009 `preserves installed catalog, sequence registry, capability, and
  resolver identity`, line 384: the installed host returns `undefined` for a
  catalog descriptor.

The exact candidate is App commit `1b4ac8b68d64837cce407953b84311e7d82795f2`.
The unchanged parent is `180d2aaea`. Both runs used the private13 dependency
overlay at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/full-main574-public13-8bd8f741/private13/node_modules`
(Composition package `0.0.13`), with Vitest `--no-cache`, one worker, and no
shared dependency writes.

Candidate command:

```sh
node <PRIVATE13>/vitest/vitest.mjs run --no-cache \
  --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/compositions/TimelineRenderer.public-host.qualification.test.tsx
```

Result: **FAIL**, 1 file, 12 tests: 10 passed, 2 failed, exactly the two
nodes above.

Parent command: the same command from an isolated `git archive 180d2aaea`
snapshot, with its `node_modules` linked to the same private13 overlay.

Result: **PASS**, 1 file, 12 tests passed.

## Causal source evidence

D10 deleted exactly these nine package-owned implementations:

- six rendering animations: `fade`, `fade-up`, `scale-in`, `slide-left`,
  `slide-up`, `type-on`;
- rendering `effects/text-card`;
- rendering transitions `cross-fade` and `fade`.

`src/tools/video-editor/runtime/astrid-element-components.tsx:47-53` builds
`ASTRID_ELEMENT_MODULES` from the `@astrid` source glob. Its resolver at
`:81-86` finds the catalog descriptor, searches that glob by
`componentPath`, and returns `undefined` when the source module is absent.
The nine deleted files are therefore no longer resolvable by
`INSTALLED_ASTRID_ELEMENT_HOST`.

This host is production-used by `BrowserVideoEditorProvider.tsx:232`,
`VideoEditorProvider.tsx:1092`, `ExtensionHarnessPage.tsx:434`, and
`VideoEditorProcessesHarnessPage.tsx:616`. It is not a test-only fixture.
The public Home host was migrated to
`PUBLIC_COMPOSITION_ELEMENT_COMPONENTS`; the installed host was not.

## Classification and next step

This is not unchanged preexisting behavior and not a stale shared10/test-env
failure: the unchanged parent passes and the private13 candidate reproduces
the deletion-correlated failure. It is not safe to claim the deletion tree
green. The App manager must either migrate the installed host's package-owned
entries to the existing Composition registry while retaining catalog and local
adapter behavior, or defer the nine-file deletion. This worker intentionally
does not implement that product migration or weaken the assertions.

No full suite, project TypeScript check, install, browser, live socket, or
shared dependency/cache write was run.
