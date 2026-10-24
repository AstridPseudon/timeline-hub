<!-- main | 2026-10-24T01:17:15Z | dispatcher heartbeat 7s | live 4 (sol 1, luna 3, other 0) | busy30 20 | status age 0m -->
# runtime board, 2026-10-24T01:16:45Z

| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| C0/R0 | Approved contract and frozen client | Sol / Luna | Approved contract | merged | Prior source and independent reviews | Frozen client 34eac; schema 35c2; producer d5f98. [Evidence](../../design/runtime-prior-proof-evidence-0051.md) | 34eac0041; 62c454ac0 |
| U1/U1b | Upstream and schema 32 | Luna / Sol | Upstream baseline | merged | U1b review 1005; service 32328 | Integrated 456 passed; 12 skipped and 2 configured exclusions are recorded. | 27f0306b9; 4e56253c6 |
| U1c-draft | Refresh draft to latest upstream | Luna | Freeze before integration | gated:freeze | Author 0051; review 0056 PASS | Independent 224 passed; zero new diagnostics; 69 protected paths unchanged. [Review](../../design/runtime-U1c-live-review-0056.md) | 40427e8b5 |
| R0-public-export | Export DocPatchArgs at package root | Luna | P1 GO | merged | Author 0049; review 0052; integrated 0057 | Actual 458595850: 144 passed in 16.25 s; wire probe, generation and Ruff passed. [Proof](../../design/runtime-R0-public-export-integrated-0057.md) | 458595850 / cf74f3e6f |
| F-runtime-full | Full suite after export fix | Service / Luna census | Terminal result retained | doing | Service 29085; census 0107 | FINAL FAIL: 6,479 passed, 36 failed, 26 skipped, 15 xfailed in 416.59 s on 458595850. Census and source causes pending. | 458595850 |
| R2r | History attribution and native authority | Luna / Sol | C0 and U1 | merged | Prior independent reviews | All source-specific results retained in [evidence](../../design/runtime-prior-proof-evidence-0051.md). | 21482a416 and later |
| R2r-atomic-native-birth | Sequential births in atomic scope | Sol / Luna | Integrated proof | merged | Author 1546; review 1554; service 14107 | 338 passed on the recorded integrated head. No guard relaxation. | 2593942df |
| R2r-sequential-input | Authenticate sequential input bindings | Sol / Luna | Integrated proof | merged | Author 1709; review 1728; proof 1737 | 67 passed on 2a9e with Agent bac; faithful 21-command seed and strict refusal checks. | 2a9e347ff |
| R2r-transcript-input | Preserve immutable capture input | Agent Sol / Luna | Agent integrated proof | merged | Agent 1818 | Original three cases passed on Agent 440 and Runtime 2a9e; manifest tampering refused. | Agent 440cc1e702 |
| R2r-history-sequential | Verify durable historical sequence | Sol / Luna | Integrated proof | merged | Review 1604; current pair 1626 | 9 passed, 27 phases and 23 permanent captures. Earlier temporary capture loss remains disclosed. | e6a844696 |
| R2r-nested-range | Authenticate inherited inverse ranges | Sol / Luna | Integrated proof | merged | Review 1606; services 8260 and 20553 | 428 passed on recorded e6 head; current docs-only cleanup preserves those source bytes. | 2ff1121fc |
| R2r-restructure-pins | Keep authenticated physical pins | Sol / Luna | Integrated proof | merged | Review 2031; proof 2036 | 141 passed on actual abd47 with Agent 07e6; exact reviewed tree and 23 strict negatives. | abd47e68de6 |
| G5-historical-fixture | Authentic SDK historical fixture | Luna / independent Luna | Fixture custody | merged | Authors 1632; reviews 1640 and 1645 | Original archive 2915 verified. Agent owns behaviour; lost historical temporary captures disclosed. | evidence only |
| R2r-report-cleanup | Remove unintended root report | Luna / independent Luna | Exact file deletion | merged | Review 1623; proof 1626 | Only report removed; all 475 other blobs identical. Current pair 9 passed. | d9e2a71e8 |
| P5 | Renderer off, authorisation and retries | Luna / independent Luna | R1 and R2 | merged | Review 0405; service 14341 | 14 native and 24 crash cases passed on exact recorded 62c454 and Agent f894. | 62c454ac0 |
| R5 | Reject old save routes | Luna / Sol | A3 and G4 | merged | Review 0557; proof 1011 | Original 20 and legacy 80 passed on recorded c6c69 with Agent ef851. | c6c69f36a |
| P4-admission | Normalise omitted gain | Luna / independent Luna | Proof acceptance | merged | Author 0641; review 0646; service 29163 | 49 passed with old failure and new success demonstrated. Proof owns P4 completion. | a5d425831 |
| DB-runtime-dry | Fresh upstream patch and generation | Luna / independent Luna | Orchestrator dry run | merged | Author 0742; review 0749; builder 7292 | 145 passed; patch and bundle verified. Final build belongs to Farm. | a5d425831 |
| R2r-prepared-media-input | Classify prepared media authority | Luna / independent Luna | Exact four requests | merged | Author 2117; review 2121 | Runtime guard correctly refused missing verified inputs. App owns caller correction. | evidence only |
| OPS-bench-store | Legacy admission and lifecycle | Sol / independent Luna | D34 resume threshold or delivery | gated:D34 | Author 0022; review 0029 | Queue fix passed; lifecycle failed two adversarial probes. Source held and uninstalled; no retirement. | 9e67ac9c58 held |
| OPS-v1-archives | Six unused source archives | Luna / independent Luna | D34 resume threshold or delivery | gated:D34 | Custody 0040; review 0042 | [Independent custody passed](../../design/runtime-v1-archive-custody-review-0042.md). Archives unchanged; no cleanup round. | evidence only |
| OPS-retire-venv | Guarded retirement route | Sol / Luna | Reviewed installation | merged | Installer 1805; remote acknowledgements | Installed a500 and 44c6; old process refusals remain stopped. | installed |
| OPS-retire-runtime | Guarded runtime retirement | Luna / independent Luna | Reviewed installation | merged | Installer 1813; peer 1825 | Installed 954d and 21f6; seven referenced targets refused. Freed 0 GB. | installed |
| OPS-retire-process | Unreadable process diagnosis | Sol / independent Luna | Source assessment | merged | Author 1840; review 1850 | Source assessment complete; superseded by lease store. No host probe or target retry. | source only |
| OPS-D21b-bench-reuse | Reuse authenticated bench keys | Sol / independent Luna | Reviewed store installation | merged | Review 1858; installer 1840 | Private caller and custody checks passed. No real reuse claimed. | installed |
| OPS-D29-child-carrier | Carry exact source paths in queue | Luna / independent Luna | Reviewed installation | merged | Review 2112; installers 2115 and 2119 | 16 caller checks passed; App three-way receipt and actual child creation succeeded. | c887a1; 3b7712 |
| OPS-D29-runtime-toolchain | Carry approved Node path in queue | Sol / independent Luna | Reviewed installation | merged | Installer 2133; App receipt 2143 | 14 caller checks passed; actual App Remotion creation succeeded. | 873ddc; 471fd4 |
| OPS-bench-store-initialize | Initialise absent App store | App Luna | Existing reviewed API | merged | App 2145 | Actual App initialisation and normal child/runtime requests succeeded; no legacy adoption. | existing 6d9368 API |
| OPS-owner/provision | Queue ownership and bounded makers | Luna / independent Luna | Installed source | merged | Reviews 0638 and 1010 | Installed route and bounded child maker retained. | 784bf; 8a646 |
| OPS-D21-bench-kit | Immutable dispatcher benches | Sol / Luna | Actual normal requests | merged | Author 1343; review 1351 | Historical normal builds succeeded with exact tuple and Node 20.19.4. | 9fc7; 39450 |
| OPS-App-template | Authentic approved profile | Proof Luna | Exact pair export | merged | Proof 1835; App 1842 | Proof pair imported unchanged. Runtime duplicate with wrong newline hash remains excluded. | evidence only |
| OPS-main-v1-registration | Finite abandoned registration proposal | Luna / independent Luna | Source only | merged | Return 1850; review 1855 | Proposal passed; no live configuration, removal or target retry. | evidence only |
| V4-deferred | H9 cut and deferred timing | Orchestrator | Deferred scope | gated:H9-cut | No new worker | Original failures stay unchanged and visible. No V4 repair or proof run. | deferred |
| F-authoring-publish-writer | Migrate Agent publication helper | HARD Sol | Agent D32 assignment | doing | rt-F-authoring-publish-media-sol-0114 | Sol0104 found source-bound media admission missing for audio and transforms. Sol0114 owns narrow semantic path; Agent capture hunks reserved. | Agent b61cebe8 |
| OPS-manifest-restore | Restore accidental generated manifest write | Luna | Exact main file identity | merged | Restore 0110; independent 0113 PASS | Exact tracked hash 7c541b restored; main cleanliness and byte equality independently verified. | HEAD 458595850 |
| R0-public-export-manifest | Refresh generated artifact hash | Luna | Full 29085 first failure | review | Author 0111; review 0115 | Author 74 passed; exactly one artifact hash and aggregate version changed. No schema or downstream adoption. | Review pending |
| R5-full-headless | Preserve ten headless scenarios | Luna | Full 29085 source census | doing | rt-R5-headless-fixture-0113 | Source-owned failure family assigned; original assertions and guards stay. No unchanged full rerun. | Base 458595850 |
| R5-full-occupancy | Preserve fifteen occupancy scenarios | Luna | Full 29085 source census | doing | rt-R5-occupancy-fixture-0113 | Source-owned failure family assigned; original assertions and guards stay. No unchanged full rerun. | Base 458595850 |
| R5-full-speed | Preserve six speed refusal scenarios | Luna | D16 earlier refusal | review | Author 0113; review 0116 | Author 14 passed; exact six inputs and SQL/CAS no-write retained. Independent review checks all other test bodies and types. | Review pending |
| R5-full-receipt-key | Preserve receipt and key guards | Luna | Full 29085 source census | doing | rt-R5-receipt-key-fixture-0113 | Source-owned failure family assigned; original assertions and guards stay. No unchanged full rerun. | Base 458595850 |
| R5-full-conformance | Assess two conformance mismatches | Luna | Full 29085 source census | doing | rt-R5-conformance-assess-0113 | Source-owned failure family assigned; original assertions and guards stay. No unchanged full rerun. | Base 458595850 |
| F-full-census-review | Verify all failures and exact recovery | Luna independent | Reports 0107 and 0110 | merged | rt-F-census-recovery-review-0113 PASS | Exact 36 nodes and all counts independently verified; main recovery clean and exact. [Review](../../design/runtime-full-census-recovery-review-0113.md) | Evidence only |
| R2r-external-pack-source | Find authenticated pack source capture | Luna source assessment | Agent peer 0110 | doing | rt-R2r-external-pack-source-0116 | Agent host security fix needs authoritative Runtime source inventory and immutable bytes. No loading, launch or authority waiver. | Read only |

