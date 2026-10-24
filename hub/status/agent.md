<!-- agent | 2026-10-24T01:13:24Z | dispatcher heartbeat 1s | live 4 (sol 0, luna 4, other 0) | busy30 25 | status age 1m -->
# agent board, 2026-10-24T01:12:00Z
| ID | task | model | needs | status | worker | proof | commit |
|---|---|---|---|---|---|---|---|
| U2 / U2b | Upstream merge and skip policy | Luna / Sol | — | merged | agt-U2b-integrated-1110 | Reviewed merge; integrated 99 passed, no skips or deselections. | abfa78a65 |
| U4a | Frozen Runtime client and schema | Luna | U1, U2 | merged | agt-U4a-envelope-review-0353 | All 15 mapped files and strict reply controls passed. | f894c3c9 |
| R1 | doc.patch, reads and sequential captures | Sol | C0 | merged | agt-R1-private-integrated-1629 | Integrated 16 passed; Runtime owns the original 9-case proof, which passed. | bac094180 |
| R1 transcript | Immutable transcript input | Sol | R1 | merged | agt-R1-transcript-integrated-1818 | Original Runtime transcript cases passed; initial pins remain immutable. | 440cc1e70 |
| R2 | Guarded undo and owner-bound inverses | Sol | R1 | merged | agt-F-R2-joined-integrated-0042 | Current joined head: 56 inverse cases and 14 fixture controls passed. | 0b8cb025c |
| R3 | Dry run and structured errors | Luna | R1 | merged | agt-R3-meta-integrated-0235 | Integrated 150 plus reload and error controls passed. | d6f05e8a9 |
| V2 | Validation without new legacy invalidity | Sol / Luna | D12, D12a | merged | agt-V2-child-integrated-0658 | Scoped validation, strict negatives and six Runtime integration cases passed. | 4edc4b321 |
| G2 / G3 | Public commit, emitter, CLI and sheet | Sol / Luna | R1, R2 | merged | agt-G234-integrated-0549 | Joined 131 plus live Runtime controls passed; P4 covers actual HTTP. | ea302e0f5 |
| G4 | Remaining production writers | Sol / Luna | G2 | merged | agt-G234-integrated-0549 | Reviewed writer migration; later full-suite gaps have separate rows below. | ea302e0f5 |
| G4 video | Prepared video duplication | Sol | G2 | merged | agt-F-five-integrated-2340 | 190 normal cases plus one public Runtime case passed. App consumer also qualified. | 02dea239e |
| G5 | Retire superseded Agent writers | Luna / Sol | H24 criteria | merged | agt-G5-integrated-custody-review-2155 | 350 cases, four SDK cases and c271 passed. Raw packet loss is disclosed in the retained report. | c36ca8c94 |
| P4 owner | Single edit, ten steps, conflict rerun | Proof | G2, G3, R2 | merged | Proof services 28012, 11615, 17739 | All three original HTTP legs passed on integrated heads. No duplicate run here. | e837 / 543d |
| F-full | Post-G5 full suite | Luna | Remaining fixes | blocked:agent | Full 25691; census review 2346 | 17,159 passed; 262 failed; 5 errors; 4 skips. All 267 failing nodes verified. No full retry. | c36ca8c94 |
| F-D32 | Tag and reconcile all 267 failures | Luna | Upstream comparison | doing | agt-F-D32-reconcile-0110 | All 267 are conservatively ours. No pre-existing claim without upstream proof. [Map](../../design/agent-D32-failure-map-0057.json). | evidence only |
| F-G2-pair | Preserve exact public publication pair | Sol | G2 | merged | agt-F-joined-integrated-0037 | Actual ca93: 15 joined checks passed, including five pair controls. | 61727f / 8563 |
| F-R2-owner | Nested order and sibling successors | Sol / Luna | R2 | merged | agt-F-R2-joined-integrated-0042 | Actual 1146: 56 plus 14 passed. Independent 186 strict controls remain valid on exact source. | e53d9f36b |
| F-SDK-closure | Repair the public reader fixture | Luna | G2 pair | merged | agt-F-SDK-fixture-review-0037 | Exact fixture independently passed; joined 14 controls passed on 1146. | 5e6823577 |
| F-capture | Keep both published capture positives | Luna | Runtime fixture | merged | agt-F-capture-integrated-0052 | Actual b61: six original positives and no-CAS controls passed; exact reviewed blobs and static identities retained. | f9c305c8e |
| F-persistence | Restart and disjoint-edit fixture | Luna | Helper digest | blocked:agent | agt-F-persistence-review-0028 | Nine passed, one failed. Legacy child word timing lacks an authenticated binding; original test stays unchanged. | fixture held |
| F-helper-digest | Keep verified helper intent after restart | Sol | G2 | review | agt-F-helper-review-0107 | Author 14 numeric controls passed; three original neighbors remain red and are explicitly under review. | branch only |
| F-renderless | Renderer-free saves with readable show | Luna | SDK reader | doing | agt-F-renderless-current-port-0112 | Independent PASS 75 plus closure and six-field identity. Worker ports only three reviewed files onto current integration. | f502 held |
| F-render-startup | Avoid unused transition-catalog scans | Luna | Source cause 0045 | review | agt-F-transition-final-review-0110 | Return passed 116; cumulative review checks both catalog integrity and error-precedence controls. | branch only |
| F-external-roots | Trust admitted installed pack roots | Sol | Runtime source capture | blocked:runtime | agt-F-external-trust-sol-0104 | Sol kept product unchanged. Runtime-owned source authority is missing; peer 0110 requests precise existing input. | 3d86; 07b held |
| F-env-86 | Original installed-child cohort | Luna | External pack fix | blocked:agent | Services 11789 and 19627 | 69 cases passed, then 16 supported source invocations passed. One external-pack positive remains open. | c36 scope |
| F-render-21 | Original rendering cohort | Luna | Startup fix | blocked:agent | Services 31761 and 10359 | 16 passed, then four passed after PATH repair. One original case still hits the unchanged 45-second timeout. | c36 scope |
| F-env-misc | D13, installers and bootstrap | Luna | Exact installed inputs | merged | agt-F-D13-wheel-input-0039 | Three original environment cases plus D13 passed. Exact c36 wheel matched installed payloads; wheel itself was temporary. | harness only |
| F-CLI | CLI census, generation and motion fixture | Luna | G5 | merged | agt-F-CLI-integrated-0012 | Eight integrated cases and 32 subtests passed; reviewed generation and fixture changes only. | 43bbb / ff5dd |
| F-observer | Nested pytest plugin isolation | Luna | G5 full | merged | agt-F-observer-harness-2355 | 25 original guard cases passed. Test bodies remain unchanged. | c8459e9f8 |
| F-schema | Registered provider-operation census | Luna | Frozen schema | merged | agt-F-joined-integrated-0037 | Six schema cases and three exact union selectors passed; schema and provider guards unchanged. | 7cc6e74c2 |
| F-stale-head | Current public helper fixture | Luna | G2 | merged | agt-F-joined-integrated-0037 | Original stale-head case passed on ca93; two other authoring gaps are assigned below. | ca93d63bd |
| F-P4-symbol | Rename stale fixture symbol | Luna | G5 | merged | agt-F-P4-symbol-integrated-0023 | Both original metadata and CLI behavior cases passed on the integrated head. | 45cecae7b |
| F-authoring-publish-writer | Migrate the remaining publication helper | Sol | failover-ok; assigned Runtime | doing | rt-F-authoring-publish-writer-resume-0104 | Production publish_authoring_candidate calls a retired route after authentic fixture setup. Two Luna attempts are retained. | 20b fixture |
| F-authoring-ABA | Classify same-alias capture ambiguity | Luna | failover-ok; assigned Viewing | doing | vw-F-authoring-ABA-cause-0101 | Current 8ea still refuses the second original case. Cause must be established before any guard or product change. | 20b fixture |
| F-D32-render-wire | Six missing render results | Luna | failover-ok; assigned Viewing | ready | Viewing assignment 0108 | Classify producer and result-path custody first; no overlap with Agent startup or installed-pack fixes. | b61cebe8e |
| A4 IMAGE | Actual App request and Runtime acceptance | Luna / App | App 22ef qualified | doing | agt-A4-image-claim-audit-0112 | Actual output reached Runtime; command identity refused. Canonical data and head stayed unchanged. Exact field audit is active. | 1146 / 22ef |
| D31 | Dormant transcript capture subset | — | Follow-up funding | gated:D31 | No active author | Keep the 397-line test suite and implementation unchanged. Literal production reachability is NO. | unchanged |
| V4 / D14 / D23 | Cut and deferred relational timing | — | Scope decisions | gated:H9 | No repair worker | Keep original tests unchanged, unskipped and visibly failing. No V4 or relational-timing completion claim. | unchanged |
| U2c | Upstream readiness candidate | — | Only if App readiness fix fails | gated:conditional | Not started | Latest orchestrator instruction holds this draft. App owns the cancelled-bootstrap restart deadlock. | no change |

