# F-D86 durable Agent ledger source handoff

Status: **SOURCEQUALIFIED / BEHAVIORPENDING**. This publication restores
eight exact source receipt rows to the durable Agent-area ledger. It does not
edit the generated combined ledger, make a functional PASS claim, retire
D107, or claim D100 fixture validity.

## CAS and generator boundary

- Source: `deletion-ledger.agent.md` only.
- Existing prefix before append: 88,200 bytes,
  SHA-256 `f482770924e1eb107a7e96f9becbdb11497baa405ee55fdfea5abb66620873e1`.
- Final source after append: 95,086 bytes,
  SHA-256 `1ca791747bdf88d999f42ebc25426890147844dd9f812cc2602f377f55e10727`.
- Readback verified that the first 88,200 bytes equal the recorded prefix.
- `ledger-index` was inspected read-only: it selects non-separator lines
  beginning with `|`, excludes the header row, and sorts by the second pipe
  field. The eight rows therefore participate in normal MAIN regeneration;
  `deletion-ledger.md` itself was not edited.

## Recovered source receipts

All eight unique markers are present exactly once in the durable source:

| marker | source identity and scope | review | receipt / membership | status |
| --- | --- | --- | --- | --- |
| `F-D86-word-mirror-0622` | Candidate `5e9acf59d266d45d74e5ae844bf62fddb64267f3`, tree `d68a366224e28ee58045805008be092a5a560944`; `tests/editing_conformance/native_word_anchor_fixture.py`; fixture SHA-256 `f70d2e9cc65ea6207d4ca4b5c0b85527c70495e29696e4acbee120718ddeddac` | `agt-F-word-mirror-review-0620`, `PASS_SOURCE`, `F-D86-source-review.md`, SHA-256 `1e5ca1cdbca5f9d99792cef252bcaa66a044cf61896472f5640c9e9da51e9a44` | normal reference `normal5554fe792b`, no new behavior receipt; original ID5 receipt `rt-R2-ID5-route-return-0558-r2-id5-route-return-0558-1025055758-1023` (one selector, setup ERROR); actual1565 `rt-D86-new-source-body-0537-fd86-new-source-body-0537-1025054041-1565` (60 selectors: word46 + sheet11 + D92 three; 0 PASS / 3 FAIL / 57 ERROR) | SOURCEQUALIFIED/BEHAVIORPENDING |
| `D106-opaque6` | Source `3c742a9cfa1509234ca70048612e7302e4e2298c`; blob `339bf63752f509c1c0cb6b1fce30cda385dd2065`; SHA-256 `3a5558085a78f3d8558219921da81029b3cb648e876b84eaefaf713d1e6e722a`; `test_commit_runtime_opaque_items.py` | `rt-D86-opaque6-protected-0517-report.md`, `PASS_SOURCE` | normal `fd3cbf2b1a9adf772296f54c23649673c054e9b6`; six cases / 29 assertions | SOURCEQUALIFIED/BEHAVIORPENDING |
| `D106-script4` | Source `060d51642bbffdba51297acfe2341329212e82a2`; blobs `f8bccaaad1e5a1b4c35157cbaade24e2c10e1e02` / `ab01bba8f17a2946464dc9cabdaab4fee9c03286`; four-selector ordinary/S3 source lane | `rt-D86-script4-protected-0518-report.md`, `PASS_SOURCE` | normal `bde578505c035ae949ee8176b466bf8297772904`; handback retains the original script blob and transcript limitation | SOURCEQUALIFIED/BEHAVIORPENDING |
| `D106-D98a` | Source `a09ebcbd80fa7d9a83288f1ceded790321ce1877`; blob `c4f54e34536dabbf196fd9a17c337b78394506e3`; SHA-256 `cf73444ebe59c7a5e62f29cff072d3c3dea87ead85043d92ef632d433cb110a1`; `test_commit_runtime_occurrence_media.py` | `handoff-agt-D98a-review-0550-report.md`, `PASS_SOURCE` | normal `a90bc7f9e1653e94384c094aaa87adf32239f5bc`; 48 selectors / 4 tests | SOURCEQUALIFIED/BEHAVIORPENDING |
| `D106-parentmedia` | Source `f261c9e26935dd0ef64f80e7512a4f27066b1c27`; blob `09feb356415afca6ccf4861036abca4a21ed80d7`; SHA-256 `6f6084fff5f645f19adf767c757ba1ee5b7c6cd4b4a097cfe90f85e103512123`; `test_commit_runtime_parent_media.py` | `reviewbatch0553 B`, `PASS` | normal `1a97728baafcef69ed3d081b03902ad3d5ac2032`; retained membership 20, historical actual 2 PASS / 18 setup ERROR | SOURCEQUALIFIED/BEHAVIORPENDING |
| `D106-sheetCLI` | Source `b68d6b96af9a830da3c4402c3d5fa6bb8a1b3206`; blob `13937e75836f5468467579898ddb4cde2afdb92e`; SHA-256 `3d391f6362053159a15f7d8ee15c7088c4b4e44a85431c0b094195a07027b8b7`; `test_native_sheet_current_runtime.py` | `reviewbatch0553 C`, `PASS` | normal `b9484befcadb9427ebac65de938dfa10217edb4f`; retained membership 3, historical actual 2 PASS / 1 FAIL | SOURCEQUALIFIED/BEHAVIORPENDING |
| `F-D86-D103-0648` | Integrated Agent `dac3df399f204126e802f7888bd006c81dffa7af`; `test_cli_trim_runtime.py`; integrated blob `9c425dea9b9aa01f6811bed76512c09b1154ad97`; SHA-256 `f95422aa07b917aafda4d533ddc2ff887336e2ff9e4c9d5a56f073056e41229d`; exact original source blob `793ab7efc71ead62c0b8e2ab827f31856a066aec`, SHA-256 `bd29a7a63e2213c326321ddf38bae2fe3df751c60ffa8acef1eaed46e8743868` | independent `A-D103.md`, `PASS_SOURCE` | canonical predecessor: 169,696 bytes, SHA-256 `db446389e7746d91cf7c972a0e94af16d76b9c98af89d118c7af904b30809ed5`; 38 assertions; historical 17724 D103 three ERROR | SOURCEQUALIFIED/BEHAVIORPENDING |
| `F-D86-S3-0648` | Integrated Agent `dac3df399f204126e802f7888bd006c81dffa7af`; `test_s3_reviewed_cohort_runtime.py`; integrated blob `e754ff53b3df0f0541e5484cc38167caf3dd1844`; SHA-256 `b611bf469880172b725c8cf6052a1288a3d101bf65218b86f00028df4d07cafe`; exact original source blob `ab01bba8f17a2946464dc9cabdaab4fee9c03286`, SHA-256 `e76420c9adc51701bd2c0aff27530a84a206fe583a0215e575f4bf6c2eaf92f5` | protected `rt-D86-script13-protected-0629-report.md`, `PASS` | canonical predecessor: 169,696 bytes, SHA-256 `db446389e7746d91cf7c972a0e94af16d76b9c98af89d118c7af904b30809ed5`; 12 assertions; historical 17724 ordinary-script four FAILs retained | SOURCEQUALIFIED/BEHAVIORPENDING |

The D106 reconciliation retained the original recovered block facts:
3,747 bytes, replaying the claimed 172,066-byte ledger hash
`eb745e019c99fe2daa655d81838995e34dc28b7e1dddbaee71646bc9609af306`, and
the prior canonical 173,720-byte hash
`ebe797dc4f450f1895e111aadf34e6368ae450f907f0ac907fccec629f6d90ee`.
Those are historical generated-ledger checkpoints, not claims about this
new durable source file.

## Boundaries

All original inputs, topology, opaque values, assertions, refusal, retry,
inverse, ABA, and no-write guards remain represented by the retained source
handbacks. The production route remains the registered `commitTimeline`
provider. No tests, imports, helpers, services, generated files, pins,
schemas, product code, or foreign-area inputs were changed.