P1 is GO under D25: original 18792 passed both cases in 141 seconds on App f8b15af0, Agent 78738040 and Runtime 2a9e347f. Proof source review 0036 and custody review 0040 passed. Final freeze must rerun all gates on the final heads.

Runtime integration is 458595850c354f4403dabc58a72b98bebbc2c3a3, tree 703b1aac733ad3c977399e67cd4e23d6ae85e7bb. The export fix is merged and integrated qualification 0057 passed. Frozen client 34eac0041, schema 35c2d9c5 and producer d5f98 remain published. No new tuple or adoption is claimed.

Blockers: App / Proof — Readiness fix 42db156 is reviewed and merged. Caller 0053 prepares the one authorised changed P2/P3 run; Proof owns the verdict.
Blockers: Agent — Runtime author 0114 owns assigned F-authoring-publish-writer; Agent owes bounded capture hunk coordination. Agent will review and home-merge; Viewing owns the separate ABA row.
Blockers: Runtime — Full suite 29085 failed 36 cases. Luna0107 owns exact census and source classification before repairs; no unchanged full rerun.
Blockers: Freeze — U1c 40427e8b5 independently passed against upstream 795379a67; integration held until freeze.

D34: Disk work is paused. Main had 9,518,256,128 bytes free at 00:47, above the 8.5 GB resume threshold. Archive review 0042 has finished; no new disk round or cleanup. This pass freed 0 GB. Legacy refusals and prior permission denials remain stopped, with no retry or alternate deletion.

