## Verdict: FAIL for artifact qualification; semantic proposal PASS

- Strict correction is faithful to C0, not a product defect. App emits six raw keys; Agent derives the seven authoritative fields. Sources: `_recording.py:246–280`, `commands.py:244–304`, `_doc_patch.py:478–528`, Runtime store `timeline_commit_store.py:947–949`, `1424–1448`.
- C0 supports this: §1 lines 102–110, 144–155; C0c lines 287–332; §4 lines 705–715; §7 lines 4611–4626.
- Independent control passed: canonical fixture plus 21 mutations covering every raw/authority family, missing/extra keys, wrong before/value/identity/order.
- Node 20 fault-order control passed: 3/3 subtests.
- Virtual syntax/type/lint passed; scoped ESLint reported 0 diagnostics.
- `git apply --check` passed; final worktree is clean at base `f6a21c285267d6475816adbda74233907ac93911`.
- Published patch SHA matches: `80127a0bc4174b8a5b25d9bc34a52d01c712f76a32a1076245ad9547c084673`.
- Protected spec SHA: `736fd38108283b9c8b5faac47adff4a9c1abd087cb326184a6bfec480e491e05`.
- Actual exact-base + exact-patch virtual SHA: `93c2bf4c72ac3c91442a1a52174e36311113751ab9d8b7e0f52e4a958559a64b`, not published `ef05a482…`. Helper region lines 957–977 hashes to `312ded…`; predicate maps base line 1820 → virtual line 1841.

No source application, browser/original/full/replay run, generated/pin/registry/spec edit, or commit was made. The hash discrepancy must be corrected before qualification. Commit message and `DONE` marker are present.