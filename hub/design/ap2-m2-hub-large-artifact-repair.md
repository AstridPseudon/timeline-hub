# App2 hub artifact repair

Status: App2-owned runtime artifacts are outside the synced design root.

- Archive moved from `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-ap2-m2-locked-graph-source.tar` to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar`.
- Graph moved from `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-ap2-m2-locked-graph/` to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph/`.
- Finished App2 strict-diff snapshots moved from `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-native-helper-strict-diff/` to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-hub-large-artifact-repair/artifacts/ap2-m2-native-helper-strict-diff/`.
- Archive bytes: `300830720`; SHA-256 before/after: `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.

Repointed consumers: `app-ap2-m2-locked-graph-wrapper.sh` (`GRAPH`,
`SOURCE_ARCHIVE`), `normal014-source-common.sh` (`LOCKED_GRAPH`,
`LOCKED_GRAPH_ARCHIVE`), the locked-graph lease, and the graph report. The
moved graph's three private package links now target its moved private copies;
shared `/home/user/work/app/node_modules` links were not changed. No archive or
App2 graph/generated environment directory remains under `design/`.

Validation: `bash -n` and `sh -n` passed; `verify_locked_graph` passed; the
wrapper's ordinary native probe passed (`0`) and its known project typecheck
returned `2` with the same 10 existing diagnostics. No active archive reader
was present. No browser, full, live-socket, or product suite was run.

Sync note: no App2-owned file over 50 MB remains under `design/`, and no
design symlink targets a large App2 environment. Two unrelated Viewing-owned
archives over 50 MB remain untouched:
`handoff-vw-m3-pcm-caller-current-land-unit-TREE.tar.gz` and
`handoff-vw-m3-main-image-cap-source-vector-main-source.tar.gz`.
