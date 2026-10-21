# REQUEST CHANGES — 1048 complete-layout custody delta

Independent process-custody result: **REQUEST CHANGES**.

The 1048 terminal stage worker returned **DO NOT COPY / DO NOT STAGE**. Its
prospective root was
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-complete-owned-runtime-layout-budget-1048/owned-stage/`,
but that path is absent. No stage script, final root/manifest/graph hashes,
or fresh validation attachment exists, so no complete-layout bytes can be
approved.

Measured storage block:

```text
free before stage       11,306,307,584
central minimum         11,320,247,244
normal floor            10,737,418,240
owned-stage allocation     394,166,272
exact STORAGE NEED          408,105,932
```

The hypothetical post-stage free space is `10,912,141,312`, below the central
minimum. The worker’s phrase “below both” the central minimum and normal floor
is a wording error: it remains above the normal floor by `174,723,072`; the
central minimum is nevertheless binding. Review-time read-only `df` showed
`10,988,228,608` available bytes, and the stage remained absent.

Independently rechecked prerequisites all pass: Runtime graph
`4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c` / 21,455
entries; lock `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`;
public13 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` /
77 members; Node20.19.4 hash
`43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`; contained
regular in-project CLI with `nlink=1`; and all six 1028 sibling files match
frozen Agent d0a byte-for-byte. The 1028 capsule has 26 regular files, no
symlinks, and `nlink=1` throughout. These are prerequisites only, not proof of
an independent final root.

Missing before approval: an independent final copy/reflink with distinct
inodes, final graph/bin-link census, final-root package/lock/registry/source/
authority hashes, fresh validation bound to final path/context, and an
executable stage script proving cleanup, failure propagation, storage guards,
and linked-ancestor/foreign-CLI rejection. The old artifact must not be copied
or used as proof.

No shared writes, install, copy, browser/helper/Runtime/socket/export/token,
or full suite occurred. Required next step: recover at least **408,105,932
bytes**, rerun staging, then review the actual stage and script independently.
