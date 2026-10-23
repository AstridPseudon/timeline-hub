**READY.** Updated only `app ap2-P1-chain-h6` in `tests/suites.conf`: six binding replacements. Fresh-read atomic publication preserved all outside-row bytes, including concurrent changes. Product worktree remains clean; P1 commit message and `DONE` exist.

| Binding | Value |
|---|---|
| Source | `18befa48fd2e277d6f4fd32bf3aa10f810a0da1c` |
| Tree | `abe418cde26c0db37b91a6b62f59f4f55b0c05b8` |
| Parents | `4ded7eefdbcbeaf0d6cecc58e55f7083004167d2 02d575e5a698931ee7ca984d23c8f919d58d3771` |
| New row SHA256 | `f2436e08d7bcfa62825930e53041a7e057c23cccbc7c6aeec3a5de5c4bf2afcf` |
| Outside-one SHA256 | `033dd2b6242387a2a69a5a721e85b8b6469ae5fcf0742428fba6a2bf8113b830` |
| P1 body blob | `0160156d6a014284012ca35b6ac2f172c594353a` |
| P1 body SHA256 | `4da0b5f39ef9709e2319a84dc2d62287cfea3893981a46e867c57f2b58924202` |
| Original first case | `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f` |
| New second case | `947cbf32197121acc0d16eb39e230608a4c238e86ac00b9e2717349fc93262ac` |
| Unchanged Gate-5 blob | `37caf28577d42fbe98afd2320dffa3c72e6e74b1` |

Commands and results:

- `bash -n /tmp/w-b7718aa055/outer.sh` — PASS.
- `bash -n /tmp/w-b7718aa055/inner.sh` — PASS.
- `python /tmp/w-b7718aa055/qualify.py` — **15/15 PASS**. Real argc2/`-c`/payload identity; authentic static prefix, receipts, installed origins, graph80/0.0.14 and toolchain; genuine export/eval; exact-source and synthetic single-parent positives.
- Capture17, innerparse and evalparse: **zero subsequent stages**. Eight rejection controls also stopped before stages. Success stubs executed all seven stages once, in order, with five durable stage logs.
- `python /tmp/w-b7718aa055/audit.py` — PASS: complete tail/guards, native21, history/rollback, both selectors and diagnostics38/2/32 preserved.
- `python /tmp/w-b7718aa055/publish.py` and published-byte verification — PASS.
- `git diff --check` — PASS.

Actual source SHA256s:

- Hook: `0f82c62fd09c6bab397e8e83e5faf84d081613143589b07e3e39cf67aa939b79`
- Hook test: `d429545ea3701d241310e89981ab93b0dfbf8107154d67ee75655c9dda0ccef6`
- Handoff: `a8661bd8db4156141f52791a09e80b0bdd7ab0d0776438009c310ec403151970`
- Handoff test: `a8c220e73f11d8afce97d8ee86f57ff0da790a96746f27c910e62f64ed7575d0`

Decision: retained proven caller mechanics and original P1 dependencies; updated bindings only. No blocker.

**NOTRUN:** actual build/setup/backend/native/list/browser/body/service; broad tests/types/lint. Manager next: submit **one original** `ap2-P1-chain-h6` run for this worker.