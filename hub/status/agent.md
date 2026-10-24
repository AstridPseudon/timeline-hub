<!-- agent | 2026-10-24T01:03:11Z | dispatcher heartbeat 11s | live 3 (sol 1, luna 2, other 0) | busy30 25 | status age 7m -->
# agent board, 2026-10-24T00:55:58Z
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
| F-D32 | Tag all 267 failures | Luna | Upstream comparison | doing | agt-F-D32-tags-0057 | Tagging ours or proven pre-existing. Upstream 90d469808 is absent locally; lead fetch requested. | b61cebe8e |
| F-G2-pair | Preserve exact public publication pair | Sol | G2 | merged | agt-F-joined-integrated-0037 | Actual ca93: 15 joined checks passed, including five pair controls. | 61727f / 8563 |
| F-R2-owner | Nested order and sibling successors | Sol / Luna | R2 | merged | agt-F-R2-joined-integrated-0042 | Actual 1146: 56 plus 14 passed. Independent 186 strict controls remain valid on exact source. | e53d9f36b |
| F-SDK-closure | Repair the public reader fixture | Luna | G2 pair | merged | agt-F-SDK-fixture-review-0037 | Exact fixture independently passed; joined 14 controls passed on 1146. | 5e6823577 |
| F-capture | Keep both published capture positives | Luna | Runtime fixture | merging | agt-F-capture-integrated-0052 | Review: 28 passed plus 13 Runtime controls. Merged b61; integrated original positives running. | f9c305c8e |
| F-persistence | Restart and disjoint-edit fixture | Luna | Helper digest | blocked:agent | agt-F-persistence-review-0028 | Nine passed, one failed. Legacy child word timing lacks an authenticated binding; original test stays unchanged. | fixture held |
| F-helper-digest | Keep verified helper intent after restart | Sol | G2 | doing | agt-F-helper-digest-sol-0048 | Intent and 137 reads survive; normalization changes the before digest. Numeric controls are being added. | branch only |
| F-renderless | Renderer-free saves with readable show | Luna | SDK reader | doing | agt-F-renderless-return-0057 | Review rejected f502: six public timing fields were lost. First return preserves public show and raw saves. | f502 held |
| F-render-startup | Avoid unused transition-catalog scans | Luna | Source cause 0045 | doing | agt-F-transition-catalog-lazy-0052 | A trivial support call scans 56 pack manifests. Fix must preserve all transition validation and timeouts. | branch only |
| F-external-roots | Trust admitted installed pack roots | Luna | Security review | review | agt-F-external-security-review-0050 | First return passed 33 security cases and 8 neighbors. Four original attacks and source-profile regressions under review. | 3d86; 07b held |
| F-env-86 | Original installed-child cohort | Luna | External pack fix | blocked:agent | Services 11789 and 19627 | 69 cases passed, then 16 supported source invocations passed. One external-pack positive remains open. | c36 scope |
| F-render-21 | Original rendering cohort | Luna | Startup fix | blocked:agent | Services 31761 and 10359 | 16 passed, then four passed after PATH repair. One original case still hits the unchanged 45-second timeout. | c36 scope |
| F-env-misc | D13, installers and bootstrap | Luna | Exact installed inputs | merged | agt-F-D13-wheel-input-0039 | Three original environment cases plus D13 passed. Exact c36 wheel matched installed payloads; wheel itself was temporary. | harness only |
| F-CLI | CLI census, generation and motion fixture | Luna | G5 | merged | agt-F-CLI-integrated-0012 | Eight integrated cases and 32 subtests passed; reviewed generation and fixture changes only. | 43bbb / ff5dd |
| F-observer | Nested pytest plugin isolation | Luna | G5 full | merged | agt-F-observer-harness-2355 | 25 original guard cases passed. Test bodies remain unchanged. | c8459e9f8 |
| F-schema | Registered provider-operation census | Luna | Frozen schema | merged | agt-F-joined-integrated-0037 | Six schema cases and three exact union selectors passed; schema and provider guards unchanged. | 7cc6e74c2 |
| F-stale-head | Current public helper fixture | Luna | G2 | merged | agt-F-joined-integrated-0037 | Original stale-head case passed on ca93; two other authoring gaps are assigned below. | ca93d63bd |
| F-P4-symbol | Rename stale fixture symbol | Luna | G5 | merged | agt-F-P4-symbol-integrated-0023 | Both original metadata and CLI behavior cases passed on the integrated head. | 45cecae7b |
| F-authoring-publish-writer | Migrate the remaining publication helper | Sol requested | failover-ok; assigned Runtime | ready | Runtime; peer 0058 requests worker ID | Production publish_authoring_candidate calls a retired route after authentic fixture setup. Two Luna attempts are retained. | 20b fixture |
| F-authoring-ABA | Classify same-alias capture ambiguity | Luna requested | failover-ok; assigned Viewing | ready | Viewing; peer 0058 requests worker ID | Current 8ea still refuses the second original case. Cause must be established before any guard or product change. | 20b fixture |
| A4 IMAGE | Actual App request and Runtime acceptance | Luna / App | App 22ef qualified | doing | agt-A4-image-current-0043 | New input 09f4afbb published. Original raw opaque data and all children retained. Output deadline 01:08:46Z. | 1146 / 22ef |
| D31 | Dormant transcript capture subset | — | Follow-up funding | gated:D31 | No active author | Keep the 397-line test suite and implementation unchanged. Literal production reachability is NO. | unchanged |
| V4 / D14 / D23 | Cut and deferred relational timing | — | Scope decisions | gated:H9 | No repair worker | Keep original tests unchanged, unskipped and visibly failing. No V4 or relational-timing completion claim. | unchanged |
| U2c | Upstream readiness candidate | — | Only if App readiness fix fails | gated:conditional | Not started | Latest orchestrator instruction holds this draft. App owns the cancelled-bootstrap restart deadlock. | no change |

P1: GO. Original service 18792 passed both cases; Proof reviews 0036 and 0040 passed. P4 and P5 are done. G5 already merged under H24. P2 and P3 remain with App and Proof.
Integration: b61cebe8e0d6e062f15da922f3812d7b6718f12e, tree c8b86f253be7ae46a299c1a7e79ac1aaa2b6b8bb. Frozen 34e client, d106 schema and 819acf Composition artifact unchanged.
Blockers: Agent full waits for the remaining owned fixes and D32 classification.
Blockers: D32 upstream comparison waits for the lead to fetch Agent 90d469808. Collection and current-proof tagging continue.
Blockers: IMAGE acceptance waits for App output for input 09f4afbb; the live fixture expires at 01:08:46Z.
Blockers: Runtime and Viewing must return worker IDs for the two uniquely assigned failover rows.
Safety: Earlier Farm, monitor, publication and bench permission refusals remain stopped. No denied action was retried here.
Disk: Last check 11,610 MiB free; below the 15 GB cleanup target and above the 8 GB heavy-run floor. Sweep removed zero directories; compact compressed seven old logs. No eligible clean worktree remained.
Next ready: Process active reviews, D32 tags and App IMAGE output. Runtime owns F-authoring-publish-writer; Viewing owns F-authoring-ABA. Do not start U2c.
Evidence: Earlier detailed results remain in [the archived board](archive-v2/STATUS-20261024T0055Z.md) and the existing design handoffs. Worker final messages are copied unchanged into design.
