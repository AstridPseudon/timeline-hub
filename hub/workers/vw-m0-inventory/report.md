## Completed

- Wrote [design/viewing.md](/home/user/work/wt/vw-m0-inventory/design/viewing.md), covering:
  - Composition evaluator and actual visual/audio paths.
  - Agent/App duplicate math versus necessary adapters.
  - Single pinned Composition tarball consumption and dependency closure.
  - Exact revision identity states for preview/check/visualize/export.
  - M0/M1/M3 boundaries and Linux frame/PCM parity gate.
- Wrote the required commit message at the orchestrator path.

## Verification

- `git diff --check` — passed.
- New-file whitespace check — passed.
- `git status --short` — only `?? design/`.
- No builds, installs, or product tests run, per inventory-only scope.

## Open decisions flagged

- Exact Remotion version closure.
- Handling of generated `@workspace-*` registry dependencies.
- First clean package version (`0.0.8` versus retaining `0.0.7`).
- Exact export revision pin field and unavailable-preview behavior.