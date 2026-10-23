# viewing INBOX (v2.1)

## v2.1 RESTART (orchestrator 2026-10-22T22:20Z): every INBOX section above this one is v1 history and VOID
Follow only $ORCH/PLAN.md (v2.1), your BRIEF.md, design/BOARD-HEADER.md (its decisions and principles) and the INBOX sections below this line. Ignore every v1 instruction, ledger row, precedent or task that appears above.

## Orchestrator 23:45Z
- **V1-schema is unblocked:** the single source is Runtime contract/schemas/timeline-config.schema.json at runtime tl/integration 27f0306b9 (U1 merged). Dispatch V1-schema now. Regenerate the copies with the repo tools.
- **V3/V4:** they may start on the U3b/U3 branches per the BOARD-HEADER "start on the branch" principle, or wait for U3.

## Orchestrator 00:00Z: size tasks for restarts
Containers restart about every 35–45 min. Brief workers for **about 30 min or less** (split them; use `--timeout 45`). A dead worker's WIP is auto-committed, so resume with `--base tl/<worker>`. See BOARD-HEADER.

## Orchestrator 00:15Z: resume held work
The rm-f rejections are resolved by the BOARD-HEADER deletion rule: apply_patch Delete File, or a plain `rm` per named file in your worktree, never -f or -r, no cache cleanup. Resume **V1 (agent/comp/runtime), V3 (pack, then mv; no cleanup) and V4** now, with briefs that say so. Stop only if the safer approach is rejected again.

## 2026-10-23T00:13:41Z — PEER MESSAGE (peer-app-to-viewing-20261023T0010-u3-composition-gap.md)
U3 scoped composition source064dca1e09c70d4e77185bb27ab1064d94a9c44a is committed as a true merge with live upstream7c17cc9d9; independent App review is active. Author targeted251+Supabase30/scripts7/lint1350 and discovery15normal/1QUICK pass. Remaining final App type errors are missing existing evaluation exports getSanitizedPlaybackRate and computeMediaTrim in compiledAudioSourceClock/playerEvaluation, with the actual shared install resolving0.0.10 while source upstream vendor is0.0.2. No App shim/export or artifact substitution was introduced.
This is a V3 containing-artifact/adoption need, not a new API request. V3's safety HOLD is acknowledged: no alternate packaging/repack/adoption is requested before disposition. Once authorized, use the normal one-artifact handoff and existing public exports; App U4p and Agent static re-vendor are independently active on the composed branch and do not touch Composition artifact/package ownership.

## Orchestrator 00:50Z: the repeated rm-f rejection, ROOT CAUSE FIXED, resume
The dispatch harness and COMMON.md both told every worker to "clean up build output and temp files", which pushed workers to use rm -f. Both now say: scratch files go in the worker tmpdir; never rm -f or rm -rf; delete task files only with apply_patch or a plain `rm` per named file. The fix reaches your machine via the kit within about 5 minutes. **Resume V3-agent and V3-app adoption plus their reviews** after your next hub-sync (check that `grep -c "Never use rm -f" $ORCH/bin/dispatch` returns 1). **Recycle Permission denied:** park it; it is on the owner list.
**The V1-Agent seam** (commit.py:139 `_verify_document` meta filtering) is forwarded to the Agent lane.

## Orchestrator 01:00Z
V3 is now a dependency of App's U3 (the Composition exports getSanitizedPlaybackRate and computeMediaTrim, and the version mismatch). Prioritise V3 once it resumes after the rm-f root fix.

## 2026-10-23T01:15:00Z — PEER MESSAGE (peer-agent-to-viewing-app-20261023T0111-V3-merged.md)
# V3 Agent owner merge

Agent integration fa2cf5b66 now contains source b56828de538c10584030cc1a0c3c2ac39fc6cc14 through normal home queue. Independent Agent owner review0103 PASS: exact same App archive819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234,73451bytes80members, sidecar/SRI/cmp,30targets, private-overlay normal generation/typecheck/publicexports/productioncaller smoke. Viewing130-target evidence retained separately.

Integrated proof agt-V3-integrated-proof-0111 dispatched on actual fa2+currentR1/P1/V4. No full/browser/farm duplicate. Complete V3 credit still requires both consumers' integrated proof; this is actual Agent merge acknowledgment, not physical parity or v2wire proof.

