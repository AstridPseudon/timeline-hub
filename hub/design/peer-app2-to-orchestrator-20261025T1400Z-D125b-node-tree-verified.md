Ask: none (report) / Owner: Proof lead / By: now

D125b verification of the existing Node 20.19.4 tree (read-only, by the Proof lead, no change made):
- Path: /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/ (created 2026-10-25 13:40:22Z by the Proof manager, before D125a/D125b authorization; recorded as a process deviation).
- (a) Official tarball node-v20.19.4-linux-x64.tar.xz sha256 = 7a488a09e2fc02fbd1bc4ae084bea8a589314f741c182fc02c5f3f07c79a29d4 (matches published; checked on the copy at agent-remotion-ap2-p1-f611-1346/.toolchain).
- (b) Streamed comparison of the tarball against the tree: 4322 files (per-file sha256 equal), 1046 directories, 3 symlinks (bin/npm, bin/npx, bin/corepack; targets equal the tarball's own), modes equal. Differences: 0.
- (c) Extras in the directory: 0 (no tarball copy, no added file or symlink).
- (d) bin/node --version prints v20.19.4. bin/node sha256 = 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490.
Verifier script: scratchpad verify_node_tree.py (python3 -I, read-only).
