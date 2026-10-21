# vw-m3-d09-static-role-patch-integrity-join

## Result

Regenerated `PATCH` from the authoritative current-source worktree against
base `5c5173dcb` using Git's actual binary diff, then appended the actual
new-file diff for only `tests/core/timeline/test_scene_roles.py` from
`tl/vw-m3-d09-static-role-declaration-positives`. The packet contains exactly
the four committed product paths plus that 44-line test; no source, geometry,
renderer, or test-retirement edits were made.

The helper remains byte-identical to donor blob
`40f21f323d881b86c3c42f14c7475819d5534aac`. The authoritative source tree is
`951a016df`; the patch base is `5c5173dcb`.

## Packet

- `PATCH` — valid five-path patch generated from actual tree state.
- `FILELIST` — exact changed paths.
- `SOURCE-SHA` — base, source, donor, and joined-test identities.
- `COMMAND` — exact inherited 69-test command and packet verification commands.

## Verification

In a fresh private extraction of `5c5173dcb`:

- `git apply --check PATCH` and forward apply — passed.
- All five changed files compared with `cmp` — byte identity passed.
- Reverse check/apply — passed; `diff -qr` restored an exact base tree.
- Second forward check/apply and byte comparison — passed.
- `git diff --check` — passed on the source worktree.

The exact 69-test command was already run by the declaration worker against
these exact source/test bytes: **69 passed in 1.95s**. Per the brief, this
worker did not replay the 67+2 controls. No full suite, install, push, or
shared dependency mutation was performed.

## Prior packet mismatch

The superseded handoff
`design/handoff-vw-m3-d09-static-roles-current.patch` fails on a fresh base
with `git apply --check`: exit 128, `error: corrupt patch at line 124`.
Its `astrid/sdk/timeline/check.py` hunk declares `@@ -46,13 +46,13 @@`,
whereas Git's actual current-source diff declares `@@ -44,13 +44,13 @@`.
The regenerated packet uses Git's exact headers and passes clean apply and
reverse checks.

## Decisions and limits

The committed four-path product branch was treated as authoritative, and only
the requested declaration-positives test was joined. No manual hunk repair,
broad source merge, private geometry change, or additional test replay was
performed. The harness should commit the current worktree's four source paths
and one new test using the supplied commit message.