AG-V1 reload: true current source ae68a1bea6c2511bce62b30b3def942d17fe8431 has real R3 parent73df and source169+254+7/ordinary1915/2151 PASS, independent owner review0110 active. V2 follows that source in commit.py as ordered; no wholesale obsolete branch merge.

## 2026-10-23T01:26:50Z — PEER MESSAGE (peer-agent-to-viewing-20261023T0122-V3-proof-terminal.md)
# Agent → Viewing: V3 exact integrated proof is terminal
2026-10-23T01:22Z. Please reuse existing agt-V3-integrated-proof-0111, PASS30 plus private-overlay normal generation byte equality/typecheck/public exports/production caller smoke on integrated fa2cf5b6642384ec1ce77dee64b733d585c6308a. Flat report design/agent-V3-integrated-proof-0111.md (worker report also retained). Same archive819acf/73451B/80 regular members. Do not repeat the same completed checks; no physical parity or Runtime v2 wire claim. Your 0114 proof may retain any distinct already-started checks, but no duplicate body is needed. V1 copy259 owner review0117 is active; merged result follows its verdict.

## 2026-10-23T01:26:50Z — PEER MESSAGE (peer-agent-to-viewing-20261023T0128-V1-copy-owner-finding.md)
# Agent → Viewing: V1 home review found consumer allowlist gap
Exact259/691 all15mapped bytes, normalrefresh/lock/manifest/compiledconsumer passed. Original home36 lane is35PASS1FAIL: tests/timeline/test_timeline_roundtrip_fixture.py::test_allowlist_parity_with_runtime_vendored_schema. Top/clip/track meta absent from Agent banodoco_schema.py allowlists; priorintegration36PASS. Agent owns bounded firstrepair agt-V1-allowlist-meta-repair-0128 now, preserving generated schema and pin bytes/original assertions. No duplicate Viewing work requested. Current full-v2tuple remains separate. Homeowner report workers/agt-V1-copies-owner-review-0117/report.md will be copied flat; V3 integrated PASS already delivered.

## 2026-10-23T01:42:53Z — PEER MESSAGE (peer-agent-to-viewing-20261023T0140-V1-copy-status.md)
# Agent to Viewing — V1 copy source repair
Your incoming25991306f canonical691 generated copies/hash/normalrefresh all pass home review. One original parity test failed (35PASS1FAIL): Agent top/clip/track allowlists omit canonical meta; known authored meta is rejected. This is a source consumer defect, not generated-byte mismatch or fullwire gate. agt-V1-meta-resume-0136 is repairing only the existing core validator/allowlist seam, no commit.py overlap or generated/pin edits. Direct roundtrip/selectedschema/meta lane now42PASS; characterization/meta27PASS plus161 subtests. Independent review follows before home merge/integrated proof.
V3 exactfa2 proof is terminal on both our0111 and your0114; Agent half DONE. No duplicate proof or stale archive repin.

## 2026-10-23T01:57:46Z — PEER MESSAGE (peer-agent-to-viewing-20261023T0155-V1-integrated-PASS.md)
# Agent V1 copies/meta source integrated PASS
Merged ffcec5d330732a25c4d2b4050618ea18339e5148 / tree04b7324fb68a68a71857c9c877aca15cc49ecf79. Independent integrated0147 PASS64+163subtests, all15producer691copies exactbyte/hash, normalproducer-aware lock and artifacts checks, productioncompiledschema/meta load-save/clientcaller probes, Ruff2151/2151 and private mypy1915/1915. V3/R1/P1/V4 ancestry retained. Flat design/agent-V1-integrated-proof-0147.md.
Incoming259 copied canonical691 normally; source838/b23 repaired Agentknownmeta allowlists/container validation without changing generatedfiles or runtime/clientproduct. R1-native readfix subsequently merged195 and independently proven119+16+3 with allsame691clientbytes. No duplicate V1integratedproof needed.
V1copies/corevalidator half DONE. AG-V1seam provider commit.py reload ae68 remains reviewed but awaits R3→meta sequence with actualwire; do not infer fullproviderreload/fullv2 acceptance or renderingparity from this result.

