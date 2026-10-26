# U2 D141m independent source/custody findings

## Result: PASS_SOURCE

The exact finalized merge `5d202569f3af3852476d182ff49683787bb1e881` / tree `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c` has the approved base and frozen upstream as its two parents. Both parent ancestry, whole changed-path set, upstream-only paths, approved-base-only paths, clean merges, actual conflicts, removals, and generated consequences were inspected.

1. **Source conservation passed.** The merge has 54 upstream-changed paths, 28 both-parent paths, 10 actual conflicts, and 44 clean inherited merge paths. All 906 approved-base-only blobs and all 26 upstream-only blobs were conserved exactly. The author source manifest independently matched 54/54 candidate path hashes. No final conflict markers or Python parse failures were found.

2. **Conflict resolutions are source-consistent.** `artifacts.json` is current under the normal generator. Custody keeps accepted native exit proofs and upstream checked process-control/sandbox behavior. Generic-host and platform-helper changes preserve upstream process-control wiring and accepted native paths. Timeline CLI preserves accepted `Path` handling and config behavior. Authoring media implements D141r. Documentation and the three conflicted test files retain frozen upstream source. Runtime writer/reads/undo and security paths remain present.

3. **D141r authority/custody passed at source level.** Accepted importing establishes and validates the existing public `generationId` plus `variantId` pair. Plan input uses that discriminator. Every unmarked alias receives upstream metadata conversion, including media type, filename, resolution from width/height, and duration, with raw source fields removed. No new authority surface or runtime-document authority was added. This is not behavior proof.

4. **Test preservation passed for the merge operation.** The conflicted pidfd, platform-helper, and installer-remotion tests are exact upstream versions. The authoring-media test function set contains the parent predicates. Inspected conflict and related test files contain no author-added skip or xfail. Upstream deliberate semantic predicate replacements remain frozen upstream source; no author resolution weakened, relabeled, retired, or suppressed them.

5. **Installer behavior is present in Agent but App adoption is a handoff item.** Agent source and its assertion include `e1c751def` User-Agent behavior. Current App integration still pins Agent `28e56cac...`, not `e1c751def`, so simultaneous App/lead source handback after normal Agent home must update and verify that adoption. This was not changed in the Agent worker and is not claimed as qualified here.

6. **Runtime custody pin passed.** Exact Runtime producer is `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`; all 15 normal lock entries and 15 canonical packet entries match. No dependency was installed or changed.

7. **Generated and source diagnostics passed against real baselines.** `git diff --check`, normal artifact generation check, and documented vendor-lock check passed. Ruff current 2143 versus baseline 2143; mypy current 1902 versus baseline 1902. No diagnostic was silenced and no baseline changed.

8. **Full proof is required later.** Recomputed union is 16 upstream-added/changed tests, tests for 28 both-parent files, and tests for 10 actual conflicts, deduplicated to 213 test files. Upstream changes shared `tests/conftest.py` and shared `tests/lanes.py`; Main D141l full rerun trigger is true. No bounded delta or full body was run.

9. **P4 proof is required later only for the actual intersection.** Original 0219 and independent 0226 maps have no direct recorded Agent node-name match, but changed `astrid/packs/timeline/cli.py` is directly imported and exercised by the selected P4 CLI test. Actual source intersection is one path and corresponding CLI selector must be rerun later. P4 body was not run; historical receipt `10086` was not retargeted; queued `19479` and D141k remain separate.

10. **No runtime qualification claims.** The v2 caller/accepted/merged/conflict/invalid/preview contract remains source-compatible with required fields and canonical outputs. No authentic runtime/App receipts, REG verdict, product proof, provider proof, or behavior PASS is claimed. Historical author BLOCKED/staging language predates the harness-finalized commit and is preserved as history, not treated as a current merge blocker.

## Validation boundary

Exact commands and outputs are in `validation.md`. This review intentionally did not run pytest, collection, provider/product imports, full or delta suites, P4 body, browser/live-socket execution, or dependency installation.
