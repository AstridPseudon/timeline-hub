READY. Updated only the existing P2 row in `tests/suites.conf`, preserving Sol2317’s exact-source OR 40-hex, single-parent SOURCE, same-tree snapshot guard.

Bindings:

- Source: `d96e45cab356e66332050aa902558789b4382dbd`
- Tree: `1764a55c7e3255628fb750b1f9d22c189289765c`
- Source parent: `cdd262c6ba62c9047e72988bb7419a94c5eb4452`
- `support/app.ts`: `d94ba6512d076072d4615d84880325730141f027`
- `mounted-readiness-safety.test.ts`: `7d45051c2dd61a7d636bf16f5ec9c68d893b7c31`

Validation commands and results:

- `python3 "$TMPDIR/qualify.py"` — **44 checks passed**: both real static-prefix positives, 14 negatives, 15 caller failure controls, capture17/argc2/`-c`/payload identity, inner/outer Bash parsing, export/eval, and preservation checks.
- `python3 "$TMPDIR/stage-controls.py"` — **6 passed**: intercepted success ordering exactly once; build/setup/native/list/leaf failures stopped following stages.
- `python3 "$TMPDIR/carrier-values.py"` — **all 13 exported carrier values exact** through clean whole-outer eval.
- `git diff --check` — passed; `git status --short` — clean.
- Four installed Python module origins verified against pinned checkouts.

Synthetic qualification intercepted only HEAD metadata. Source Git, receipts, executables, body hashes, and the 80-file graph remained real. All eight original cases, native/history assertions, later stages, original tail, and dependency bindings are preserved.

P2 row SHA256:
`3763145c84305d061f2f8687c28440a21e32518f49b8e2df9e54172227d3dd4c`

My atomic write preserved **505611 outside-row bytes**, SHA256:
`5b188a8e64760488b28a3b1caf523f228fc789a6aa0f5d01515b83717c146863`

A subsequent concurrent P1-row update changed the current outside-row SHA256 to `4bcd3ab254b4ff10064443e8e2ca08d8cc52bf27b51fc9d38c105b1176c3179c`; I left it untouched. P2 remains exact.

**NOT RUN:** actual mount/build/setup/native/list/browser/backend/HTTP/service/provision/dispatcher or journey stages. No blockers or discretionary semantic changes. Commit message and `DONE` written.

Next: manager submits **one changed P2 `full-e2e-three-products` run against this worker target**, alongside P3.