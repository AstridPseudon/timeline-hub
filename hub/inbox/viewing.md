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
