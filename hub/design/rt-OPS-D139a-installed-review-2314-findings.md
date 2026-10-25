# D139a installed-custody/security review

Verdict: **PASS_INSTALLED_CUSTODY**.

The authorized D139a combined install is present and byte-exact:

- `ORCH/bin/make-child-venv`: SHA-256 `fd83c9e2…4fc22b5`, 111171 bytes, mode 0755, owner UID 0, regular single-link non-symlink.
- `ORCH/bin/request-child-venv`: SHA-256 `60d2238a…412504`, 18066 bytes, mode 0755, owner UID 0, regular single-link non-symlink.
- `ORCH/bin/check-child-imports`: SHA-256 `8215f5d9…a272d7c`, 14033 bytes, mode 0755, owner UID 0, regular single-link non-symlink.

The installed maker and wrapper match the reviewed composition source at commit
`0921ec1c8eb7cab668203963c5a5eeb0e4616c00`, tree
`577a3cca4e23c94d051e839eb47d7b1bd7a1c9c3`. The source worktree is clean; no
uncommitted source identity was used.

The maker backup is the exact authorized f07 preimage
`f07b8093…b969f`, 75541 bytes, mode 0755. The wrapper backup is the exact
authorized bdda preimage `bddaee9c…55e94`, 15435 bytes, mode 0755. Both are
regular single-link files owned by UID 0. Protected `bench_store.py` and
`verify_dependency_seed.py` retain hashes `123bb93c…adfe2` and
`116b4e6b…d7bfe2`; prior backup hashes match their earlier receipts. No install
lock remains.

The reviewed helper and receipts preserve descriptor-bound CAS, O_NOFOLLOW,
O_EXCL/no-clobber, identity checks, atomic rename, readback, and lock controls.
Independent private wrong-preimage, symlink-destination, and existing-backup
controls refused as expected. The checker’s initial-target absence is
receipt-supported and its O_EXCL/O_NOFOLLOW route is source-supported, but the
historical absence cannot be re-observed after the checker was installed; it is
not claimed as a fresh pre-install observation.

The normal caller path is wired: the installed wrapper parses and emits the
schema distribution/manifest pair once in the normal `CHILDVENV` pending-row
shape, preserves the source carrier, and the installed maker parses both schema
flags, validates the physical inputs, forwards source/manifest paths into the
existing verification path, and binds `__timeline_schema_identity__` in the
existing Store-key path. This was checked statically and by the five private
installed-wrapper queue/parser controls. No live queue was touched.

The D137 decision verifier accepted the real receipt: authorization D137,
fixture gate WITHDRAWN, E2E NOTRUN, `e2e_pass=false`, CAS_MANAGER_ONLY, and
`production_install=false`. The canonical checker result is diagnostic only:
expected exit 1, 1146 census rows, 22 probes, 12 missing canonical names, 12
failures, zero missing installed distributions. It does not claim a real child.

No source edits, new installer, replacement, rollback, cleanup, Store/index/
registration mutation, package acquisition, child/venv, Farm, provider,
browser, full suite, or body run was performed.

## Separate publication and Farm status

This review qualifies installed custody only. A source hash is not a remote
installed receipt. No D139a hash/commit publication record was found under the
normal local hub tree; the central design copies are not treated as a remote
kit receipt. Kit publication remains pending/manager-owned. Farm receiving,
child acceptance, and D140 core revenue remain unverified and separately
gated.
