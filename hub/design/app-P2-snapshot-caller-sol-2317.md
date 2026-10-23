Repaired only the existing P2 row in `tests/suites.conf`, using a fresh read and atomic replacement.

The guard now accepts the exact source or a 40-hex snapshot with exactly one parent equal to that source and the same tree. Source identity, parent, ancestry, body hashes, and clean state remain independently checked.

Pinned identities:

- App: `cdd262c6ba62c9047e72988bb7419a94c5eb4452`
- Parent: `fa702ec1638fe7ee6bbb0e73c567101a1cc00353`
- Tree: `bd2e11b9e193bc458b10c94e16ef6755c6520b5c`
- Agent: `079580ca46af77e0292d49dc34386b25c8391f99`
- Runtime: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`

Validation commands and final results (`TMPDIR=/tmp/w-596fc5e523`):

- `python3 "$TMPDIR/qualify.py"` — **18 checks passed**, including inner/outer `bash -n`, real outer argc=2/`-c`/payload equality, durable export/eval, and real static-prefix qualification.
- `python3 "$TMPDIR/additional-controls.py"` — reproduced the original rejection; additional source negatives, **15 caller failure controls**, and original-tail equality passed.
- `git diff --check` — passed; `git status --short` — clean.
- Separate installed-Python origin probe verified all four modules resolve inside the pinned Agent/Runtime checkouts.

Both positive routes reached the final static stop before mount/build. All **nine negative cases** refused before stages. Synthetic qualification intercepted only HEAD SHA/parents/tree observations; source Git, receipts, executables, 80-file graph, and body hashes were real. The service-name fixture and diagnostic output directory were relocated for local qualification.

New P2 row SHA256, including newline:
`9d479dd83d05cbf7d6bd98363c8c1bcd50153f0022f0abe0da99063583787d62`

Outside-P2 bytes remain identical: **505611 bytes**, SHA256:
`5b188a8e64760488b28a3b1caf523f228fc789a6aa0f5d01515b83717c146863`

Later stages, fail-capture machinery, all-eight selection, native/history assertions, exports, original tail, and P3 are byte-preserved. Expensive stages were not executed; live qualification remains outstanding. No blockers or plan deviations. Commit message and `DONE` written.

Next: manager runs exactly one changed-P2 `full-e2e-three-products` target; retain P3 run **11562** without resubmitting.