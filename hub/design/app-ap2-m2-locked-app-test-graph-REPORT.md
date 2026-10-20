# App M2 locked dependency graph

## Result

## Relocation

The immutable App2 environment is now outside the synced design root:

- Old archive: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-ap2-m2-locked-graph-source.tar`
- New archive: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar`
- Old graph: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-ap2-m2-locked-graph/`
- New graph: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph/`
- Archive size: `300830720` bytes
- Archive SHA-256 before/after move: `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`

Consumers repointed: this wrapper's `GRAPH` and `SOURCE_ARCHIVE`, `normal014-source-common.sh`'s `LOCKED_GRAPH` and `LOCKED_GRAPH_ARCHIVE`, and this lease/report. The moved graph's three private package symlinks were repointed inside the moved artifact; shared dependency symlinks still target `/home/user/work/app/node_modules` and were not modified. No old archive, graph directory, or large symlink remains under `design/`. The two unrelated Viewing archives over 50 MB remain in place and were not moved.

Design is safe to sync for this App2 artifact: no App2-owned file over 50 MB remains under `design/`.

Prepared one private, read-only dependency graph for App `48576cfa2783331f2c7c8309ff4069162a3afd11` (tree `126983e329d1ab85a59d7a62ebb96676f8aab622`). The App worktree is clean; no source, config, test, package pin, lockfile, generated file, or Git ref was changed.

Published artifacts:

- Graph: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph/`
- Reproducible wrapper: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-ap2-m2-locked-graph-wrapper.sh`
- Unchanged source archive: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar`
- Ordinary Node/TS probe: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-ap2-m2-locked-graph-probe.ts`
- Lease: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-ap2-m2-locked-graph-LEASE.md`

Downstream must treat the graph as read-only. The wrapper creates and removes a private `/tmp/app-ap2-m2-locked-run.*` source run and places `TMPDIR`, `VITE_CACHE_DIR`, `XDG_CACHE_HOME`, and `npm_config_cache` below that run. No install or network access was used.

## Graph contents and lock identity

- Shared registry dependencies are symlinked read-only from `/home/user/work/app/node_modules`: 421 symlinks.
- The lockfile `file:` packages `@banodoco/timeline-ops`, `@banodoco/timeline-schema`, and `fake-indexeddb` are private copies in `private-file-packages/`, with private symlinks from the graph. This keeps the source-archive run independent of the mutable App worktree vendor paths.
- The only version mismatch in the shared install was Composition. The graph replaces it with the extracted immutable `@banodoco/timeline-composition@0.0.13`; its 77 extracted regular files byte-match the locked tarball.
- The graph has 425 symlinks total: 421 to shared dependencies and 4 to private graph entries; zero broken links. No private graph regular file or directory is writable (`find -P ... -perm /022` was empty).
- All 672 versioned `node_modules/*` lock entries present in the platform install match their locked versions; there are zero mismatches and zero missing required packages. The 109 absent lock entries are platform-optional packages only.
- Exact graph versions: React `18.3.1`, React DOM `18.3.1`, Remotion `4.0.509`, `@remotion/media` `4.0.509`, `@remotion/layout-utils` `4.0.509`, `@remotion/player` `4.0.509`, TypeScript `5.9.3`, Vite `5.4.21`, Vitest `4.1.5`, and tsx `4.21.0`.

Integrity:

- public13 archive SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- public13 archive SHA-512: `eaa80401c7d8a841ae89eb284650458f54271200ca759b22b1076b322bce36d73794072df2d85dcd56cd57a2fb958e5fd83f6fbd32191d30fcbca85f5a02ceb9`
- package-lock integrity: `sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==`; independently recomputed archive integrity matches exactly.
- source archive SHA-256: `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
- wrapper SHA-256: `993e283f05cb734126f7d9cfd3bfa01c51150db1d1309cc54cdf8f818624639e`
- probe SHA-256: `c3b475a7befcfe015961cfe1fde88a5e1a83dbecfc4dd883c78476167b9e2d32`

## Validation

Exact wrapper command:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-ap2-m2-locked-graph-wrapper.sh
```

Result: wrapper exit `2`; ordinary probe exit `0`; real project typecheck exit `2`. The probe output was:

```json
{"composition":{"computeMediaTrim":"function","trim":{"trimBefore":15,"trimAfter":45}},"ordinary":{"operations":["clip.set","track.set"],"hold":1.23456789,"label":"ordinary-🎬","move":{"op":"clip.move","on":4}}}
```

The wrapper's exact typecheck was:

```sh
NODE_OPTIONS=--max-old-space-size=4096 node "$GRAPH/node_modules/typescript/bin/tsc" --noEmit --pretty false -p tsconfig.app.json
```

The 10 remaining diagnostics are genuine current App source errors, not a false-green or package-skew result:

- `src/tools/video-editor/commands/elementCapture.ts:236` — `TS2345` (`string | null` passed where `string` is required).
- `src/tools/video-editor/commands/elementGesture.ts:89` — `TS2345` (`ElementCaptureArgs | undefined`).
- `src/tools/video-editor/commands/elementGesture.ts:93` — `TS18048` (`edit.elementRef` possibly undefined).
- `src/tools/video-editor/commands/elementGesture.ts:112` — `TS2345` (`ElementCaptureArgs | undefined`).
- `src/tools/video-editor/commands/genericPatchCapture.ts:306` — `TS2345` (`JSON` passed where `number` is required).
- `src/tools/video-editor/commands/occurrenceDuplicateCapture.ts:83` — `TS2322` (returned state not assignable to `AgentState`).
- `src/tools/video-editor/commands/occurrenceDuplicateCapture.ts:195` — `TS2345` (`JSON` passed where `string` is required).
- `src/tools/video-editor/commands/occurrenceDuplicateCapture.ts:199` — `TS2345` (`JSON` passed where `string` is required).
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx:49` — `TS2345` (readonly `clear` incompatible with `ElementParamsArgs`).
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx:50` — same readonly `clear` incompatibility.

The ordinary probe imports and executes the actual archived App TypeScript modules for hold, label, and move, and imports public13's `computeMediaTrim`. It does not mock the source modules. No full, browser, localhost, socket, build, Vitest, or external-service suite was run.

## Safety note

During initial graph assembly, an attempted move onto the pre-existing private graph symlink created one temporary nested `package/` directory under the shared Composition package. The shared package root remained `0.0.8`; the exact nested directory was removed immediately, and the final audit confirms it is absent. No existing shared file was overwritten. The final graph was rebuilt only after unlinking the private graph slot, and all subsequent validation used the private `0.0.13` directory.

