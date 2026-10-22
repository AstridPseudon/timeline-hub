# U1 review: FAIL

Reviewed commit: `85b13f3b4bab09688967eca19e08fb40003aeb73` (`feat(runtime): complete U1 upstream schema merge`)

Base reviewed: `tl/integration` at `cc7410a1fa9bd5acc703abfd1b8fde0cf3d00365`. The U1 diff contains six runtime/test files; it does not change contract or generated files.

## Findings

1. **FAIL — the upgrade test does not open an actual upstream app-state v31 realm.** `test_upstream_v31_schema_migration_installs_empty_history_without_invented_baselines` starts a current `RealmStore`, drops selected current columns/tables, sets the metadata version to 31, and then migrates it. That is a synthesized shape, not an upstream v31 fixture or realm produced by upstream code. The committed `tests/fixtures/precut-v31.tar.gz` is a real schema-v31 fixture, but it contains `timeline_commit_history`, so it exercises the legacy timeline-v31 shape rather than upstream app-state-v31. The test therefore does not prove the required upstream-v31 provenance.

2. **FAIL — rerere/merge evidence is absent.** `git config --show-origin --get rerere.enabled` reports `file:/home/user/banodoco/banodoco-workspace-runtime/.git/config true`, but `git rev-parse --git-path rr-cache` points to an rr-cache containing zero files and `git rerere status` is empty. The author log contains no merge, conflict, rerere, recorded-preimage, or resolved-conflict operation. `origin/main` is already an ancestor of the base and tip, so the U1 commit itself is a regular commit rather than evidence of an upstream merge. The reviewed ancestry check passes, but the requested rerere evidence is not present.

3. **FAIL — no independent upstream app-state-v31 source is evidenced.** `origin/main` is `b535646faaad2f8ae7968dfe0f4fa3057f960264` and reports schema 30; it is already an ancestor of the base. The frozen R4 candidate is a separate branch (`31c7ac3a00f7a205f507bf5bd4d4625628d429bd`). U1 adds a metadata-only v30→v31 step and then installs timeline schema v32, but the review found no actual upstream app-state-v31 realm/fixture against which that transition was validated.

4. **FAIL — new static typecheck diagnostics relative to base.** On the changed runtime files, Pyright reports 447 errors on HEAD versus 446 on the extracted `tl/integration` base. Mypy (with the author’s `--ignore-missing-imports --follow-imports=skip` options) reports 15 versus 14. Both checks are baseline-non-clean, but the +1 deltas are new findings and are not waived here.

## Passing evidence

- `git merge-base --is-ancestor origin/main HEAD` passed. `git rev-list --left-right --count HEAD...origin/main` was `249 0`; upstream-main SHA: `b535646faaad2f8ae7968dfe0f4fa3057f960264`.
- The direct legacy/upstream shape probe classified both synthetic shapes as version 31, while distinguishing them by the presence of `timeline_commit_history`; no immediate v31 layout collision was found in that classifier.
- U1 does not modify asset/media identity handling. The asset-identity diff search found no changes to asset identity, media IDs, or content digests.
- `git diff --check tl/integration...HEAD` passed with no output.
- Exact generator/artifact verification passed:

  ```text
  PYTHONPATH=. /home/user/work/venv-runtime/bin/python generators/generate.py --check
  /opt/node22/bin/node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --fixture-root conformance/fixtures --check
  PYTHONPATH=. /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
  => contract/artifacts.json is current
  ```

  No generated contract/client files are present in the U1 diff. The author’s first TypeScript generator invocation omitted its required `--output-root` and failed; the corrected invocation and final checks passed.

- `npm run build --prefix packages/typescript` passed on HEAD and on the extracted base.
- The exact required targeted command completed with `206 passed, 5 failed, 7 deselected`. All five failures are the same localhost socket-permission failures in `tests/test_generated_client.py` (`PermissionError: [Errno 1] Operation not permitted` while starting `RuntimeDaemon`). The identical command on base produced `206 passed, 5 failed, 7 deselected`; no regression was observed.
- The author’s narrower command reported `131 passed, 8 deselected`. The eight deselections are integration-marked live/integration tests, not required U1 migration/commit acceptance tests; live integration/browser suites were not run per the review instructions.
- C0 draft compatibility: `contract/commit-v2.md` is unchanged relative to `tl/integration`, and U1 does not alter its commit request/reply/patch semantics. This is a compatibility result, not C0 approval.

## Lint/typecheck and omissions

The repository has no configured Python lint/typecheck gate in `pyproject.toml` or CI; CI is pytest-based. The author’s focused Ruff command was rerun identically on HEAD and base. Both report the same baseline rule inventory and `Found 174 errors`; no new Ruff rule-category delta was found. The author’s narrowed Ruff command passed, but it is not treated as the full lint gate.

Full suites, browser journeys, live sockets, and farm-owned integration suites were not run. The five targeted socket failures are environment permission failures reproduced on base, not accepted as passing test evidence.

Recommended next steps: provide or generate a genuine upstream app-state-v31 realm/fixture and add an upgrade test that opens it; preserve concrete merge/rerere evidence for the upstream integration; and resolve the new Pyright/Mypy diagnostics before re-review. No repair, merge, push, or C0 approval was performed.
