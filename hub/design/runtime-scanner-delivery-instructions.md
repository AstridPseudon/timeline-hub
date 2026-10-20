# Scanner delivery instructions

For the separately authorized final build, use the installed `delivery-build`
carrier's existing repeatable arguments with the unchanged frozen payloads:

```bash
--extra "extras/owner_film_cliplook_scan-v1.0.8.zip=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip" \
--extra "extras/owner-film-differences.md=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md"
```

Expected payload hashes are scanner ZIP `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee` and owner instructions `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`. Composition's current piece is `e7ef7a`, not historical `ac918`.

This note records the arguments and installation state; no final ZIP, owner scan, or completed-gates claim is made here.

## Final carrier installation

At 2026-10-20T23:38:33Z, the exact independently approved source-ancestor
candidate was installed at `$ORCH/bin/delivery-build`:

`3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`

The installed mode remains `0755`. The frozen payload paths above are unchanged
and remain the exact delivery inputs:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip` — SHA-256 `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md` — SHA-256 `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`

Only the approved source-ancestor patch was installed; no final ZIP, four-repo
build, owner scan, or completed-gates claim is made here.
