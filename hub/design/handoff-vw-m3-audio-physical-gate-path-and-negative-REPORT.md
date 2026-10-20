# Report

- Confirmed case4 does not reach `compareNativeAudio`; it only captures/probes the tab stream.
- Published one unapplied test-only patch: [proposal.patch](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-audio-physical-gate-path-and-negative/proposal.patch>).
- Patch wires real Player capture PCM to the same CPU export PCM, then checks a planted half-gain failure after the positive comparison.
- Added cheap source-reachability/order assertions; no product, pin, grant, source-freeze, or frame-negative changes.

Tests passed:

- `audio-join.test.ts`
- `canvas.test.ts`
- `tab-audio.test.ts`
- Candidate temporary apply: `canvas.test.ts`, ESLint
- `git apply --check proposal.patch`

Targeted TypeScript check remains unverified due existing unrelated `.ts`-extension, harness typing, and `tab-audio.ts` errors.

No browser, render, live capture, full suite, install, or physical qualification was run. Artifacts: [report.md](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-audio-physical-gate-path-and-negative/report.md>), [COMMAND](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-audio-physical-gate-path-and-negative/COMMAND>), [commit-msg](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-audio-physical-gate-path-and-negative/commit-msg>), and `DONE` are present.