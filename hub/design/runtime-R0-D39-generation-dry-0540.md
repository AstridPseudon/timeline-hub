# R0/D39 dry-run report

Generated the branch-only Runtime candidate from existing generators. No source schemas, OpenAPI, consumers, pins, or handwritten files were changed.

Changed generated outputs:

- `contract/artifacts.json`
- Python client metadata/generated client
- TypeScript contract metadata
- Runtime contract metadata

Hashes:

- Schema digest: `35c2…398d4c` → `4118…b413d2`
- OpenAPI: unchanged `302523…c075`
- Artifact file: `190f…cbd9` → `2f3d…e369`
- Bundle: unchanged `b6a155…5b39`
- TS generated client: unchanged `7be7…581a`

Checks passed:

- `generators/generate.py`
- `generators/generate.py --check`
- `scripts/artifact_manifest.py`
- `scripts/artifact_manifest.py --check`
- Second generation diff identity
- `git diff --check`
- TypeScript `tsc --noEmit`

Tests:

- Central targeted generated-client/type/manifest suite: **147 passed**
- `tests/test_response_contract.py` is absent; equivalent is `tests/test_recorded_responses.py`.
- Equivalent central run: **148 passed, 15 errors** because `ASTRID_CHECKOUT` was unavailable.
- Direct run reached **143 passed**, with socket-backed failures/errors due sandbox `EPERM`; no product assertion weakening.

D39 behavior confirmed: retired legacy routes return `410 retired_route`; canonical `commitTimeline` returns `409 conflict` with `details.reason: stale_head` for stale heads.

Mounted callers remain pinned:

- Agent: `astrid/sdk/_remote_timeline.py:249` via `WorkspaceClient.commit_timeline`
- App: `src/integrations/runtime/dataProvider.ts:336,1049,1099`

Consumer adoption and merge are intentionally held for freeze and independent Luna review. `DONE` marker and commit message were written; no commit was run.