Later: OPS legacy admission, registration custody and pin retirement resume only below 8.5 GB or after delivery. Dormant D31 transcript implementation and tests stay in the delivery; no new migration. Agent failover assignments will use Agent IDs and its owner merge queue.

Blockers: KIT CHANGE: dispatcher-daemon f18bc20b23010dc47a6891d4ef7a357da5991a620b83b5cdc67e0c8741892c15 — installed and retained; no new installation this pass.
Blockers: KIT CHANGE: retire-child-venv 954d5d87fe2e6fcf42b34953ec0edc519a2eb97ade8f66f0f2f96f523516b791 — installed and retained; no new installation this pass.
Blockers: KIT CHANGE: request-retire-venv 21f61833a6718794ab2a06a3a96d34ca58c050ccd0151622e16866ac78758139 — installed and retained; no new installation this pass.
Blockers: KIT CHANGE: bench_store.py 6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8 — installed and retained; no new installation this pass.
Blockers: KIT CHANGE: test-run f599c5ad7bf3cd61aeb01791d903ce6edfa87d5d04a39b3ebb630b3517b17ff4 — installed and retained; no new installation this pass.
Blockers: KIT CHANGE: make-child-venv c887a1bef4831f2ca5a43372ee28430000b2f20b9d290bffb237f27ffc404ff2 — installed and retained; no new installation this pass.
Blockers: KIT CHANGE: request-child-venv 3b771253b465a6ba06b57ab16d6049273114dc75f491ce81d0132fedb3c8aa33 — installed and retained; no new installation this pass.
Blockers: KIT CHANGE: make-runtime 873ddcfa636b3ae9e285613a6fb65c643e21ac749e00197d582e0c820dd70149 — installed and retained; no new installation this pass.
Blockers: KIT CHANGE: request-runtime 471fd470efeae102140b96b4f97db857e0d6d79b0839afa10a1a00e911b33b5f — installed and retained; no new installation this pass.

Next ready: Consume assigned Sol0114, five full-suite repair families and independent census review. U1c is reviewed and held for freeze; Agent owns review and home merge for the assigned writer row. No ready Runtime product row is waiting.

