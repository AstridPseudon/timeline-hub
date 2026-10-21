# Gate7 shallow App packer status

Date: 2026-10-21

## Result

No Runtime source or packer change was needed. The authorized shallow-App
handling is already installed in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`

Installed identity: SHA-256
`3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`, mode
`0755`.

The exact installed correction is the independently reviewed source-ancestor
patch, whose candidate SHA-256 is
`3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990` and whose
diff SHA-256 is
`96d5cf2a2a25ee0de656b6685cfcafcf42cdb6f24a751c91b1e502db37e43e71`.
It only changes `_open_extra_source`: source ancestors are opened through
descriptor-scoped `O_DIRECTORY|O_NOFOLLOW`, and the regular leaf is opened
relative to the final directory fd with `O_NOFOLLOW`. The existing safe extras
staging/collision/cleanup/atomic-output controls remain unchanged.

The installed packer also contains the previously reviewed `private_source_view`
handling. For shallow App only, it creates a fresh per-run Git repository below
the private verification temp root, points an alternates file at the source
object store, pins only `origin/main` and `tl/integration`, rejects shallow
metadata and missing reachable objects, and checks the pinned tip and tree
before statistics, patch, or bundle generation. It does not write source `.git`
metadata, fetch or push, loosen equality/checksum checks, or traverse beyond
the private scratch root.

## Current read-only source evidence

Read-only inspection of `/home/user/work/app` found:

- `tl/integration`: `780c502368cb6eb379cf3848af7009067c7cd744`, tree
  `8eed52bb7f8555c7765a8b485e00920bbf906639`.
- `origin/main`: `860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree
  `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`.
- The checkout is shallow, with boundary
  `3f05489e8c5f66870a5401f0aaa5ce6913eb8e11`.
- Boundary `3f05489e8c5f66870a5401f0aaa5ce6913eb8e11` and parent
  `e1d440723d7e75b07c7a60472c78b3f026ee6bbf` are locally present.
- `origin/main` is an ancestor of `tl/integration` (exit 0).

This confirms the settled disposition: the parent-graph symptom is handled by
the owned private view; no App source Git repair or owner Git action is needed.

## Tests and verification evidence

I did not rerun the packer or any test because the fix was already installed,
and the task explicitly says not to change/rerun when that proof exists.

The existing independent review ran the bounded private fixture against the
candidate with:

```bash
PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null \
DELIVERY_TEST_SCRIPT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-delivery-shallow-view-script-fix/delivery-build \
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-delivery-ref-fix-final-review/test_delivery_final.py
```

Result: **11 passed in 2.682 seconds**. The source-ancestor review also
recorded compile/help success, a synthetic symlinked-parent refusal with
descriptor-count preservation, and unchanged frozen payload hashes. No
four-repo dry run, full suite, ZIP, publication, owner scan, or Runtime source
test was run for this task.

## Next authorized dry run

After the coordinated Runtime adoption is complete and real free storage is
at least 10 GiB, run exactly one four-repo dry run with the installed carrier
and the unchanged frozen extras:

```bash
GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1 \
TIMELINE_DELIVERY_SCRIPT_SHA=3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990 \
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build \
  --dry-run --repos "agent runtime app composition" \
  --extra "extras/owner_film_cliplook_scan-v1.0.8.zip=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip" \
  --extra "extras/owner-film-differences.md=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md"
```

The frozen extra hashes remain scanner ZIP
`204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee` and owner
instructions
`969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`.

No final ZIP or publication is claimed here.
