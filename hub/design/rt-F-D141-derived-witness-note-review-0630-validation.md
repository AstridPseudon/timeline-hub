# D141 derived-witness note review validation

Result: **PASS**.

## Exact commands and results

- `sed -n '1,240p' .../PLAN.md` and `sed -n '241,520p' .../PLAN.md`: PLAN read; it ends at §5 in this checkout, with F governed by the task brief and the board header.
- Read-only inspection of the 06:08 board item, 0600 review/handoff/source-manifest/validation, 0606 publication/controller admission, and author installation evidence: PASS; the required disclosure and limits agree.
- Read-only Python custody/readback check: PASS. Current target hashes are README `13f2b3409d42313dd2ed02d1d479bc5e27cb74f7ec29151e30199428fe0bc776` and gate-results `b29945990c34adc8d8ae0b25f8c6621c4c509f43c84b22adb7dedca141815b47`; both are regular `0644` non-symlinks. Each backup has the specified author preimage hash, and removing exactly the inserted line recovers the full backup byte-for-byte.
- The same controlled fake-input `delivery-build.render_readme` function smoke used by the author and 0254/0258 reviews: **PASS** — placeholders `0`; fence lines `16`, balanced; exact note `2`; placement `2`; A2 `2`; SWAP `2`; Element `2`. No real delivery build or D141m smoke ran.
- Source-record readback/hash check: **PASS**, 5 author-recorded source files matched their recorded bytes and SHA-256 values.
- `cmp -s /home/user/work/runtime/contract/commit-v2.md /home/user/timeline-hub/hub/design/commit-v2.md`: **PASS**, C0 copies byte-identical.
- `git -C /home/user/work/wt/rt-F-D141-derived-witness-note-review-0630 diff --check`: **PASS**.
- `git -C /home/user/work/wt/rt-F-D141-derived-witness-note-review-0630 status --short --branch`: clean worktree; no repository edits.

## Scope and custody

The author receipt records canonical preimage CAS, staged atomic replacement, immediate readback, mode/type checks, directory fsync, no rollback, no unknown-drift overwrite, and 568/568 outside-file hash/mode conservation. The author’s 568-entry preimage inventory was not retained as a standalone file, so this review records that as receipt-backed custody rather than claiming a fresh hash-by-hash replay. No live replay, measurement, witness reconstruction, source repair, production receipt attachment, export/clone/apply/build/ZIP, browser/network action, or product test was performed.

The production caller paths and C0 field surface were read from the unchanged 0600 review and contract context: base revision/publication pair, commands, label, ordinal steps with own patch/reads, `fields|atomic`, declared reads, idempotency, dry-run, source/rationale/group; accepted/merged canonical closure and authenticated receipt fields; conflict reason/head; invalid code/path/hint/suggested command; and unchanged preview. No DTO or contract change was made.
