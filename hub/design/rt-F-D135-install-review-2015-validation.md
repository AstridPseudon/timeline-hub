# D135 installed receipt verification

## Result

**PASS.** The actual installed entrypoint is still the exact reviewed
`delivery-build` candidate. Source, installed bytes, mode, regular-file status,
single-link status, and retained predecessor custody all match the installer
receipt. No installation was performed by this review worker.

## Exact identities

- Reviewed source commit: `d45e07dfb305c41d588fe168a2518d5ffa1c4954`
- Reviewed source tree: `92401b1abc84a0a6a23d5b0d9b9bfebeb41638a2`
- Source path: `/home/user/work/wt/rt-F-D135-install-review-2015/ops-delivery-d135/delivery-build`
- Source and installed SHA-256: `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`
- Source and installed mode: `0755`; both are regular, single-link files
- Installed path: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`
- Exact predecessor backup: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build.20261025T201050.398733Z.bak`
- Backup SHA-256: `f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708`, mode `0755`

## Checks

| Check | Result |
|---|---|
| `git rev-parse HEAD HEAD^{tree}` | PASS — exact reviewed commit/tree |
| `git ls-tree HEAD -- ops-delivery-d135/delivery-build` | PASS — mode `100755` |
| `git show HEAD:ops-delivery-d135/delivery-build \| sha256sum` | PASS — `ef9cd…680fd9ca` |
| `git show HEAD:ops-delivery-d135/tests/test_delivery_build.py \| sha256sum` | PASS — `c00401…3286bf` |
| `sha256sum` source, installed path, and named backup | PASS — source/installed exact; backup exact predecessor |
| `cmp source installed` | PASS |
| physical `stat`/`realpath` checks | PASS — regular, single-link, `0755`, no symlink substitution |
| `TIMELINE_DELIVERY_SCRIPT_SHA=ef9cd… python3 -B installed/delivery-build --help` | PASS |
| in-memory `compile(installed bytes)` | PASS |
| prior genuine installed-caller receipt | PASS — 8 focused controls passed |

The focused test source remains byte-identical to the reviewed commit and the
installer receipt. The eight installed-caller controls are not repeated because
the raw installer log and receipt resolve no mismatch; the receipt used a
private in-memory substitution so the caller exercised the installed path and
the exact SHA guard.

The installer’s first post-install neighbor verifier reported a false alarm
because it did not exclude the newly authorized predecessor backup. The
replacement had already completed; its read-back then confirmed all
pre-existing direct `bin` neighbors unchanged, the backup exact, and no
temporary remaining. No second installation or fallback was attempted.

## Boundaries

No source/product code was changed. No build, ZIP, clone, network, package or
venv operation, Store write, child/hub write, production request, host-process
probe, backup rewrite, normal tuple movement, or full suite was run. Positive
delivery remains D59-gated. Downstream callers may use
`TIMELINE_DELIVERY_SCRIPT_SHA=ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`.
