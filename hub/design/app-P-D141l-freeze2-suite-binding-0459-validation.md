# D141l freeze2 paired binding validation

Status: `PROSPECTIVE_PRODUCTION_BUILDER`; `registration=false`; `execution=none`.
This is source preparation only. No submit, registration, checkout request,
preflight, browser, provider import, service request, queue change, test body,
or future submit plan was run or written.

## Authenticated source identities

Read-only Git checks found clean detached exact pins:

| repo | commit | tree | checkout |
| --- | --- | --- | --- |
| App | `5344c53e3063001bb3255bd0c9cd32cc5e77967f` | `dd989783046aeff652486a1ba39db42aea86e201` | `/home/user/work/wt/app-pin-5344c53e` |
| Agent | `8585ed9c0404d0187b2ce70242d25114a32747c2` | `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c` | `/home/user/work/wt/agt-pin-8585ed9c` |
| Runtime | `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` | `ac5b862744bece65b2e30565db1777bacd60da28` | `/home/user/work/wt/rt-pin-6a011d58` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `/home/user/work/wt/vw-pin-635f4de0` |

The genuine App builder is
`/home/user/work/app/scripts/testing/d66-plain-stack.mjs`, Git blob
`59b65214bc74c1ca118b097bc3b13c0ffe480a93`, SHA-256
`2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`,
49,914 bytes. The pure export used was only `serviceRecipe`; no diagnostic
helper was supplied.

## Exact first pair

Target: `app-pin-5344c53e`; repo: `app`; selector:
`p2-automatic-child-placement`.

Normal suite: `d141g-p2-automatic-child-placement-5344c53e-submit`.

- command: `normal-command.txt`
- exact UTF-8 bytes, no terminal newline: 966
- SHA-256: `98522d5511c5e66fcfeaa68044f84eaf9fb45b22e9a1145613a5262be47f21a6`
- exact row plus one LF: 1,022 bytes
- row SHA-256: `0ff8814a6f3a6b62ddff3737aafd2e2d0260b50bc0fb647752f172b2a5de4f5d`

Preflight suite: `d141g-p2-automatic-child-placement-5344c53e-submit-preflight`.

- command: `preflight-command.txt`
- exact UTF-8 bytes, no terminal newline: 978
- SHA-256: `97277b3a42e033819b830ff4f1e450616073d6ea3f6d8e4bd598e32681541ad7`
- exact row plus one LF: 1,044 bytes
- row SHA-256: `bb42880db0cf7987c74ae7da7b82377b467e0e0c76a5439dedfdd86580facbc1`

The row convention is exact row UTF-8 bytes followed by exactly one LF
(`0x0a`), with no CRLF. The command files were independently checked at the
listed byte lengths and hashes.

## Independent prior-row comparison

The supported Node20.19.4 probe called only the genuine `serviceRecipe` pure
builder for the prior 867 tuple and compared its generated full row to the
existing registry lines:

- row 408, `d141-p2-automatic-child-placement-867cb273-submit-preflight`:
  present; actual and expected SHA-256 with one LF both
  `e919663afc6a8637bf9b9e7e81f217f22dd1a69194ccf90b5271cc2891b5a42c`;
  exact match; differences `null`.
- row 409, `d141-p2-automatic-child-placement-867cb273-submit`: present; actual
  and expected SHA-256 with one LF both
  `c0640bd4f2ef25675681514b6dee4c596ebec2931f7e3527dd4fac1ff48fdd6f`;
  exact match; differences `null`.

The current registry preimage was read without mutation:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`,
733,149 bytes, SHA-256
`5ce57b6ee789de40c6d25874a29af37c4fff3d477b913219617eff8b1d01f072`.
Every prospective `d141g-*-5344c53e-*` name in `binding.json` was absent.

## Contract preservation and limits

The packet preserves the existing C0 v2 spelling and shape for the later
caller: request `api_version`, `project_id`, `timeline_id`,
`base_revision_id`, `base_publication_id`, command `schema_version`, `op`,
`version`, `select`, `args`, `created`, label, per-step `id`, `label`,
`intent`, `tags`, `command_ordinals`, `patch`, `reads`, merge mode, top-level
reads, `Idempotency-Key`, `dry_run`, `source`, `rationale`, and `group_id`;
accepted/merged data and receipt fields including canonical document/digest,
normalized commands, id map, base/previous/accepted revisions and
publications, rebasing, records, bindings, effects, dependencies, history,
undo steps, and merge mode; conflict reason/head; invalid code/path/hint and
suggested command; and preview `would_status` with null receipt. No new
receipt or landing schema is introduced.

No code, product, test, fixture, generated, pin, metadata, hub, registry, or
queue file was changed. The later normal D66 `--submit` route must atomically
register each preflight/normal pair after actual paired-kit admission and
compare the registered bytes with this production-builder output before any
dispatch. This packet must not be called installed or actual registered.
