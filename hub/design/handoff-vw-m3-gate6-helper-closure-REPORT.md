# Gate6 frozen pack-host helper closure

## Result

The frozen App tuple cannot safely launch the real pack host yet. The exact
failure from central `...28498` is preserved: Agent d0a's clean tree does not
contain `tests/packs/rendering/real_pack_host.py`. No central rerun, activation,
browser, render, socket, credential, or marker operation was performed.

The reviewed helper is available only as committed Agent history, not as a
supported current carrier:

- source commit: `b70b9d569b2c80885d72734c61cd57e64c3715a8`
- source tree: `687f077c4771e3dbb66bfb7ff2b98f310ac054b6`
- path: `tests/packs/rendering/real_pack_host.py`
- blob size: `10,938` bytes
- blob SHA-256: `bc75d73f21c6310efad7fc41e4a3d790bfe3a8975e0eb96c08c3dec63e62961b`
- parent: `c9284b892e76394c511e0b2b8d81473979f211a8`

The frozen Agent source is `d0a5072bbe7b7ce9489f43aa0a81027ec400343b`
(`6adb4a1190dfb2874e101565f37eccd392b1ae2f`) and the frozen Runtime source is
`8f105c26e3b62f9c2683f717a9773a12bc775a8e`
(`b7f456d5135cba6049980ebc43a91c7a72ab8f7e`). The helper commit is an
ancestor of d0a, but later d0a commits delete the helper path. Current
`/home/user/work/wt/vw-m3-host-agent-source`, `/home/user/work/agent`, and the
current `/home/user/peteromallet/astrid-agent` do not carry the helper. The
remaining copies are worker scratch/overlay artifacts and are not supported
source carriers.

## Compatibility proof

Static checks passed that the reviewed helper is syntactically valid and its
imports/calls are present in d0a. With d0a first in `PYTHONPATH`, these resolved
from the d0a checkout: `RuntimeProtocolClient`, `host_bootstrap.ensure_pack_host`,
`PACK_HOST_ACTOR`, `PACK_HOST_SCOPES`, the host custody/cleanup helpers,
`_pack_host_lock`, and `_safe_local_path`. d0a's `ensure_pack_host` accepts the
helper's `reconfigure_action` and `startup_idle_seconds` call. This is only a
source/API compatibility proof; it is not a live Runtime8f or host-start proof.

## Unapplied patch

[PATCH](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-frozen-pack-host-helper-closure/PATCH)
is one minimal test-only App patch. It:

- adds `ASTRID_PACK_HOST_HELPER_CHECKOUT` as an explicit private carrier;
- requires the carrier to be a separate realpath and verifies exact b70 commit,
  tree, path containment, regular-file status, size, and SHA-256;
- performs that refusal before Runtime/fixture startup and rechecks before spawn;
- invokes the reviewed helper by file path through the existing child-process,
  stdin stop, and cleanup seam;
- puts frozen d0a before Runtime in `PYTHONPATH`, so normal provider imports
  remain d0a rather than silently switching to the helper carrier;
- includes one configured positive-carrier test and one missing/wrong-carrier
  refusal test.

The patch was mechanically imported with `tsx`, its refusal test passed in the
temporary applied validation, `git diff --check` passed, and `git apply --check`
passes against the clean App base. The positive test was not run because no
owner-approved b70 carrier exists on this machine.

## Remaining static cheap prerequisites

Before a future physical run, the harness must also pass all existing guards:

1. central boundary: no viewing `QUIET.md`, browser flock held;
2. Runtime Python/checkout and Agent Python/checkout, exact explicit import
   origins, and the helper carrier guard above;
3. current hosted production `dist/index.html` and hosted-origin asset marker;
4. OpenSSL, `ffmpeg`, and `ffprobe` for certificate, video, and PCM fixture
   bootstrap;
5. Node `v20.19.4`, exact export headless-shell/browser bytes, selected Player
   browser profile and bytes;
6. frozen tuple schema/paths, App content freeze, exact Agent/Runtime/
   Composition HEAD/tree/cleanliness, and exact Runtime client file graph;
7. exact Composition 0.0.13 artifact bytes and 77-member package graph for
   both App and Agent, six pinned Remotion/Player peer files per consumer;
8. selected Remotion project realpath and Agent export-browser environment;
9. temporary Runtime realm/support directories, free direct ports, Runtime
   startup/health, product credential, and the normal worker credential and
   discovery contract created by the real Runtime;
10. native fixture generation/import, then the real host's `rendering.render`
    process readiness and Runtime catalog readiness.

The existing `harnessUnavailableReason()` covers only Runtime Python, hosted
dist, and OpenSSL; the remaining items are enforced later by sourceVersions,
fixture setup, or the bootstrap. The helper absence therefore arrived late in
28498 even though it was statically knowable.

## Exact peer requirement / blocker

Agent/Home must provide a read-only checkout/carrier whose realpath is pinned
to b70's exact commit/tree and contains the exact helper blob, or land the
reviewed helper into d0a and publish a new Agent HEAD/tree tuple. Viewing then
needs the carrier path supplied as `ASTRID_PACK_HOST_HELPER_CHECKOUT`; no
generic waiting, copied helper, source-label change, or central rerun is safe.

