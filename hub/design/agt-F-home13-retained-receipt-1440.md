## F/R2 report

- Added retained evidence and flat publication:
  - [Evidence map](evidence/agt-F-home13-retained-receipt-1440/source-selector-map.md)
  - [Design publication](docs/design/agt-F-home13-retained-receipt-1440.md)
- Preserved prior log/report/meta/finalize verbatim and extracted the three XML payloads as transcript-retained XML with byte ranges and full SHA256.
- Recoverable prior result: 13 PASS (6 + 1 + 6), production caller reported through `queue_proposal → flush → producer batch → RuntimeCommitService → inverse validation`.
- Original XML custody is unavailable: `/tmp/w-bda7eb9404` was cleaned up. No bytes were reconstructed or relabeled.
- Tests/source execution: none, per task. Read-only verification passed: XML byte-range `cmp`, publication excerpt `cmp`, and `git diff --check`.
- No product, test, generated, lock, or source edits.
- Wrote commit message and empty `DONE` marker.