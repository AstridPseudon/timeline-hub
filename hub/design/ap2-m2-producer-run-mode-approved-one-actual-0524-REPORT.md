# App M2 producer run-mode approved one actual — 0524

## Result

**HOLD — no producer actual was submitted.** The task required both the
closed-repair report and an explicit APPROVE from
`producer-run-mode-delta-review-0524`. The repair completed, but the named
review remains an explicit **HOLD** written before the repaired candidate
existed. No actual, browser, hosted build, full suite, install, or product
source change was made.

## Verified frozen source and artifacts

- Frozen keeper HEAD/tree: `17d2518c341c47a2d8634047b400399886da3a2a` /
  `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`.
- Committed wrapper:
  `scripts/testing/run-producer-public13-list.sh`, SHA-256
  `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0`.
- New owned external gate:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-run-mode-closed-repair-0524/final-keeper-gate-run.sh`, SHA-256
  `cc7accb504c5847c379e927de44a470534aec0df370cb0bc523b11c3e8ffcc97`.
- The new gate is byte-identical to the immutable 0501 gate except for the
  `preflight|list|run` usage/allow-list extension. The immutable gate remains
  unchanged.

The source worker’s report is
`ap2-m2-producer-run-mode-closed-repair-0524-REPORT.md`. It records the
required offline dispatch proof and the new central source-only preflight:

```text
ap2-m2-producer-run-mode-closed-repair-0524-ap2-m2-producer-run-mode-closed-repair-0524-preflight-1021052700-1778
exit 0; public13 preflight PASS checks=10
```

The preflight resolved official Composition 13 (`9412ae25…`) while retaining
the private graph as a separate cohort. The exact one-test seam remains the
original config/spec and title; no body/options/timeouts/assertions/pins were
changed.

## Checks and prerequisites

The repair report records PASS for:

- shell syntax, exact gate diff, frozen guard probes, and invalid-mode/root
  refusal;
- real-wrapper offline list/run dispatch to the exact Playwright argv/root,
  no-child refusal for invalid/custody cases, and child status propagation;
- the one complete central source-only preflight above.

At the final read-only check this worktree was clean at the frozen HEAD/tree,
the wrapper hash matched, and disk free space was `13,875,620 KiB` (above the
10 GiB floor). The shared browser lock file
`/home/user/work/.app-m1-browser.lock` was present, so the actual was not
eligible for submission even apart from the missing review approval.

The previous result `...actual-1021052003-6793` remains preserved as an
invocation failure: exit 2, zero collected and zero executed tests, because
the immutable outer gate rejected `run` before child dispatch. It was not
retried.

## Exact blocker and next step

`ap2-m2-producer-run-mode-delta-review-0524-REPORT.md` still says **HOLD**
because it reviewed before the candidate artifact/report existed; it does not
explicitly approve the final new gate or literal actual command. Therefore the
authorization condition for one actual is unmet. Re-run that independent
review against the completed repair, then re-check the browser lock, disk,
two-copy limit, and exact source identity before considering the one registered
actual command. Do not submit an actual from this worker until that review is
an explicit APPROVE.

