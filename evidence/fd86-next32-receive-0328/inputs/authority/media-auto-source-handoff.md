# D86 media20 and auto2 source authority

This packet consumes the flat Agent handoff
`handoff-agt-F-next32-0314-{flat-ready-source-selector-manifest.tsv,per-id-eligibility.tsv,set-accounting.tsv,packet-metadata.json}`.

- media20: source `2a04d92fca`, normal receipt `7f4ea9ce7d`, reviewed source
  receipt `rt-D86-parent-media-review-0245-report.md; blob98c25406a`, SHA-256
  `6f68086f887b8c984597b5a7940261ae6fd18564f1da4dccff96351c03afdf76`
- auto2: source `824e03f6a2`, normal receipt `7e23790248`, reviewed source
  receipt `rt-D86-parent-auto-review-0254-report.md; blob30ed39e4`, SHA-256
  `3138f2ac264cf3a5e52bdd44677eb6f8cf9f70d362a0630e5b16490307a6b22c`

The source files are present in the current normal Agent checkout with the
reviewed blobs and hashes. The six guarded-address parent-auto failures remain
held; the two track-label literals are source-only rows in this packet.
