# Ordinary real-batch capture repair

Ready for harness commit; live qualification remains outstanding. Base App `30ebb0ec15c571556b90ef3ecb3defcda9fa0e17` (owner `7d42`/`8c0` included). Followed PLAN 2/3/6; no navigation, source pin, contract, provider/session or dependency changes.

## First mismatch and repair

The retained central report and `central-first-failure.md` contain the HTTP409 but **no raw JSON body**. The driver's EXIT cleanup deleted its binary trace. Accordingly this is a fresh, deterministic reconstruction of the committed `seedThreeProducts` closure and all ten resolved Scene Phase Markers operations (markers 1/6, tail 3), not a claim to have recovered that lost request. Only runtime-specific identities have deterministic stand-ins; all five clips and move/hold intents remain.

Frozen native SDK: `8130a401bf44a518d5a40ae274d398b8c560be55`. Pure replay of the pre-fix App capture reproduces `capture_mismatch: submitted reads does not match authoritative capture`:

- Commands **0–4 match exactly**, including the first occurrence-owned move.
- FIRST differing claim: **command index 5**, `clip.set`, `occurrence:f2-occurrence/clip:f2-plate`, `{values:{hold:3},clear:[]}`; **read index 74** (both arrays have 85 reads).
- App: `{ref:'occurrence:f2-occurrence',path:['track'],state:{state:'present',value:'S1'}}`.
- SDK: `{ref:'occurrence:f2-occurrence',path:['source_offset'],state:{state:'present',value:0}}`.
- Identical read-order defect recurs at command indices **7 and 9**. Other seven commands match. Per-record comparison finds only `reads` differing at 5/7/9; writes, bindings, selections, dependencies, created IDs (all empty), and derived writes match. This is an ordering error, not a different mutation, alias, source pin or ownership decision.

`genericPatchCapture.ts::clipHold` had its own reordered occurrence map paths. Aligned its array with SDK `_clip_scalar_commands._hold_extent` / `capture.MAP_FIELDS`: placement start, at_ms, duration_ms, **source_offset, speed, track, placement.track, time_map, timeMap**, then active flags. Product diff: **3 added / 2 removed lines**. The explicit-clear helper already uses that correct order. No shared owner patch is required; no parent-swap claim is implicated.

After repair, fresh native capture and verification match **all 10 complete commands, all 10 complete records, independently opened original bundle, and final authored bundle**. Native execution receives the original complete command list atomically, without claim filtering. App regression also checks immutable original parent/placement/source basis, original source pin dependencies, order, no births, transition and opaque clip preservation. Neither SDK nor App input mutates. One real-batch regression plus a 5.5KB input fixture and a small pure Python comparison helper; no matrix or generated record dump committed.

## Public013 boundary

Read Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` artifacts with `git show`. Its command schema is byte-equal to SDK8130, SHA256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`. All ten commands, the `CommitRequest`, and ten `CommandRecord`s validate against the exact public013 bundled schemas. Thus this capture defect does **not** require a private cohort or counterpart contract patch. This proves schema/capture compatibility for this batch, not live Runtime publication, retry or undo qualification.

## Exact verification

All commands ran from `/home/user/work/wt/ap2-m2-ordinary-real-capture-contract-repair`.

```sh
ORDINARY_CAPTURE_OUTPUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-real-capture-contract-repair/app-capture-after.json ./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/commands/ordinaryRealBatch.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/ordinaryMoveMember.test.ts src/tools/video-editor/commands/ordinaryScalarMember.test.ts
```

**PASS: 4 files, 26 tests**, exit 0 (final run 4.61s).

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-real-capture-contract-repair/run-pure.sh
```

**PASS**, exit 0: original capture reproduces the precise first failure, then `10/10 exact native commands and records; opening, final bundle, original basis verified`. Uses one private SDK8130 archive at a time with EXIT cleanup and read-only `/home/user/work/venv-app2-native`; no installs or shared cache writes. Retained `pure-result.txt`, `compare.py`, and before/after JSON are in that worker folder. Initial archive omitted `pyproject.toml` and failed import before comparison; adding that exact source metadata fixed setup without altering SDK code or version.

```sh
/home/user/work/venv-app2-native/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-real-capture-contract-repair/check-public013.py
./node_modules/.bin/eslint src/tools/video-editor/commands/genericPatchCapture.ts src/tools/video-editor/commands/ordinaryRealBatch.test.ts --ext ts --report-unused-disable-directives --max-warnings 0
git diff --check
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-real-capture-contract-repair/later-gate.sh
```

**All PASS**, exit 0. No full suite, project-wide typecheck, request-test, driver, browser, socket, renderer or live Runtime was run. No commits, merges or integration/shared dependency writes. No build output remains in the worktree.

## Later gate (staged, NOT executed)

After the harness commits this candidate, the exact command is:

```sh
sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-real-capture-contract-repair/later-gate.sh
```

It checks clean candidate source and ancestry, then submits exactly:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-real-capture-contract-repair e2e-m2-ordinary-committed-driver-gate) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The registered driver retains exact SDK8130 / Runtime2c4 / public Composition13 and existing graph/bin/source guards, selecting the original ordinary journey with all ten commands. If wait exits 124, wait on that same R; do not resubmit. Recommend that single committed-source gate next; lost-ACK/restart/exact retry/guarded undo and zero-legacy remain unverified here. No current blocker to committing this bounded repair.
