# Read-only custody report

- Base: `abd47e68d`; worktree clean.
- Six exact archives verified regular, non-symlink, device `65024`, mode `644`, UID/GID `0/0`; parents exact, root-owned, mode `755`.
- All have `ended` and `recycled`; no `KEEP`, `ACTIVE`, or `running` markers.
- External manager/status/lease/KEEP/test/queue/running-worker scan: zero references for all six. (Only this task brief mentions them.)
- `fuser -v -a` exact six-file probe: exit `1`, stdout empty; stderr listed all six paths with no PID/access/command entries and no visibility errors.

All six: **PASS — unused as of this check**.

Hashes:

- `rt-m2-text-clear-native-private-pair`: 63,924,165 bytes, mtime `2026-10-23 00:45:17Z`, SHA256 `930072b2d582b4f5d6b9f8dd52d534c0469824588004b373ba666702aeceae8c`
- `rt-m3-capture-actual-agent-current-pair`: 64,016,431 bytes, mtime `00:45:37Z`, SHA256 `eaf8dbedff0d62ce68ff8c6468e9f0c6486cbde9ed933fc7f08a2aadf4d840cd`
- `rt-m3-candidate-source-basis-fix`: 63,893,049 bytes, mtime `00:45:27Z`, SHA256 `da0ef58559abaa550c5c9196d1738d2403ed1bb1cec724b74f13e0a15fa5107e`
- `rt-m2-release-s2-final-compose`: 63,938,811 bytes, mtime `00:45:07Z`, SHA256 `f0d9632ec2b5edc867c3f8604490be4c2716aa373dae2635fa224c661568832e`
- `rt-m2-registered-render-canonical-target`: 64,354,756 bytes, mtime `00:44:57Z`, SHA256 `44b212995871f90aad9c9494d94a9a64019b92abde50974540799bd8a4d62a29`
- `rt-m2-producer-record-normalization`: 63,894,747 bytes, mtime `00:44:47Z`, SHA256 `c2004c7406cec0d5850130680f2d9e057dd0afd2e9d996b91d9b160c8e6f1db4`

Aggregate size: 384,021,959 bytes. No cleanup performed; no GB-freed claim. Product tests/lint/typechecks: **NOT RUN**, correctly scoped out.