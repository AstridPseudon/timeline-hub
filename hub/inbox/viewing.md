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
