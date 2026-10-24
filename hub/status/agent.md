<!-- agent | 2026-10-24T01:50:04Z | dispatcher heartbeat 11s | live 5 (sol 0, luna 5, other 0) | busy30 24 | status age 0m -->
# agent board, 2026-10-24T01:49:51Z
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
| F-D32 | Exact upstream failure comparison | Luna | Host fetch complete | doing | agt-F-D32-baseline-0148 | All 267 remain ours until identical failure on exact upstream 90d and no project change touching it are proven. | evidence only |
| F-G2-pair | Preserve exact public publication pair | Sol | G2 | merged | agt-F-joined-integrated-0037 | Actual ca93: 15 joined checks passed, including five pair controls. | 61727f / 8563 |
| F-R2-owner | Nested order and sibling successors | Sol / Luna | R2 | merged | agt-F-R2-joined-integrated-0042 | Actual 1146: 56 plus 14 passed. Independent 186 strict controls remain valid on exact source. | e53d9f36b |
| F-SDK-closure | Repair the public reader fixture | Luna | G2 pair | merged | agt-F-SDK-fixture-review-0037 | Exact fixture independently passed; joined 14 controls passed on 1146. | 5e6823577 |
| F-capture | Keep both published capture positives | Luna | Runtime fixture | merged | agt-F-capture-integrated-0052 | Actual b61: six original positives and no-CAS controls passed; exact reviewed blobs and static identities retained. | f9c305c8e |
| F-persistence | Restart and disjoint-edit fixture | Luna | Helper 3b0 reviewed | merged | agt-F-transition-fixture-integrated-0126 | Actual 940b: original restart positive and six pair controls passed. Other sequential and deferred cases remain separate. | b3bb4695f |
| F-helper-digest | Keep verified helper intent after restart | Sol | G2 | merged | agt-F-helper-reader-integrated-0118 | Actual 92b: 14 passed; reviewed blobs and Runtime origins verified. Strict Ruff improvement is tracked separately. | 3b0dc9e80 |
| F-renderless | Renderer-free saves with readable show | Luna | SDK reader | merged | agt-F-helper-reader-integrated-0118 | Actual 92b: 75 plus closure passed, with all six public fields retained. Strict Ruff improvement is tracked separately. | 61070c542 |
| F-render-startup | Avoid unused transition-catalog scans | Luna | Source cause 0045 | merged | agt-F-transition-fixture-integrated-0126 | Actual 940b: 116 controls passed. Exact reviewed source retained both catalog authority guards. | 2b2c1a02f |
| F-external-roots | Authenticate installed external roots | Sol | Runtime private source authority | blocked:runtime | Runtime review 0125; Sol 0134 | Runtime observed bytes but lacks authenticated origin/definition admission. Runtime escalation 0143 owns scope; no trust waiver. | candidates held |
| F-env-86 | Original installed-child cohort | Luna | External pack fix | blocked:agent | Services 11789 and 19627 | 69 cases passed, then 16 supported source invocations passed. One external-pack positive remains open. | c36 scope |
| F-render-21 | Original rendering timeout | Luna | Supported current child invocation | doing | agt-F-timeout-harness-return-0148 | Service 4004 failed missing Runtime import: preflight used child but body used source-only parent. D18 harness return active. | 521c source |
| F-env-misc | D13, installers and bootstrap | Luna | Exact installed inputs | merged | agt-F-D13-wheel-input-0039 | Three original environment cases plus D13 passed. Exact c36 wheel matched installed payloads; wheel itself was temporary. | harness only |
| F-CLI | CLI census, generation and motion fixture | Luna | G5 | merged | agt-F-CLI-integrated-0012 | Eight integrated cases and 32 subtests passed; reviewed generation and fixture changes only. | 43bbb / ff5dd |
| F-observer | Nested pytest plugin isolation | Luna | G5 full | merged | agt-F-observer-harness-2355 | 25 original guard cases passed. Test bodies remain unchanged. | c8459e9f8 |
| F-schema | Registered provider-operation census | Luna | Frozen schema | merged | agt-F-joined-integrated-0037 | Six schema cases and three exact union selectors passed; schema and provider guards unchanged. | 7cc6e74c2 |
| F-stale-head | Current public helper fixture | Luna | G2 | merged | agt-F-joined-integrated-0037 | Original stale-head case passed on ca93; two other authoring gaps are assigned below. | ca93d63bd |
| F-P4-symbol | Rename stale fixture symbol | Luna | G5 | merged | agt-F-P4-symbol-integrated-0023 | Both original metadata and CLI behavior cases passed on the integrated head. | 45cecae7b |
| F-authoring-publish-writer | Migrate publication helper | Sol / Luna | Cumulative source review | review | agt-F-publish-review-0148 | Runtime 5aee source complete; original first test plus six controls passed. Agent reviews all ten cumulative paths. | 5aee branch |
| F-authoring-ABA | Original same-alias rebind and undo | Luna / service | Reviewed source and fixture merged | doing | agt-F-ABA-integrated-0150 | Home bc38 contains exact reviewed source and 52-assertion fixture. One original live run plus integrated 87 controls queued. | 61d53 / c3af |
| F-D32-render-wire | Six original SDK wire results | Luna / service | Existing installed child | merged | Service 27934 | Six original cases passed in 41.48s; body hashes, 19 source identities, import origins and read-only profile retained. | 521c source |
| F-helper-sequential | Capture actual helper replay-map refusal | Luna | Existing diagnostic seam | doing | agt-F-helper-capture-0149 | Actual failure inputs were lost; inventory 0144 excludes numeric and old captures. One bounded observed diagnostic is queued. | no product change |
| F-D32-h3-import | Seven isolated child-import cases | Luna | Existing installed child | merged | agt-F-h3-env-0137 | All seven original fault cases passed in 3.60s; preflight/postflight, body and source identities retained. | 521c source |
| F-ruff-baseline | Record one fewer Ruff finding | Luna | Strict static gate | merged | agt-F-static-integrated-0130 | Actual 521c: make ruff passed 2,147/2,147 and make mypy passed 1,911/1,911. Protected source and pins verified. | 4511f3d81 |
| A4 IMAGE | Actual App request and Runtime acceptance | Luna / App | App created claims | blocked:app | Agent audit 0112; review 0116 PASS | Missing asset and clip claims reproduced the exact Runtime refusal. App source correction requested; old fixture closed. | 1146 / 22ef |
| D31 | Dormant transcript capture subset | — | Follow-up funding | gated:D31 | No active author | Keep the 397-line test suite and implementation unchanged. Literal production reachability is NO. | unchanged |
| V4 / D14 / D23 | Cut and deferred relational timing | — | Scope decisions | gated:H9 | No repair worker | Keep original tests unchanged, unskipped and visibly failing. No V4 or relational-timing completion claim. | unchanged |
| U2c | Exact upstream readiness draft | Luna | Source object fetched | doing | agt-U2c-readiness-port-0148 | Exact f38e source is now available. Four-file port and focused tests only; no cause or merge claim. | branch only |
P1: GO. Original service 18792 passed both cases; Proof reviews 0036 and 0040 passed. P4 and P5 are done. G5 already merged under H24. P2 and P3 remain with App and Proof.
Integration: bc38aa3eb37008e97bcd85833ac9001eb6523d5f, tree 14b3e85f69ec41bbb9979bba572aeef93a70aa8d. Frozen 34e client, d106 schema and 819acf artifact unchanged.
Blockers: Agent full waits for the remaining owned fixes and finite qualifications. D32 baseline comparison is active; no full retry.
Blockers: Runtime external-source producer waits for its orchestrator decision 0143; Agent host consumer remains unchanged.
Blockers: IMAGE acceptance waits for App created-claim correction; Agent source audit and independent review passed. The old fixture is closed.
Blockers: Agent owns remaining helper evidence, ABA fixture/live proof and rendering timeout. All peer worker IDs are received.
Safety: Earlier Farm, monitor, publication and bench permission refusals remain stopped. No denied action was retried here.
Disk: Sweep removed zero eligible old temp directories; compaction found no eligible scratch. About 9 GB remains, above the 8 GB heavy-run floor. Refused or referenced benches stay untouched.
Next ready: Consume ABA fixture and publication reviews, then current-only port and original integrated proof. U2c and D32 comparison run independently.
Evidence: Earlier detailed results remain in [the archived board](archive-v2/STATUS-20261024T0055Z.md) and the existing design handoffs. Worker final messages are copied unchanged into design.
D32: Upstream 90d is fetched. Baseline comparison 0148 is active; all 267 remain ours pending exact proof. No pre-existing credit yet.
