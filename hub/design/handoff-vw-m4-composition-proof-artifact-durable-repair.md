# Composition M4 proof artifact handoff

The completed clean-main proof artifacts are durably located at:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-composition-proof-artifact-durable-repair/delivery/composition-origin-main-to-ac918bb64.patch`
  SHA-256 `60a82dff67e7516cb17439910d7e44fe70122218add4bc8a72452aa6c0f6c26b`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-composition-proof-artifact-durable-repair/delivery/composition-origin-main-to-ac918bb64.bundle`
  SHA-256 `c49d2638b3118aa9d2c0b7584a72151cc7e3c8a7303f6acdecff404d95861532`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-composition-proof-artifact-durable-repair/delivery/report.md`
  SHA-256 `24c3b92c860a2b1fc97a34b269ab55e535db4aeef9a1aedca96f33a3dd428240`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-composition-proof-artifact-durable-repair/delivery/COMMAND`
  SHA-256 `ee76bb4d883b6ea9b47990b9e5a4e7ef4758655a8ec77ea7fdc66a8ae0741488`

The predecessor harness tested source commit
`ac918bb645d2ee4e8e36bbb98df02fb732176475`, source tree
`d23317a0cec4dbff51f12737adf0982cc3a4fdc1`, against fresh `origin/main`
commit `67b8aa3d0d6831d3e3504a340ff583c3da253707`, main tree
`62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`. The patch applied cleanly and
matched all 113 tracked paths, modes, and blobs; the main archive had 29/29.
Bundle verification, ancestry, and `git diff --check` passed.

The immutable public 0.0.13 archive remains SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` with 77
members. Central result `composition-full-1020223241-16395` remains PASSED
with 78 passed, 0 failed, and 0 skipped. This repair performed no test or
build rerun.
