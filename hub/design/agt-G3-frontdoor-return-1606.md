# G3/G5 normal CLI commit frontdoor return

Worker return report: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G3-frontdoor-return-1606/report.md)

Disposition: source/test return complete; P1 remains dependent on the manager's
Runtime-backed rejoin of the two consumer retry assertions.

The local one-page history replay was removed in favor of the authenticated G2
persisted-outbox/commit route. Blank keys refuse before outbox creation. The
document wrapper normalizes only the existing supported diff boundary's empty
parent `config.app`, preserves non-empty unknown data, and restores meaningful
human label/receipt output. Product changes are limited to
`astrid/packs/timeline/cli_native.py`; the only tracked test change is the
owned `tests/packs/timeline/test_cli_document_commit.py`.

Evidence and exact commands/results are in the worker report. No live Runtime
HTTP or full/P1 suite was run.
