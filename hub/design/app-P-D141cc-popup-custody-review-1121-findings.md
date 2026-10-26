# D141cc independent popup custody review

## Verdict

`PASS_CUSTODY_TEST_FAIL`.

The executed selector has valid native custody and a terminal browser result: one preflight passed; one normal request was created and waited to terminal `fail`, exit 1, in 207 seconds. The result is one readiness pass and one popup ADD failure. This is a test failure, not a custody failure.

## Findings

1. The exact new attempt has one preflight directory (`...26455`) and one normal directory (`...27026`). The normal `request` hash is `dc398cc68a89e1ab322d6bb3a17e5a3362229461db099e9f9f8dcb86d5e80568`; `snap` is `59ed646fd153d3ed6ccf2c468a942ad66575f4f9b0de1fd51a064deb0cc2c71b`. The raw normal `d66/manifest.json` is `5329d7d05a295e9baa5ecde401bfee8c52b083305827c4e0fa57fd1275020350`; `status` is `fail`, `exit` is `1`; `summary` is `5901023ee6edcb8e893d1f1c92baae78948a549f6243440ff229be3ae2860221`; raw `KEEP` is `2948a4e8decacbe88f5695adb46082a97cec947f5150a8dbf802941604a4ae34`.

2. The source identity is exact: App `82e9e13ddf1d7ec6c736521b2eb091dca9877598` / tree `6a6e49eb4461b5ca1a7fa1247653bc794f26d710`; Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92` / tree `d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`; Runtime `95d98f038320d5d46bd679ac000ab3e15825c935` / tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`; Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`. The unchanged builder is SHA-256 `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`, Git blob `59b65214bc74c1ca118b097bc3b13c0ffe480a93`.

3. The author recipe `/dispatches/0` is `d665c4907abd063edc9da0f29c887b56f7b66fb80febbe52f14732ea66e95d0d`. Its normal command hash recomputes as `27fcd174df3f214502bbca1e67b0eb366c361c11e1f5ae5c0c48d7a987582501` and normal row hash as `c89f8ac7430f4e5342fbffb23cd5ce4aa54f2151e38b3e46af7035aea13fc6c3`. The preflight command/row hashes recompute as `12a77c6b068f56a092136bda8953ca916bb456cdf3501f823828fd7a2c23dcc3` / `76706b38147716c75e577d7685ef0b9cf220bf0190f3f52e33bc636fd7216abe`. Normal command bytes have no terminal LF; rows have one LF, as required.

4. The retained native path is authenticated by the actual tool session `86698` and wait session `92916`. The controller receipt records one invocation, no direct `request-test`, no manual request recreation, and same-ID waiting. The raw normal summary/XML/log show the ordinary daemon route, readiness PASS, and popup failure at the unchanged locator before dialog activation. The popup XML has tests=1, failures=1, skipped=0, errors=0; readiness XML has tests=1, failures=0, skipped=0, errors=0.

5. Old IDs `13234` and `20413` were not touched: both remain `cancelled` with the same snap hash `9911cd9aa3298d1090031caf58c297731c279ed036d8dfdfae450a87efe8ef12`. `13234` retains exit 130; `20413` has no body exit or summary, consistent with queued cancellation. Their request hashes are `3196311a5aa5b92e922639016adf80e7b579afe64c31d150f3b1241a62b123b7` and `f5c0e1ab8611ab5897e937d1f4a3448b904aef0aea3ed30458112d7349a833b5`.

6. Native body trace recomputation gives 44 samples from `11:13:20.959Z` through `11:16:46.596Z`, minimum free bytes `5,471,948,800`, maximum sample gap `5.006s`, and no 4-GB stop. The controller sampler was separate from this body trace. The controller worker log supports its sampler being the first tool after worker start (`meta` start `11:11:04Z`, sampler `11:11:14Z`); its requested `start` file is absent, so that file-based cross-check is unavailable. The author’s first-tool label is not supported: the author log first runs `pwd`/PLAN, while the supervised sampler begins at `10:46:03Z`; the author explicitly records the initial detached attempt as unobserved/unreaped. This is disclosed as a historical trace limit, not used to invalidate the controller’s native custody.

7. The bounded D141j records define four structural fields: accepted read-head continuity; occurrence presence in that read; `activeCanonicalOccurrences` before `useShotGroups`; and `useShotGroups` input/result before `ShotGroupOverlay`. `27026` proves none of them. Its manifest records source/test identities and the XML/log record only a pre-popup DOM timeout (`[data-shot-group-key^="f2-occurrence-copy:"]` absent); no canonical read/projection values are retained. Therefore cause remains `UNKNOWN`; no diagnostic, collector, instrumentation, body, rerun, test adaptation, product repair, or new approval is inferred.

8. No outside-row conservation claim is made. The current-selector registry is not an earlier genuine preimage, and the author’s manager INBOX was explicitly mutable during source checks. Only retained genuine request/snap/artifact hashes are used here.

## Trace and review limits

The browser result is immutable and was not repeated. Product tests, Vitest, pytest, typecheck, lint, service commands, and full-suite requests were not run in this review. The reviewer’s own foreground sampler was stopped with Ctrl-C and reaped after three 5-second samples, but it started after read-only inspection; it is not body evidence and does not backfill the author’s historical first-tool gap.
