# P4 fixed-source staged port handoff

PASS for the bounded test-only port.

- Base exact commit/tree: `1f93b8b3057a7c2a611f7bdc186c943418b62bc` /
  `681c9e5151fbc7d97d87ed2d4c97f0039f654d5f`.
- Donor exact commit/tree: `98190338b33124668048d0acafb705290ebcada5` /
  `9c7ea32f8500bbac8d3f411936da661fd06802be`.
- Donor and worktree blob for
  `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py`:
  `c18fe40b6ad304a1d594ce736efde41cf1d2a1a1`.
- Outside-file equality passed: only that test path differs from the base;
  all other tracked blobs are unchanged. No donor product ancestry/report was
  imported.

The reviewed test retains the original a0→5, b0/café/order/raw/full closure,
request, cache boundary, accepted/merged canonical document, digest, receipt,
effects/bindings, steps/dependencies, show/history/head, and stored-readback
assertions. The production ordinary show path is verified as
`cli_show.print_cut_table` → fixed `build_cut_table`; the production sheet
caller is verified as `cli_native.commit_edit` → public `TimelineSession` →
`NativeSheet.apply` → `commit_many` → Runtime commit.

Evidence:

- explicit integration collection: exactly 1 node, exit 0;
- scoped Ruff: PASS;
- direct private-cache mypy on the touched file: PASS;
- `git diff --check`: PASS;
- offline cache/export/binding/steps/dependencies witness: PASS;
- baseline comparator: current 1,899 vs baseline 1,915, an existing 16-error
  improvement and not growth (comparator exits 1 to request baseline lock-in).

The literal acceptance collection command uses the repo's default
`not integration` addopts and therefore exits 5 with one deselected node; the
explicit marker override supplies the exact-one collection evidence without
executing the test. No HTTP/socket/body/full/browser/build/service request was
run, so live accepted show/history/receipt readback remains unverified by this
stage. The manager-owned existing one-node `p4-v2-http-nodes` request is the
next validation step. This branch is not an integration merge candidate.
