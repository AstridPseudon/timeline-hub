**READY — all six caller acceptance groups passed under interception.**

Updated only `app ap2-P1-chain-h6` in `suites.conf`. Fixed private graph selection, exported all tail variables, cleared inherited dist overrides, and added a fresh hosted build before setup. Existing guards and complete final tail remain preserved. Worktree clean; commit message and `DONE` created.

Validation commands:

- `bash -n /tmp/w-035f5af960/outer.sh` — PASS.
- `bash -n /tmp/w-035f5af960/inner.sh` — PASS.
- `python /tmp/w-035f5af960/qualify.py` — **13/13 PASS**: actual argc=2, `-c`, byte-exact payload; authentic static guards; clean export/eval; exact-source and synthetic single-parent snapshot positives; parent/tree/multiparent/dirty/body/receipt/path negatives.
- Exit-17, inner-parse and eval-parse controls produced **zero following stage attempts**. Success stubs executed graph → hosted-build → setup → beforeAll → trivialboot → selector → body exactly once.
- `python /tmp/w-035f5af960/audit.py` — PASS: both protected case hashes, Gate-5 blob, native **21** assertions, history, diagnostics **38/2/32**, and full original tail preserved.
- `git diff --check` — PASS.

Bindings and hashes:

| Item | Value |
|---|---|
| App | `5b6aae277417bdbea495f5557eb7c584523ee95e` |
| Tree, equal to reviewed 504dd | `7144f37755d164b57e86b4d8c53b7f09fd123998` |
| Published row SHA256 | `2695e8746edf056c4b180fb7933bf747ad0e409d45437fb6d1e27e0def696fed` |
| Actual payload SHA256 | `429e02824615ad44ae6a2fdd28caad190645d69f30a01601833e452d4ee0d732` |
| Outside-row SHA256, unchanged | `368154c1859ee3270ea8d2eeefbf36e5cd50d58c8c6be4ef658e2ab7fb9fe86b` |

Actual source SHA256 attestations:

- Hook: `0f82c62fd09c6bab397e8e83e5faf84d081613143589b07e3e39cf67aa939b79`
- Hook test: `0e95837e56520b43f22977ea8cb121f56a9b72967074812d406f15ed95de1452`
- Handoff: `e6651748b146e8f31826f0ad6cfdaa89cd4ad7eaeaeb976053e05246cd149a75`
- Handoff test: `a8c220e73f11d8afce97d8ee86f57ff0da790a96746f27c910e62f64ed7575d0`

Decision: shared Composition was **0.0.10**; the approved private graph verified **80/80 files at 0.0.14**. Selection now precedes build/setup. Node20/npm10/6144 and installed Python origins verified.

**NOTRUN:** actual build/setup/backend/native/list/browser/body/service. Unchanged-source tests/types/lint were not repeated. Prior evidence remains untouched; no blocker.

Manager next: submit **one** original run:

```bash
bin/request-test app-P1-actual-caller-sol-2242 ap2-P1-chain-h6 --no-cache
```