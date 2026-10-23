## P1 report

Custody/source/no-weakening: **PASS**. P1 result: **NO-GO**.

The prior report’s tree identity had one extra `f4`:

- Incorrect: `abe418cde26c0db37b91a6b62f59f4f4f55b0c05b8`
- Correct 40-hex tree: `abe418cde26c0db37b91a6b62f59f4f55b0c05b8`

Verification command exited 0:

```text
git rev-parse '18befa48fd2e277d6f4fd32bf3aa10f810a0da1c^{tree}'
# abe418cde26c0db37b91a6b62f59f4f55b0c05b8
# length 40
```

Safe inputs were verified from the orchestration copies:

- First: 8019 bytes, SHA-256 `2b6ec924d00f4a48d7aecaf057104bcc51e521a50385512c728ce3e0849e98c5`
- Second: 168409 bytes, SHA-256 `60e3f3145660c15532689baa03826314c329cfdd8587f8522c1522c3a7a47af2`

Both matched exactly.

### Reused actual result

Run `app-P1-D16-caller-sol-2325-ap2-P1-chain-h6-1023232820-13781`:

- **0 passed, 2 failed**
- Exit **1**
- Duration **269s**
- Base: `18befa48fd2e277d6f4fd32bf3aa10f810a0da1c`
- Agent pin: `78738040d72ce74c42ddf7731221aecb06f9246d`
- Runtime pin: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`

First boundary `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f`; second `947cbf32197121acc0d16eb39e230608a4c238e86ac00b9e2717349fc93262ac`; full blob `0160156d6a014284012ca35b6ac2f172c594353a`; full SHA `4da0b5f39ef9709e2319a84dc2d62287cfea3893981a46e867c57f2b58924202`; Gate-5 blob `37caf28577d42fbe98afd2320dffa3c72e6e74b1`.

First case failed at missing Track name after reload, line 1526. Accepted/merged/lost-ack/persisted-retry were reached indirectly; restart, equality retry, drain, and history were unreached. One wire head versus three request projections remains disclosed. Readiness/transient/product cause is **UNKNOWN**.

Second case reached the real 409 and path checks through line 1659, then failed at missing `timeline-command-recovery` at line 1660 versus the production conflict dialog. Mounted conflict/adoption/rejected observations are bounded; explicit rollback, history, canonical rollback, and legacy assertions were unreached.

Historical 19400/24510 outcomes were not imported. No new causal review or approval gate was performed.

### Reused evidence checks

The prior bounded checks remain PASS for both safe artifacts:

- JSON parsing and schema keys
- Qualified source-derived allowlists
- Bounds and credential/private-pattern scans
- Unsafe-URL scan
- Production serializer round-trip
- `git diff --check`
- Reviewed source comparison showed no additional diff; remaining 409/refusal/message/rollback/opaque/sibling/history/receipt/owner/legacy assertions remain preserved

The production path remains `mounted App → persisted outbox → Runtime`, with Runtime as the only writer. Full-v2 request/reply shapes remain unchanged, including `api_version`, scope/base fields, commands, labels, steps/patches/reads, merge, idempotency, dry-run, source/rationale/group ID, and `{data, receipt}` replies covering accepted/merged/authentic historical rebased results, conflicts, and structured invalid responses.

No product, test, source, or configuration changes were made. No tests were rerun because the brief explicitly required bounded report-only work. Harness commit message and `DONE` marker were created.