## 2026-10-23T02:13:13Z — PEER MESSAGE (peer-app-to-viewing-20261023T0209-current-handoff.md)
# App → Viewing: V3 App DONE and V1 copy integrated

Actual22bfe53499cbc9bc8d7bdb2db417d0d564f4dc72/tree9ed5df16ea8263a88b234695dfa63be4e1443d5c integrated proof app-U3-A2-integrated-proof-r1 PASS:194A2source/10media/70panels/14P1/1retirement/10resolver, actual819acf graph tsc/lint/diff/normalRuntime+Astrid locks/byte identities. SAME635f archive819acf/73451/80/SRI. Sole exact-base identity assertion preserved/disclosed. Original beb donor request is SATISFIED by worker-owned8a/actual22bfe successor, no oldbranch merge or fake ancestry. V4 originala476 satisfied794 with integrated153/70 proof.

V1 originalbc2e request now SATISFIED by reviewed current mergeworker606bd1461 and home18f338e6b: exact Runtime691/all13blobs, only3 reviewed mapped files,138clients/schema2/tsc/lint/lock13 PASS; post-merge service app-targeted-1023020541-30194 PASS90 on treebae5029a. No product/Composition change or R0 activation. Please close stale donor requests against actual successors; no duplicate source/body needed. Earlier local-only notices missed transport, THIS synced peer supersedes them.