P1: GO. Original service 18792 passed both cases; Proof reviews 0036 and 0040 passed. P4 and P5 are done. G5 already merged under H24. P2 and P3 remain with App and Proof.
Integration: b61cebe8e0d6e062f15da922f3812d7b6718f12e, tree c8b86f253be7ae46a299c1a7e79ac1aaa2b6b8bb. Frozen 34e client, d106 schema and 819acf Composition artifact unchanged.
Blockers: Agent full waits for the remaining owned fixes and D32 classification.
Blockers: D32 upstream comparison waits for the lead to fetch Agent 90d469808. Collection and current-proof tagging continue.
Blockers: Agent external-pack source repair waits for Runtime to name the authenticated capture input; peer 0110 sent.
Blockers: Viewing must return F-D32-render-wire worker ID. Runtime publisher resume 0104 is active and remote.py stays reserved to Agent.
Safety: Earlier Farm, monitor, publication and bench permission refusals remain stopped. No denied action was retried here.
Disk: Last check 11,610 MiB free; below the 15 GB cleanup target and above the 8 GB heavy-run floor. Sweep removed zero directories; compact compressed seven old logs. No eligible clean worktree remained.
Next ready: Land reviewed current ports, consume helper and transition reviews, finish D32 reconciliation and IMAGE command audit. Runtime owns F-authoring-publish-writer; Viewing owns F-authoring-ABA. Do not start U2c.
Evidence: Earlier detailed results remain in [the archived board](archive-v2/STATUS-20261024T0055Z.md) and the existing design handoffs. Worker final messages are copied unchanged into design.
