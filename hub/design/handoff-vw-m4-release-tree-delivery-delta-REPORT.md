# Composition14 release-tree delivery delta

Prepared an unapplied, fail-closed refresh command for the reviewed source
tree `d2fcf410` at `3a675f38`, rooted at `origin/main=67b8aa3d` (tree
`62f4456b`; merge-base and ancestor check pass). Relative to the existing e7
delivery, the exact delta is nine modified paths: six authored source/test
paths (`fade-up`, `scale-in`, `clip-look`, `scene-evaluation`, and the two
scene tests) plus `CHANGELOG.md`, `package-lock.json`, and `package.json` for
the approved 0.0.14 metadata.

The live `/home/user/work/composition` integration ref remains e7, so no new
patch or bundle was generated. The command waits for that ref to carry the
reviewed source tree, then uses the existing binary `git diff` and `git bundle`
recipe only. It preserves scanner 1.0.8 (`204a7aac…c93ee`) and the installed
carrier (`3dfd5c28…3e990`) by hash-checking them without invoking or replacing
either. No tests, archive, whole-ZIP, scanner, or final census claim is made.

Runnable command: `workers/vw-m4-release-tree-delivery-delta/COMMAND`.
