## FAIL

- Source: base `780da6d605033ca71dbe2ad48c10ec2870ea4865`; candidate `252dd8dc376fc509661ba8c63e91a5d9b0a1d258`; tree `eb91a75f20f0f56f9dbf1f6f834d966ba7643060`.
- Files: `contract/commit-v2.md` only, `+91/-4`.
- Tests: targeted pytest `45 passed`; C0d fixture assertions PASS; JSON parsing PASS (`20` blocks, `7` headings); copies byte-identical.
- Copy SHA-256: `39194655a8a9cc2e2c0ee037a6269cceac07a2b6f527ace1a16bc7ec4cd28673` for both.
- `git diff --check 780da6d60`: PASS.

Blocking finding: the new invalid-case examples use outer `"code": "invalid_document"` (lines 1354, 1358, 1362), contradicting unchanged §4, which requires outer `code` to be `"validation_error"` and semantic codes under `details.code` (lines 1265–1269; existing example line 1397). Change those scenario expectations before merge.

No full/browser/native/lint/type suites run; Markdown-only and provider behavior remain unverified.