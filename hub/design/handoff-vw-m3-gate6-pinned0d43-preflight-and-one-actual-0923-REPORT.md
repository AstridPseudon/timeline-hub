# Gate6 KEEP-pin preflight and one-actual handoff — 0923

## Result

**FAIL CLOSED before central request.** The exact KEEP source exists and is
clean, but the checkout has no ignored runtime prerequisites:

- `/home/user/work/wt/app-pin-0d432391/node_modules` — missing

The packet uses the retained d00 dist explicitly at
`/home/user/work/wt/app-pin-d00a6613/dist`, after checking d00's exact HEAD
and no KEEP-source build-input diff outside the approved `cases.ts:91` hunk.
The exact packet therefore cannot reach source validation. No central
preflight request and no physical request were submitted. No grant, marker,
browser, Runtime, helper, socket, media, or raw physical result was created.

## Source and packet

- App source: `/home/user/work/wt/app-pin-0d432391`
- Commit: `0d4323913b92c4e0e3830bf14ec7f35d981475ca`
- Tree: `5a1e0e85d0f336f642426b91ccf3b3f1984ebd14`
- Source is clean and `d00a66134f330672ea7471dc69db38c1566d94cf` is an ancestor.
- The only source diff is `tests/e2e/timeline/viewing-parity/cases.ts:91`.
- The UI filename assertion at line 159 remains `authoredOutput.file`.
- Source member binding remains the reviewed `5902` files and
  `sha256:4fb1e53b2dce325f826b6b071d0782544e5ba2c7b27418b6170f8c947c450435`.
- Fresh packet namespace: `gate6-20261021T0923`.
- Packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-pinned0d43-preflight-and-one-actual-0923/packet`
- Source lease: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/notes/gate6-app-pin-0d432391.lease`

The packet changes only the source path, retained-d00-dist binding with an
explicit build-input equality guard, namespace, approval text, and packet
checksums from the 0916 donor. The old 0916 packet and source were not edited.

## Evidence

Static checks from ORCH cwd passed:

```text
(cd /tmp && bash -n <packet>/run.sh <packet>/preflight.sh)
(cd /tmp && node --check <packet>/prepare.mjs && node --check <packet>/issue.mjs && node --check <packet>/dist-availability.mjs)
PYTHONDONTWRITEBYTECODE=1 python3 -B <packet>/short-player-temp-controls.py --self-test
```

All packet checksum, Bash, Node, Python AST, and short-temp self-tests passed.
The exact local command
`bash <packet>/run.sh --preflight` exited `1` at the missing
`app-pin-0d432391/node_modules/tsx/dist/loader.mjs`; its owned temp root was
cleaned and fd9 remained owned by `run.sh`.

The complete prerequisite list found:

- PASS: exact source files, source identity/cleanliness/ancestry, one-line
  delta, unchanged UI filename assertion.
- PASS: retained d00 dist used by the packet: 339 files, index
  `aeb5d83399b453b15a8cbc67b31260cf2820f8d65770ccd458986ddd551e257b`, manifest
  `43e2cd02d757f6f63833b7c4b89fc9241fd1ba41fa6b2dd8723ac398af070ed4`.
- PASS: existing private d00 App graph `8bdc44e93ce6f712f2a26fc44f1f8e904215c1785f54ed97f826a98fe0145c5b/32393`;
  frozen Runtime graph `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c/21455`.
- PASS: Runtime official artifact count `75`; public13 Composition archive
  regular-member count `77`.
- PASS: Node `v20.19.4`, SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`;
  Chrome headless shell SHA-256
  `63eca986a3fe7f523d2d6e79d9f13daf4f1c73c1d9013c2c4a05b123510145b4`.
- PASS: short socket path bound (`48`-character temp root; socket path under
  the 100-character requirement), clean child-env unsets, single fd9 ownership,
  negative/cleanup controls.
- PASS: latest measured free bytes `11720073216`, above staging threshold
  `11320247244` and floor `10737418240`.
- FAIL: exact KEEP App `node_modules/` is absent. The separately existing d00
  graph cannot be substituted: the guards require the exact source root and
  reject shared/escaping graph links.

## Decision and next step

No decision was made beyond the settled fail-closed rule. Do not install,
copy, symlink, hardlink, or modify shared dependencies or the exact source
checkout from this worker. The dispatcher/manager must materialize an approved
owned `node_modules/` for the exact KEEP pin, or provide an explicit
preflight-compatible owned graph. The retained d00 dist may remain the
direct-dist input only while its equality guard passes. Then rerun the full
prerequisite list and obtain fresh authority; this packet's central requests
were not spent.
