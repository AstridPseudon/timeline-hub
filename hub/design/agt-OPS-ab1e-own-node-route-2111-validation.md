# D134 own-node source/dry validation

## Passed

- bash -n evidence/ab1e-own-nodes.sh — PASS.
- Embedded Python origin probe via the wrapper — PASS; Agent imports resolved from the actual snapshot PWD and runtime_protocol from /home/user/work/wt/rt-pin-ab1e4f61.
- Positive dry control — PASS: inert stub returned 17 and was called exactly once.
- Poison dry control — PASS: zero Runtime SHA failed preflight with exit 1 and zero stub calls.
- Runtime identity — PASS: clean ab1e4f6141987706132916e2da16477f5a019464, tree 7d8e77b2f5a4af79305c9212ce5174d3ea9fd657.
- python3 -m json.tool runtime.lock.json — PASS.
- git diff --check — PASS.

## Static row checks

proposed-row.txt is the normalized authoring-current8ea-nodes row with only the suite name and Runtime bind changed. It retains env -i, normal Agent PWD binding through $PWD, -q -o addopts= -m integration -p no:cacheprovider --timeout=45, and no -k, deselection, skip, xfail, or PYTHONNOUSERSITE workaround.

No pytest collection or behavioral body was run. No Runtime/provider/network/browser/profile/Store/child/core/full/test-service body was started.

## Precise blocker

The unchanged historical authoring selector is not admissible for this row: tests/timeline/test_authoring_media.py:916 hardcodes missing /home/user/work/wt/rt-pin-8ea0766f. This is reported as exactmissinginput; no acquisition, overlay, test edit, guard change, or fallback was attempted. Selectors that honor ASTRID_RUNTIME_CHECKOUT may be reviewed by the manager against this row after normal review.
