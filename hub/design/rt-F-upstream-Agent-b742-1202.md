## Result

Completed the source-only rehearsal. Authentic local Agent ref exists:

- New SHA: `b742893426a46a99a2f30583a54faeebe2bd98b7`
- Tree: `ccb2f286eae9419b95a3f54b11208f68c57b27cf`
- 14 commits after `08e6b905…`
- Source and integration checkouts remained clean and unchanged.

Retained patch used exactly:

- Scope: `92443771676ef2bbb547d0a103d708fa8bec4c63` → `d6294843286c18e57af3c1874cf1996be42212d2`
- Captured tree: `6aeae30f0892a424104a4348bca6fd74ba1315d6`
- Patch: 12,425,282 bytes
- SHA-256: `f5d49d5e63ddc0e7a0fb85966280024af70e498eb4f75bd6595bfb59a52a204a`
- D108 manifest SHA-256: `37e559e6e176f4d9b4c20db27cdf6de8b4f5ef532b5abedf35533caffb2a4504`
- This is the D108 retained patch only; later D122 product changes are not included.

## New commits

`76c7032`, `b3dfcb3`, `0d58a1e`, `1d0b8f0`, `316e366`, `75ede7e`, `c1b8f14`, `6b1e009`, `d14907b`, `1e2eac8`, `98011b1`, `bf603d5`, `f5821b6`, `b742893`.

Touched-path union: 71 paths, including Agent chat, installer, skills, OMP, docs, and tests. Exact overlap with the retained patch is 35 paths:

`astrid/chat/acpProcessHost.test.ts`, `astrid/chat/acpProcessHost.ts`, `astrid/chat/astrid-acp-bridge.ts`, `astrid/chat/astrid-acp-models.test.ts`, `astrid/chat/astrid-agent-models.test.ts`, `astrid/chat/astrid-agent-models.ts`, `astrid/chat/astrid-local-agent-host.ts`, `astrid/chat/astrid-local-agents.test.ts`, `astrid/chat/astrid-local-agents.ts`, `astrid/chat/astrid-project-chat.test.ts`, `astrid/chat/astrid-project-chat.ts`, `astrid/chat/astrid-shared-acp-sessions.test.ts`, `astrid/chat/astrid-shared-acp-sessions.ts`, `astrid/chat/discoveryProbe.ts`, `astrid/chat/localAgents.ts`, `astrid/chat/modelCatalog.ts`, `astrid/chat/service.mjs`, `astrid/chat/service.test.ts`, `astrid/chat/service.ts`, `astrid/core/gateway/dispatch.py`, `astrid/installer/backend.py`, `astrid/installer/core.py`, `astrid/installer/launcher.py`, `astrid/installer/omp/recipe.json`, `astrid/installer/tools.py`, `astrid/packs/rendering/docs/SKILL.md`, `docs/install/OMP-LANDING.md`, `docs/reference/services.md`, `docs/testing/TESTING.md`, `scripts/refresh_omp_recipe.py`, `tests/test_installer_acl.py`, `tests/test_installer_cleanup.py`, `tests/test_installer_lifecycle.py`, `tests/test_installer_omp_source.py`, `tests/test_installer_wheel.py`.

Changed-test overlap: 12 paths, so the D59 zero-overlap criterion is not met.

## Apply result

Materialized exact `b742893426…` via `git archive` in isolated scratch, then ran the retained patch with no Git repository metadata, commit, merge, rebase, reset, or upstream writes.

- `git apply --check`: rejected 6 paths.
- `git apply --reject`: partial application, exit 1.
- Exact rejected paths:

  - `astrid/chat/astrid-local-agents.test.ts`
  - `astrid/chat/astrid-project-chat.ts`
  - `astrid/chat/service.mjs`
  - `astrid/installer/backend.py`
  - `docs/install/OMP-LANDING.md`
  - `tests/test_installer_omp_source.py`

No conflicts were resolved. These paths and the 35 overlap paths are returned to the orchestrator as Agent-owned follow-up.

## Verification

Ran source/ref/hash checks and patch dry-run only. No full suite, tests, browser, render, stage, ZIP, or D54a rerun was performed.

Composition worktree is clean. `DONE` and the required commit message were created.