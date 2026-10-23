## Report

- Waited on the same full run ID: `agent-full-post-g5-2225-1023222822-25691`.
- Terminal result: **FAIL, exit 1** after 4,162.57s.
- Exact totals: **17,159 passed, 262 failed, 5 errors, 4 skipped, 0 xfail, 0 deselected, 17,430 collected, 86 warnings, 533 subtests passed**.
- D14/D23/H9 remained visible and unskipped. No retry, rerun, body execution, source mutation, or PASS credit.

Failure classification across 267 deduplicated failing nodes:

- 62 direct `runtime_protocol` child-import failures — Runtime child-import/OPS owner; repair admission/import setup.
- 9 isolated child `astrid` import failures — Agent execution/host import-fence owner.
- 28 retired `--native`/legacy CLI-route failures plus 2 retired-route setup errors — Luna2254/G5/R5 migration owner.
- 22 occurrence-media inverse failures — fixture780a/independent2257 owner; authenticated binding normalization unavailable.
- 15 startup custody/probe validation failures — bounded2250 startup/host owner.
- 3 D09 setup errors — installed-profile/source-root custody mismatch; unique D09 harness owner 2255.
- 3 `FakeCheckout.path` fixture failures — Luna2254 CLI owner.
- 6 missing render-result files — rendering owner; cause explicitly unconfirmed.
- Remaining **117 nodes explicitly unconfirmed**, grouped for Agent SDK/timeline (52), execution/rendering (22), CLI/manifest (7), skip/lanes guards (23), and other task-specific rows (13). No upstream/preexisting claim was made.

Custody verification passed:

- Original controller and gw0/gw1/gw2 before/after origins identical.
- Agent and Runtime source manifests identical before/after.
- Runtime execution pin: `8ea0766f5e9fb23cea26c7398770a8aaac06b258`.
- Whole profile unchanged: 23,108 entries, manifest `ed4616c674ffea71e6849f615f385ffa312914c7ca39cf0172e0da1e6df9750e`.
- Profile controls preserved: 21,501 read-only non-registry files, 33 internal links, 80 archive files, and all four registry hashes unchanged.
- Historical creator and complete-byte identity remain `UNKNOWN`.

Complete terminal outcome shards and result log remain retained under 40 MB compressed. Product worktree is clean. Wrote the commit message and `DONE` marker; no product commit was created.