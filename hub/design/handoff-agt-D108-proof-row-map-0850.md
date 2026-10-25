# F-D108 source-qualified row applicability map

Read-only reconciliation of the immutable D108 F01-F47 membership map against the terminal D108b 2016 body. This artifact does not close board rows, repeat body execution, or reproduce classification0846A/B/C.

## Boundary and accounting

- Scope membership: 47/47 complete; held F48-F57, dd2fc D100, and 44cf R2/2154 remain separate.
- Immutable original selector set: 9268; terminal XML nodes: 9269; actual-only terminal nodes excluded from historical scope: 186; original selectors absent from terminal: 185.
- Terminal result: 159 failed, 8763 passed, 86 warnings, 347 errors, 173 subtests passed in 1451.66s (0:24:11).
- Scope applicability: {'ERROR': 26, 'FAIL': 17, 'PASS': 4}. Source hashes match reviewed 070dfc for 47/47 scopes.
- Scope-case memberships total 1234; unique original cases 1180; overlapping case memberships 54. The JSON records every overlap and every node.

## Per-scope result

| Scope | Original cases | Actual outcomes | Source | Applicability | Historical board key | Disposition |
| --- | ---: | --- | --- | --- | --- | --- |
| F01 NativeSheet ordinary-runtime fixture | 12 | error=12 | MATCH | ERROR | F NativeSheet11 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F02 R2 inverse/authentication source identity | 7 | error=7 | MATCH | ERROR | F inverse stage7 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F03 cli-document-commit | 12 | error=11, passed=1 | MATCH | ERROR | F D72 CLI nine | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F04 commit-provider-custody | 162 | failed=3, passed=159 | MATCH | FAIL | F9211 command identity | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F05 document-patch-emitter | 79 | failed=5, passed=74 | MATCH | FAIL | D86-docpatch5 / D92 | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F06 fresh word transcript frontend source identity | 3 | error=3 | MATCH | ERROR | D86 main word46 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F07 media-manifest inverse fixture | 2 | error=2 | MATCH | ERROR | D86 manifest inverse8 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F08 native-batch-ingress | 40 | failed=24, passed=16 | MATCH | FAIL | F native batch24 | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F09 native-word-binding | 95 | error=95 | MATCH | ERROR | D86 main word46 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F10 relational-timing-capture | 8 | error=8 | MATCH | ERROR | D23 helper and restart | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F11 saved capture/projection source fixture | 43 | error=9, passed=34 | MATCH | ERROR | F9211 projection | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F12 selected-schema runtime fixture registration | 9 | passed=9 | MATCH | PASS | F scalar fixtures11 | retain applicability PASS; no blanket closure until the manager confirms this exact historical case set is the row scope |
| F13 test-native-sheet-ordinary-runtime | 12 | error=12 | MATCH | ERROR | F NativeSheet11 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F14 test-next-command-cohort-runtime | 11 | error=9, passed=2 | MATCH | ERROR | F next cohort11 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F15 test-next-ordinary-union-runtime | 2 | failed=2 | MATCH | FAIL | D86 ordinary script4 | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F16 test-occurrence-media-manifest-inverse | 47 | passed=47 | MATCH | PASS | D86 manifest inverse8 | retain applicability PASS; no blanket closure until the manager confirms this exact historical case set is the row scope |
| F17 test-recipe-m2-auto-placement | 40 | error=6, passed=34 | MATCH | ERROR | F M2 placement20 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F18 test-recipe-m2-placement-create-unplace | 37 | error=4, passed=33 | MATCH | ERROR | F M2 placement20 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F19 test-recipe-m2-shared-auto-placement | 80 | error=6, passed=74 | MATCH | ERROR | F M2 placement20 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F20 test-recipe-m2-shot-pool | 29 | error=7, passed=22 | MATCH | ERROR | F M2 pool6 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F21 test-recipe-m2-video-unplace | 35 | passed=35 | MATCH | PASS | F video unplace12 | retain applicability PASS; no blanket closure until the manager confirms this exact historical case set is the row scope |
| F22 test-recipe-occurrence-media | 66 | error=3, passed=63 | MATCH | ERROR | F occurrence48 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F23 test-s3-reviewed-cohort-runtime | 1 | failed=1 | MATCH | FAIL | F S3 setup return | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F24 test-timeline-clip-scalar-provider | 15 | failed=2, passed=13 | MATCH | FAIL | F scalar fixtures11 | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F25 test-timeline-element-publication-runtime | 60 | failed=4, passed=56 | MATCH | FAIL | D86-core-element2 | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F26 test-timeline-script | 6 | failed=1, passed=5 | MATCH | FAIL | F6058 script4 | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F27 wc6-completion-capture | 13 | failed=2, passed=11 | MATCH | FAIL | F WC6 fixture11 | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F28 commitTimeline provider / CLI trim/move | 3 | error=3 | MATCH | ERROR | D86-cli-trim3 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F29 commitTimeline provider / M1 outbox/restart | 10 | error=10 | MATCH | ERROR | D86 main M1 10 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F30 commitTimeline provider / NativeSheet frontends | 3 | error=3 | MATCH | ERROR | F native frontends7 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F31 commitTimeline provider / native checkout | 4 | error=4 | MATCH | ERROR | F D72 SDK restart | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F32 commitTimeline provider / occurrence-media | 48 | error=48 | MATCH | ERROR | F occurrence48 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F33 commitTimeline provider / opaque occurrence | 6 | error=6 | MATCH | ERROR | F6058 opaque6 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F34 commitTimeline provider / owned parent move | 9 | error=6, passed=3 | MATCH | ERROR | D86-owned-move8 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F35 commitTimeline provider / parent media swap | 25 | error=24, passed=1 | MATCH | ERROR | D86 main swap12 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F36 commitTimeline provider / parent track batch | 1 | error=1 | MATCH | ERROR | D86 parent track3 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F37 commitTimeline provider / parent track label | 2 | error=2 | MATCH | ERROR | D86 parent track3 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F38 commitTimeline provider / scalar outbox | 1 | error=1 | MATCH | ERROR | F scalar fixtures11 | retain ERROR open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F39 commitTimeline provider / selected-schema HTTP seed | 33 | error=1, failed=7, passed=25 | MATCH | FAIL | F word oracle two | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F40 commitTimeline provider / shared inverse | 10 | error=5, failed=4, passed=1 | MATCH | FAIL | D86 main inverse10 | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F41 commit-rebase-custody | 49 | error=6, failed=1, passed=42 | MATCH | FAIL | D86-owned-move8 | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F42 historical-redo-authority | 17 | failed=3, passed=14 | MATCH | FAIL | F D72 SDK restart | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F43 publication-route | 14 | error=1, failed=1, passed=12 | MATCH | FAIL | D86-publication1 | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F44 selected-schema-inverse | 33 | error=1, failed=7, passed=25 | MATCH | FAIL | F inverse source six | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F45 semantic-history-authority | 31 | failed=9, passed=22 | MATCH | FAIL | D86-graph-redo2 | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F46 test-commit-runtime-clip-scalar-fields | 3 | failed=3 | MATCH | FAIL | F scalar fixtures11 | retain FAIL open; route per-node failures/errors to classification0846 owners; no blanket closure |
| F47 test-commit-runtime-numeric-move | 6 | passed=6 | MATCH | PASS | D86 main numeric9 | retain applicability PASS; no blanket closure until the manager confirms this exact historical case set is the row scope |

## Evidence and limits

- Original membership: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agt-D108-0656-core-roots.txt` and exact selector list `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D108-core-input-0656/evidence/current-selectors.txt`.
- Terminal outcomes: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agt-F-D108b-core-local-0811-outcomes.json`; source hashes: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D108b-core-local-0811/evidence/test-source-hashes.txt`; manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agt-F-D108b-core-local-0811-manifest.json`.
- `PASS` means only that every immutable original node in that scope is present, passed, and source-matched in the terminal body. It is not a source-only or fixture-only behavior PASS and is not a board closure.
- `FAIL`/`ERROR` retain terminal behavior gaps for shared classification ownership. No cause, regression, or upstream comparison is inferred here.
- Later normald0ec D07/Windows source deltas are reported separately and are not used to retroactively qualify historical cases.
- The TSV is one row per scope-case membership (including explicit NOT_SELECTED rows); JSON carries complete scope rows, tested/reviewed hashes, dependency tuple identity, and overlap accounting.
