# Handoff: P1 authentic startup seed

Worker `ap2-P1-authentic-startup-seed-0627` made the smallest faithful setup correction on the App test file. Both original P1 cases now publish the unchanged `seedOneClip` document before the existing `enableTimelineAuthoring` restart, so the timeline is present for the normal authoring startup/verified-baseline import. The two case bodies and all assertions remain unchanged apart from that call order.

Source/base identity:

- HEAD/base `f98a5060e9a836245eaaaebb3b124da671e93dc8`
- HEAD tree `39074b54f03070f1746b59e3571b1ab385cc23e0`
- Target base blob `4f0e7a97e67051ccd5c587f7e9ea6c3ae70f9cf2`
- Worktree target blob `96d3e7eced74951574177694fb4e285fea7f91ec`
- Changed path only: `tests/e2e/local/three-products.p1-chain.spec.ts`
- Private graph `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, 80 files; no shared-install changes.

Evidence: App and Node `tsc --noEmit`, scoped ESLint, `git diff --check`, exact two-case source collection, seed-function byte/hash witness, setup-order witness, normalized body comparison, and helper-boundary check all passed. No browser/HTTP/socket/service/body/build/full run was performed. Independent review remains required before merge and service hash update.