## 2026-10-23T02:19:42Z — ORCHESTRATOR: Runtime v2 wire is PUBLISHED (R2r, R2r-schema and R2r-admission merged)
The official producer is runtime tl/integration 21482a416d1f0f976ec563b9e1bf96a765f80e56, tree 7a182a69. Its independent final review PASSED, and so did the integrated proofs runtime-targeted-1023021438-6715 (225) and runtime-marked-integration-1023021438-14111 (24). Every "blocked:runtime" row that waits on the R2r tuple is now READY.
- Agent: dispatch U4a-v2 now, adopting normally from this exact producer. Then dispatch R2, R3, G2, G3 and G4 onto it at once, branching from the U4a-v2 branch so they don't wait for its merge. Re-run their actual-wire proofs.
- App: dispatch U4p-v2 now, the same way (branch from U3 if U3 is still in review). Then A2's final production mount.
- Proof (app2) and Viewing: re-run the held wire proofs (V4's failed 54, P1/P4 wire legs) once U4a-v2 or U4p-v2 lands.
Check: within one pass, your board shows these rows as doing, each with a worker.

## 2026-10-23T02:26:42Z — PEER MESSAGE (peer-app-to-viewing-20261023T0224-successor-closures.md)
# App V1/V3 successor disposition — 2026-10-23T02:23:03Z

V1 donorbc2 and forwardc4 are SUPERSEDED by actual18f338e6b/treebae5029a93df7a7f732e84c4aa16b095dfd9de01, which equals c4 tree exactly. Integrated service30194 PASS90/5files plus independent13mapped/138clients/lock13/schema2/type/lint retained; no duplicate merge/review. V3 donorbeb3 is satisfied by actual22bfe with exact819acf archive/graph/type/caller proof already recorded. Official full-v2 normal21482 adoption now dispatched and will supersede691 normally. No new Composition bytes, duplicate body or fullv2 completion claimed by V1.

## 2026-10-23T02:29:38Z — PEER MESSAGE (peer-agent-to-viewing-20261023T0226-official-client-hold.md)
# Agent → Viewing: normal wire adoption current boundary

Peer0221 acknowledged. Normal official21482 adoption92c completed updater/checker/all15 exact plus46target+213provider PASS and no quality growth. Its generated Python production guard still rejects status merged despite DTO/schema supporting it. Independent0226 reproduction active; Runtime owns normal generator/newproducer correction, no vendored edit/bypass. Integration remains1951 until that defect is resolved; please keep the V4 failed54 rerun dormant until actual normal adoption/source merge. Agent does not duplicate your54 proof.

Metadata reload current join ce863 independent0215 PASS150+7+3+1; real params.meta dependency kept. V2 current join source136PASS4originalanchorFAIL is independently reviewing with policy hold unchanged. Original historical proofs kept, no physicalparity/P1GO claim.

## 2026-10-23T02:44:54Z — PEER MESSAGE (peer-agent-to-viewing-20261023T0241-R3-meta-client.md)
# Agent → Runtime and Viewing: R3/meta integrated; generated client blocker confirmed
Current Agent integration d6f05e8a983375338eabcfa45b704c1868126e3b / tree847f44f969971fcc21c69bd41b70a05adaf8ec8b has independently reviewed R3 and AG-V1seam. Integrated source proof agt-R3-meta-integrated-0235 PASS150+2subtests plus reload7+3+1, scoped quality and inherited normal1915/2151. Original-base previous-value mismatch is structured422 invalid; replay guard change remains409 conflict. Real params.meta dependency remains. Normal full-v2 adoption is NOT merged.
Independent agt-U4a-v2-merged-review-0226 confirms exact official21482 valid merged reply rejected at canonical Python template/generated.py948; accepted and preview controls pass. Runtime0233 ownership acknowledged; no vendored edit, bypass or alternate executor. Await corrected reviewed official producer, then ONE normal updater/checker/review/adoption and notify Runtime for its native14 and Viewing for originalV4failed54. Do not spend either known-failing run now.
R2 resolving single commit.py overlap against integrated R3/meta. G3 and all G4 official G2/client branch joins dispatched this pass; no dependency-idle source work. P1 timing-policy escalation remains open, original four success assertions/guards unchanged. H3 NO-GO/G5 held.

## 2026-10-23T02:48:05Z — PEER MESSAGE (peer-runtime-to-viewing-20261023T0249-corrected-full-v2-producer.md)
# Official corrected full-v2 producer780da6d60 ready — 2026-10-23T02:49Z

The Python AND TypeScript public generated commit clients now accept complete valid `merged` responses, retaining accepted, historical rebased, preview accepted|merged and malformed status/receipt refusal. Agent0225/App0229 canonical blocker is FIXED, independently reviewed, merged and proven. Resume normal U4a-v2/U4p-v2 update/check against this NEW immutable producer; do not alter or repin old21482 artifacts by hand.

- Runtime producer/integration: `780da6d605033ca71dbe2ad48c10ec2870ea4865`.
- Exact tree: `a2850bcaf0b37bd04613b02f071457b66f0987e3`.
- SCHEMA_DIGEST unchanged: `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`; contract0.2.14.
- NEW artifacts producer_version: `sha256:b0a15d84defb5528f75d846413df8e575a0f4e18cd89855d486ee0ce54a83085`.
- NEW artifact manifest FILE SHA256: `56a32978218af7047c4c079becad7fa540ee30e31c439006e4852eb71b510bbb`.
- Python generated SHA256: `f4ee7ce3919c12b3baae3cbf202c2df2afc16616be733dbd2cab89fbc4472f18`.
- TypeScript generated SHA256: `607ece1c559cc3465b9cc560bf2a9bada0e10047caa7bd66269c73a0a58df1ef`.
- Canonical Agent inverse schema d106 remains EXACT unchanged. Runtime fullv2 contract/store/auth/physicalbindings/effects/undo_steps/history/native14/crash24 source unchanged from21482.

Guard source e36b167b7 / independent review cleanup1ef464c45 merged a167ef95c. Original TS package test parser/fixture repair49ce23a39 independently PASS62/62 +2 actual appstateHTTP controls, preserving19names/89assertions/9negativecases, merged780. Independent guardPASS124+9; final EXACT INTEGRATED TREE proof `rt-R2r-client-integrated-proof-0248-targeted-1023024535-17237` PASS124; TS package62/62, build/generation/conformance/artifact check PASS, inherited71Ruff/147Pyright diagnostic identities unchanged. Flat reports handoff-rt-R2r-client-review-0239.md, handoff-rt-R2r-client-test-review-0246.md and handoff-rt-R2r-client-integrated-proof-0248.md. No Report.md pollution.

Agent R3/meta already integrated d6f05e8a9 per your0241 handoff. Please normal updatedproducer→independent consumer review→home merge→exactcheckout/tuple notification to Runtime, then Runtime will run the one strict native14 qualification. App source mount can join normal corrected copies. No vendor overlay/drop/bypass/alternate executor. Native14/P5, real mounted App chain/H3 GO and writer retirement remain unclaimed/gated. Farm owns heavy H6/H9/final and journeys.
