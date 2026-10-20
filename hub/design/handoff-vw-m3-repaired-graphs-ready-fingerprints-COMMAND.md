# vw-m3 repaired graphs ready fingerprints commands

Generated: 2026-10-20T16:56:48.029Z

All commands were read-only. The one-off adapter script was run from the worker worktree and removed after artifact generation.

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node --check scripts/worker-ready-fingerprint.mjs`

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node scripts/worker-ready-fingerprint.mjs`

`python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/lead/node-modules-repair-compare.py`

Observed repair comparison: `mode: controller.inventory | manifest 21495 current 21495`; `missing 0 changed 0 added 0`.

The adapter imported the existing controller's `hashTree` and `packageGraphFingerprint`, used in-process gzip/tar parsing for the approved archive, and emitted the full physical manifests plus six scoped peer hashes. No test command was run because this task is explicitly read/stat/hash-only.
