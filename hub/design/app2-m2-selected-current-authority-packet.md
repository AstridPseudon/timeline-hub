# ap2-m2-selected-current-authority-packet

## Base and deliverables

Current App root: `d12d0909746c552dee6dac7b5d8459e8e1f27679` (contains `ea38656fe`; `ea38656fe` is an ancestor).

The accepted resolver is restored from approved helper `c90277edd`, without importing the old 89bb root/cohort/pins. Assigned worktree source files:

- `src/tools/video-editor/commands/selectedParamAuthority.ts`
- `src/tools/video-editor/commands/selectedParamAuthority.test.ts`

Resolver SHA-256 values:

- `selectedParamAuthority.ts`: `10e129c45a1e63b3eb27999f6edab8a1141672cf58bf2b9fc41c983920ef31f7`
- `selectedParamAuthority.test.ts`: `685b97242cf8d63f6c8d225fe55b2d30e82f886c33d78fde2b1a92054900a15a`

## Current-root shared seam proposal

[app2-m2-selected-current-shared-port.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app2-m2-selected-current-shared-port.patch)

SHA-256: `ab5cf099ed6785158b6692f2fa83d890a9f4531170ab15e8560476ec80e6a958`

This is a real four-source-file unified patch, apply-checked against the current root. It changes only:

1. `src/integrations/runtime/client.ts`: authenticated retained document/object reads keep the original pin, client, session slot, and handshake identity across async reads.
2. `src/integrations/runtime/dataProvider.ts`: project-scoped read capability and complete history pagination through the first captured head, rejecting cursor cycles and head drift.
3. `src/tools/video-editor/data/DataProvider.ts`: typed accessor over the existing `DocumentPin` / verified document types; no DTO, store, API, or persisted pin.
4. `src/tools/video-editor/hooks/useTimelineCommandSession.ts`: captures accepted basis/history on initial/fresh/poll reads and exposes a synchronous resolver using that existing basis and frozen head.

Apply order: add the two resolver files, then apply this patch. `git apply --check --whitespace=error-all` passes.

The resolver contract is fail-closed: it consumes only authenticated accepted history through the captured head, checks predecessor/order/completeness and structural reorientation, and returns the exact direct-triple original P. It does not consult a latest catalog/manifest, relabel to HA, or manufacture bindings. Unknown authority raises/refuses while the caller retains the draft. The retained read preserves P through async capture/retry/restart by refusing changed session identity rather than silently refreshing.

## Row-local PropertiesPanel wiring

[app2-m2-selected-current-row-local.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app2-m2-selected-current-row-local.patch)

SHA-256: `284011b069591be180f7f27b251ed419c1920877e509b811d974a046e6daa4ce`

This separate two-source-file patch changes only:

- `src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx`
- `src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx`

It adds optional retained-pin, existing TimelineOps, and existing command-session state props and forwards them into the mounted ClipPanel. It does not create a native PARAM capture path, submit route, or direct POST. Therefore this is prop wiring only and makes no production-native-row claim; PARAM command capture/finish/submit remains a separate gate.

## Evidence

All commands were run without changing shared worktrees, shared node_modules, or shared virtualenvs.

- Resolver focused test: Vitest selected resolver file, no cache, one worker: **12 passed**.
- Resolver lint: ESLint on the two resolver files with `--max-warnings 0`: **passed**.
- Private combined selected candidate (approved helper plus retained-input/property controls): six Vitest files, exact requested combined lane: **181 passed**.
- Private session regression: `commitSession.selectedParams.test.ts`: **19 passed**.
- Native qualified source archive `47c1ee60`, read-only `venv-app2-native`, selected authority suite: **27 passed**.
- Native refusal probe using qualified source `47c1ee60` and direct `runtime_protocol.timeline_commit.CommitRejected`: reversed authenticated history page and parent `config.clips` reorientation: **2 passed**.
- TS/native accepted fixture parity: **2 cases, exactParity=true**.
- Current-root private overlays with each proposal applied: `npm run typecheck:strict-islands -- --pretty false`: **passed**.
- Current-root patch validation:
  - `git apply --check --whitespace=error-all app2-m2-selected-current-shared-port.patch`: **passed**.
  - `git apply --check --whitespace=error-all app2-m2-selected-current-row-local.patch`: **passed**.
  - `git diff --check` on private applied overlays: **passed**.

No full, browser, localhost, live-socket, or e2e suite was run. No shared repository edit, dependency change, generated file, Git ref mutation, ledger change, DTO, API, or new persisted authority field was made.

