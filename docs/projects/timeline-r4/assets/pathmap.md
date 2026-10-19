# Historical path map

Published control files replace source-machine absolute paths with symbolic roots. Resolve these only when the receiver explicitly configures the corresponding workspace.

| Token | Meaning |
|---|---|
| `${TIMELINE_R4_CONTROL_ROOT}` | Original run-owned control root; relocated here to `docs/projects/timeline-r4/`. |
| `${ASTRID_WORKSPACE}` | Astrid host/source checkout selected by the receiver. |
| `${RUNTIME_WORKSPACE}` | Runtime checkout selected by the receiver. |
| `${APP_WORKSPACE}` | App checkout selected by the receiver. |
| `${COMPOSITION_WORKSPACE}` | Composition checkout selected by the receiver. |
| `${CODEX_BIN}` | Receiver-selected Codex executable, passed explicitly to the dispatcher. |
| `${NODE_BIN}` | Receiver-selected Node executable for the pinned Codex CLI package. |
| `${RECEIVING_HOST_LOCK_PATH}` | Receiver-configured workload lease path; configure per host. |
| `${HISTORICAL_USER_HOME}` | A source-machine user path omitted from the portable instructions. |
| `${OLD_LOCAL_ENDPOINT}` / `${OLD_PORT}` / `${OLD_PROCESS_HANDLE}` | Nontransferable source-machine runtime evidence. |
| `${OLD_LOCAL_TEMP_ROOT}` | Redacted old-machine Runtime/app-support/temp path; never use as a receiver path. |
| `${ORIGINAL_CONTROL_RUN_ROOT}` / `${HISTORICAL_CONTROL_RUN_ROOT}` | Historical run roots retained only as source provenance. |
| `${ASTRID_EXECUTION_CLONE}` / `${ASTRID_EXECUTION_WORKTREE}` | Receiver-selected execution clone/worktree; control authority stays in tracked `docs/projects/timeline-r4/`. |

Historical links inside copied source documents may still name local run receipts, review folders, or workspaces that are intentionally not transferred. `handover-manifest.json` is the complete original-to-package file map. A missing old-machine link is not evidence that its claim passed; use the attached selected receipts and exact source refs, and keep every untransferred prerequisite marked missing or UNKNOWN.
