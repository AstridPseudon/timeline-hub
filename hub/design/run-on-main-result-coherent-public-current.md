# MAIN handoff disposition — no full result yet (2026-10-21)

**CODE APPROVED / STORAGE HOLD.** This note is a consolidated action and
blocker record, not a setup refusal relabelled as a full result. The approved
wrapper is commit `fc4c23d079f17aa4d8f167b385c7e5bda2edd299`, tree
`7ce6a0b8022928cd98a2f7cd448bf9d24a442587`, blob
`198a94ad1f1c9921705399febb7e7f71dffd419d`, SHA-256
`0e1b5ccd2157788d53d6ba7fa6c0e1adc362e97f190e734cc023bf4ff92e87d`.
The frozen product is Agent b3c/tree3467 with C13 Composition 0.0.13, not
C13/14; the new immutable `agent-remotion-0014` runtime must be built from
the exact b3c source.

## Required before MAIN can run

- Clean exact Agent b3c/tree3467, Runtime b92/tree6abc, and client
  95bd/tree d3a290 checkouts under
  `/home/user/work/main-timeline/coherent-public-current-b3c96a758/source/`,
  including Agent `runtime.lock.json` pinned to client 95bd.
- Immutable `/home/user/work/runtimes/agent-remotion-0014` with b3c
  `.source-commit`, the C13 0.0.13 tarball and lock hashes recorded in the
  request, private symlink-free `node_modules`, and generated env pointing to
  it with Node v20.19.4. Existing 0013 is stale 30da and is not a substitute.
- Approved wrapper at the durable MAIN runner path, a private profile at
  `/home/user/work/main-timeline/coherent-public-current-b3c96a758/profile/agent-coherent-public-current-b3c96a758`,
  its 164-pin carrier, three local product wheels, 166 distributions, 166
  `RECORD` files, eight private import origins, and source/wheel/install byte
  parity.
- Node, VibeComfy, ffmpeg and ffprobe checks; exact `env -i` invocation;
  direct wrapper final command `exec "$PROFILE_PY" -m pytest -q -n 3 "$@"`.
- MAIN must observe `df -B1 /home/user/work` free space strictly above
  `13,958,643,712` bytes before admission. The current worker-side read-only
  value is `12,755,468,288` bytes (`11.879456 GiB`), a gap of
  `1,203,175,424` bytes (`1.120544 GiB`). MAIN's earlier note says about 11
  GB; it must measure its own filesystem at admission.

## Retained storage evidence and disposition

The measured setup subtotal is `1,254,760,448` bytes (`1.168587 GiB`) from
retained `du -sx -B1`: profile reference `716,853,248`, source-checkout
analogues `143,859,712`, and old C13 reference runtime `394,047,488`. This
does not measure the b3c-source 0014 runtime. Transient full-run/setup peak
with known `-n 3` concurrency is **UNKNOWN**; there is no basis for adding a
2 GiB margin and lowering the >13 GiB floor. At the measurement timestamp,
`df -B1` was `12,480,892,928` bytes free (`11.623737 GiB`), short by
`1,477,750,784` bytes (`1.376263 GiB`).

## Exact next action / block

Lead must free or obtain the storage gap, then MAIN must request and verify
the b3c-built 0014 runtime, materialize and audit the private profile, and
make exactly one allowed full request. No build, install, run, full request,
named-suite request, 0013 substitution, C13/14 substitution, release,
adoption, pin, or activation is authorized by this note. The terminal full
result remains unwritten until those prerequisites and the exact run are
complete.
