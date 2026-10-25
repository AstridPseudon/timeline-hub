# D139 final independent review validation

Result: **PASS** on the corrected finite route and accounting.

## Checks

- Original 2154 report, audit JSON, candidates JSON, and validation packet hashes match the recorded 2202/2205 metadata byte-for-byte.
- Independent 2202 review JSON hash matches the 2205 source manifest; its route correction and finite no-candidate conclusion remain intact.
- Every source hash in the 2205 manifest matches current bytes: `request-child-venv`, `make-child-venv`, `bench_store.py`, `request-retire-venv`, `retire-child-venv`, `dispatcher-daemon`, `bench-store/index.json`, Agent `INBOX.md`, and the referenced 2154/2202 evidence.
- Current finite read at `2026-10-25T22:09:31Z`: 5,282,807,808 B free versus the 5,905,580,032 B child reserve; deficit 622,772,224 B. After the explicitly unverified 200,000,000 B source estimate, the residual deficit is 422,772,224 B. Free space remains 282,807,808 B above the 5 GB source floor and 1,282,807,808 B above the 4 GB stop line.
- The active store metadata has exactly two child entries. Superseded d137 is the `3e163...` entry registered at `21:24:50Z`; d40 is the `3b5cb...` entry with its live suite reference. Both remain retained.
- `request-retire-venv` accepts work-root names and queues `RETIREVENV`; `retire-child-venv` resolves `/home/user/work/NAME`. No source-proven direct command targets `/home/user/work/bench-store/entries/child-*`; direct route is `EXACT_MISSING`.
- The source-proven production lifecycle is `request-child-venv` → `CHILDVENV` → `make-child-venv` → `Store.ensure('child', ...)`; `Store.ensure` invokes lease-guarded `Store._evict` before the reserve check. This distinguishes ordinary guarded lifecycle from guessed direct retirement.
- MAIN 22:18 permits the ordinary guarded route only after `2026-10-25T22:24:50Z`. The age boundary alone does not authorize a command, index edit, or filesystem edit.
- Retained guards from independent 2202 are accepted without another broad disk census: dirty G2, KEEP-protected 0816, suite-referenced d40, protected d22/f1012, and preserved prior refusals. Candidate count remains zero.

## Commands and results

- `sha256sum` over all 2205 manifest sources: PASS; all ten hashes matched.
- `sha256sum` over original 2154 and independent 2202 packet files: PASS; recorded hashes matched.
- `jq empty` plus semantic assertions on 2154 audit, 2202 review, 2205 correction, and 2205 source manifest: PASS.
- `df -B1 /home/user/work`: PASS for the finite accounting above.
- bounded `du -sx -B1` on the named store/runtime/protected paths: PASS; values were stable and matched the retained packet metadata.
- source-only `sed` inspection of route, guard, Store, dispatcher, and owner-directive spans: PASS.

No tests, imports, providers, Store operations, eviction, retirement request, recycle, deletion, cleanup, queue mutation, refusal retry, manual index edit, or filesystem edit was performed. No D130 review was performed.
