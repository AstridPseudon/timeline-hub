# F-D86 D106 script4 source handback

Disposition: **SOURCE-QUALIFIED / BEHAVIOR-PENDING**. This publication carries no functional PASS, full-core result, retirement, normal merge, or D106 source-body proof.

## Exact source and receipt

- Source candidate: `060d51642bbffdba51297acfe2341329212e82a2`, tree `8fb07d6b66d9de9882de306a2bdf21ae9c3fda16`.
- Listed source paths are the two permitted test files from the candidate; the timeline-script source remains unchanged at blob `d055b1ebc51e6fdd4c20462b210ad16942546b6e`.
- Ordinary-union blob: `f8bccaaad1e5a1b4c35157cbaade24e2c10e1e02` (`f8bccaaa`). S3-cohort blob: `ab01bba8f17a2946464dc9cabdaab4fee9c03286` (`ab01bba8`). Unchanged script-test blob: `729445cd499dd2f975b7374cce95ed8a44b97e5d`.
- Independent review: `rt-D86-script4-protected-0518-report.md`, 1857 bytes, SHA-256 `0f0657db33ec6022ab39c965138bfcc3b5d92bab8c7172f1e56f969165bab9c9`, **PASS_SOURCE**.
- Normal receipt: `bde578505c035ae949ee8176b466bf8297772904` (`normalbde5`), the normal publication pair for this source.
- D106 source body: `rt-D86-new-source-body-0537-report.md`, 1364 bytes, SHA-256 `c5ca88d0db6866f502b01ddac116912c01acbe704a1f851dc3d928591b664cce`; body outcome was bounded NO-GO and is not reclassified.

## Conservation and boundary

The independent review preserves all four selectors, parameters, opaque values, timing, assertions, guards, inverse/ABA behavior, branches, refusal, retry, and no-write guards. It records that no fabricated `created`, reads, or physical claims were added and that the transcript limitation remains separate. The authored setup lane and exact source/review/normal pair are kept distinct; the production route remains the registered `commitTimeline` provider.

D72 remains **SOURCE-QUALIFIED / BEHAVIOR-PENDING** only. Existing historical failures remain; there is no new functional PASS, `fullcore`, retirement, D103 duplicate, D100 fixture-valid phrase, normal-merge claim, or failed-M1-anchor archive/graph-rename entry. No `/home/user/timeline-hub` write was attempted.
