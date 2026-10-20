# App M2 locked-graph wrapper owner rerun

## Result

FAIL overall: the exact wrapper exited `2` because the real project typecheck exited `2`. The ordinary Node/TypeScript probe passed with exit `0`. This reproduces the original result; it does not indicate a deleted `/tmp` dependency.

Central test ID: `app-ap2-m2-locked-graph-wrapper-owner-rerun-integration-1020214324-22557`  
Central App source tree snapshot: `d6aa0af87d200c19f2b53a412d634f1ff716367e`  
Duration: 63 seconds  
Central status/exit: `fail` / `2`

## Exclusion and command

Before queuing, the established shared exclusion was occupied by the live owner `ap2-m2-ordinary-committed-driver-gate-e2e-m2-ordinary-committed-driver-gate-1020214054-27865`, whose driver read the same locked graph and archive. I waited in short intervals until it reached terminal `fail` and its snapshot cleanup completed. No other test was running when this rerun was queued. No concurrent locked consumer was observed during the wrapper run.

The unique central App integration suite was registered as `ap2-m2-locked-graph-wrapper-owner-rerun-integration` with this exact command:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-ap2-m2-locked-graph-wrapper.sh
```

The wrapper was invoked exactly once, with no arguments, through:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:app ap2-m2-locked-graph-wrapper-owner-rerun-integration --no-cache
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-ap2-m2-locked-graph-wrapper-owner-rerun-integration-1020214324-22557
```

No full suite, browser journey, package installation, network install, or retry was run.

## Tested immutable inputs and guards

- Source archive: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar`
- Source archive SHA-256: `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
- Graph: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph`
- Wrapper SHA-256 at run: `74652a0a221bac0d78bc0a559ae9530490dbf8aee7ab28d4f697fd9d3048fbfd`
- Locked Composition tarball SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- Composition package version: `0.0.13`
- Package-lock Composition integrity: `sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==`
- Graph symlinks: `425`; broken symlinks: `0`
- Extracted Composition regular files: `77`
- Writable graph regular files/directories: `0`
- Private file-package symlink targets (`timeline-schema`, `timeline-ops`, `fake-indexeddb`) matched the graph's private package directory; Composition remained the extracted regular package, as required by the original graph.

The wrapper's own per-run `TMPDIR`, Vite cache, XDG cache, npm cache, and EXIT cleanup were used. After completion, no `/tmp/app-ap2-m2-locked-run.*` directory and no central running marker remained.

## Output

The ordinary probe output was:

```json
{"composition":{"computeMediaTrim":"function","trim":{"trimBefore":15,"trimAfter":45}},"ordinary":{"operations":["clip.set","track.set"],"hold":1.23456789,"label":"ordinary-🎬","move":{"op":"clip.move","on":4}}}
```

Wrapper summary:

```text
source_archive_sha256=895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
tsc_status=2
ordinary_probe_status=0
```

The 10 typecheck diagnostics were the same genuine current App source diagnostics reported by the original reproduction:

- `src/tools/video-editor/commands/elementCapture.ts:236` — `TS2345`
- `src/tools/video-editor/commands/elementGesture.ts:89` — `TS2345`
- `src/tools/video-editor/commands/elementGesture.ts:93` — `TS18048`
- `src/tools/video-editor/commands/elementGesture.ts:112` — `TS2345`
- `src/tools/video-editor/commands/genericPatchCapture.ts:306` — `TS2345`
- `src/tools/video-editor/commands/occurrenceDuplicateCapture.ts:83` — `TS2322`
- `src/tools/video-editor/commands/occurrenceDuplicateCapture.ts:195` — `TS2345`
- `src/tools/video-editor/commands/occurrenceDuplicateCapture.ts:199` — `TS2345`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx:49` — `TS2345`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx:50` — `TS2345`

No exact missing canonical path, owning lease, or deleted dependency was reported. No graph repair or product change was made. Recommended next step: classify/fix the existing 10 App type errors in the owning App work before treating the locked wrapper as green.
