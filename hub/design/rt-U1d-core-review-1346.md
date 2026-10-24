# U1d Core Review Report

## Verdict

- **Independent core/security source review: PASS**
- Exact candidate: `f69ad58139dc0026ceca814539386b0829493f96`
- Genuine two-parent merge:
  - `becfe6db88b2cc034dba3fafa6c050117cdf2b06`
  - `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`
- No upstream-revert commit detected.
- Protected commit/auth/schema32/D40/R5 paths remain unchanged.

Provider registration, authenticated actor propagation, canonical request handling, one-writer service path, legacy-route refusal, Windows ownership, admission-fence FD custody, replacement, realm creation, and upgrade paths are intact.

## Contract and provenance

- 55 manifest-listed OpenAPI/schema/runtime-schema/generated-client blobs: **0 mismatches** against the local parent.
- `python scripts/artifact_manifest.py --check`: **PASS**
- `python generators/generate.py --check`: **PASS**
- Candidate change is manifest-only visual fixture union:
  `conformance/fixtures/visual-seam-cases-v1.json`
- No D39 regeneration or consumer adoption claim is made.
- Runtime has no normal `vendor_lock` checker. `tests/astrid-agent.pin` and schema provenance `source_commit` facts remain unchanged; consumer lock/source rebind remains separately unverified.

## Tests

Requested targeted command:

```text
... pytest -q -o addopts= -p no:cacheprovider
tests/test_platform_windows.py
tests/test_realm_creation_publication.py
tests/test_realm_replacement_publication.py
tests/test_timeline_commit_authentication.py
tests/test_timeline_commit_sequential_verifier.py
tests/test_timeline_legacy_authority.py
```

Result: **exit 0**, `282 passed, 9 skipped` in 158.32s. XML: 291 tests, 0 failures, 0 errors, 9 declared Linux skips. Native Windows lock/process coverage remains unexecuted on Linux.

Additional upgrade tests: **exit 0**, `50 passed, 1 declared Darwin skip`.

Exact two strict xfails:

- `test_generated_python_client_timeline_publication_is_retired_pending_commit_replacement`
- `test_generated_direct_timeline_shot_reference_writers_remain_retired`

Both remain existing registered strict xfails with HTTP 410 refusal behavior. XML reports 0 failures/errors; raw pytest exit was **1** because the repository policy reports these xfails as undeclared skips. No test, marker, or exclusion edits were made.

Author broader evidence was authenticated separately: final XML reports `440 passed`, `11 skipped`, `0 failures/errors`, 185.889s. The earlier main log still contains 8 FAIL entries; it was not relabeled. Visual/protected FPS coverage was not rerun because it belongs to the separate join worker.

## Static checks

- Ruff normalized comparison against actual `becfe` plus incoming inherited diagnostics: **0 genuinely new diagnostics**.
- Pyright: raw exit 1 with **142 errors both before and after**, zero normalized new diagnostics.

## Handoff

Safe handback is limited to this Runtime source/core review. Consumer adoption, vendor-lock compatibility, source-commit rebinding, native Windows execution, and protected FPS test joining require their designated owners/services.

Worktree is clean. Commit message written; `DONE` marker created.