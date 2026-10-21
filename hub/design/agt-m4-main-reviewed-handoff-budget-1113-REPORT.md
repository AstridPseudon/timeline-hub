# Final MAIN handoff consolidation — 2026-10-21

## Disposition

`CODE APPROVED / STORAGE HOLD` remains unchanged. The approved wrapper is
`fc4c23d079f17aa4d8f167b385c7e5bda2edd299`, with SHA-256
`0e1b5ccd2157788d53d6ba7fa6c0e1adc362e97f190e734cc023bf4ff92e87d`.
The frozen product is Agent `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40` /
tree `3467b7bffb0fe6edf9178c9a9de4d446c8ab8857`; C13 Composition 0.0.13
remains required. The immutable `agent-remotion-0014` runtime must be built
from that exact b3c source; existing 0013 is stale 30da and is not a
substitute.

## Exact prerequisites

1. Clean exact Agent b3c/tree3467, Runtime b92/tree6abc, and client
   95bd/tree d3a290 checkouts under the MAIN source root, with Agent
   `runtime.lock.json` pinned to client 95bd.
2. Immutable `/home/user/work/runtimes/agent-remotion-0014` with b3c
   `.source-commit`, C13 0.0.13 tarball SHA-256
   `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, C13
   lock SHA-256
   `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`, and
   private symlink-free `node_modules`.
3. The durable runner must match the approved wrapper identity; the private
   profile must contain the 164-pin carrier
   `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`, the
   three local product wheels, exactly 166 distributions and 166 `RECORD`
   files, eight private import origins, and source/wheel/install byte parity.
4. Node v20.19.4, VibeComfy, ffmpeg and ffprobe must pass. MAIN must use the
   exact `env -i` command and preserve the direct final
   `exec "$PROFILE_PY" -m pytest -q -n 3 "$@"`.
5. MAIN must observe more than `13,958,643,712` free bytes on its own
   `/home/user/work` filesystem immediately before admission.

## Storage evidence

The retained `du -sx -B1` setup subtotal is `1,254,760,448` bytes
(`1.168587 GiB`): profile reference `716,853,248`, source-checkout analogues
`143,859,712`, and old C13 reference runtime `394,047,488`. The b3c-source
0014 runtime is absent from that measurement. Transient setup/full-run peak
with `-n 3` is **UNKNOWN**, so the >13 GiB floor is not lowered.

The worker-side read-only command `df -B1 /home/user/work` currently reports
`12,755,468,288` bytes free (`11.879456 GiB`), leaving a gap of
`1,203,175,424` bytes (`1.120544 GiB`) to the threshold. The retained
measurement at 2026-10-21T10:51:38Z reported `12,480,892,928` bytes free
(`11.623737 GiB`), a `1,477,750,784` byte (`1.376263 GiB`) gap. MAIN's
earlier note reported approximately 11 GB; that is separate from this
worker-side local observation and does not qualify MAIN admission.

## Action / blockers

- Lead: obtain the missing MAIN storage, then have MAIN request and verify
  the b3c-built 0014 runtime and materialize/audit the private profile.
- MAIN: after every prerequisite is present, make exactly one allowed full
  request and write the terminal result; do not claim a result from setup or
  preflight.
- Blocked now by insufficient free storage, absent/unverified 0014 runtime,
  absent/unverified private profile, and unknown transient peak.

No build, install, run, full request, named-suite request, release, adoption,
pin, or activation was performed by this worker.
