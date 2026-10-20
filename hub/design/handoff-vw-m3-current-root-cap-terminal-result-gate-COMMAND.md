# Terminal result audit commands

Existing central result audited; no new test was submitted.

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-current-root-cap-three-stills-prep-e2e-viewing-current-root-cap-three-stills-1020140356-7643 100
sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-root-cap-three-stills-prep-controller.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-root-cap-three-stills-prep-manifest.json
```

The first command returned `pass exit=0 in 25s`. The second returned the approved controller SHA `079fa981...8dc97` and manifest SHA `4127d7e...90dff`.

Independent read-only pixel audit: Pillow loaded each actual PNG and its frozen MAIN counterpart as native RGB, checked dimensions/mode, raw SHA-256, RGB SHA-256, full histogram, three sample coordinates, and every pixel/channel. Result: all three byte-identical; 2/255 threshold had zero pixels over threshold.

Independent read-only control audit: compared preflight graph with postflight `before` and `after`; checked `valid`, `post_errors`, and `source_outputs_unchanged`. Result: equal, valid, no errors, unchanged; controller-reported owned temp `/tmp/vw-cap-tyoz9eis` was removed.

No browser/render/network/install/service/full-suite action was initiated by this audit. No source TGZ was created: existing immutable public12 tar SHA, 1,427-file manifest, dependency proof, and pre/postflight are sufficient source proof.
