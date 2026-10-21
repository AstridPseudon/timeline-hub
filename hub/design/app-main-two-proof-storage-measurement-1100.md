# App main: measured storage for the two approved proofs

Date: 2026-10-21  
Scope: `automatic1490` and `publicTrim0cc` only  
Mode: read-only measurement; no copy, install, build, browser, test, or new graph was run

## Decision-ready result

The two proofs can be run serially from the measured storage baseline. The
reusable materials and the automatic runner's known physical overlay total
`1,524,616,676` bytes (`1.420 GiB`). Reserving `2 GiB` for the unrecoverable
per-run transient peak and a further `2 GiB` margin gives a conservative
planning envelope of `5,819,583,972` bytes (`5.420 GiB`) for one active App
source slot. Keeping both App source slots at once would raise that envelope to
`6,116,761,119` bytes (`5.697 GiB`); serial execution should release the first
slot before materializing the second.

Against main's stated `11 GiB` free space (`11,811,160,064` bytes), the
one-slot envelope leaves `5,991,576,092` bytes (`5.580 GiB`) free. It therefore
leaves more than the stated `5 GiB` refusal floor, subject to the existing
source-runner and global guards continuing to pass. This is a storage budget,
not permission to lower any guard.

The exact peak of the build output, Runtime realm, browser profile, and
per-run caches was not retained. The `2 GiB` transient reservation is an
explicit conservative allowance for those unknowns; it is not being presented
as an observed peak. If main needs a proven byte-for-byte peak rather than this
bounded admission budget, the result is `UNKNOWN` until a permitted run records
it. No approval request or wrapper change is justified by that uncertainty.

## Approved identities

| Proof | App commit | App tree |
| --- | --- | --- |
| automatic1490 | `1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf` | `8e242d1497841f391b6152ecd8d204143fa03b52` |
| publicTrim0cc | `0cc2583aaf07e89190b9344b5ac82849d6279586` | `320e74a93676c781e83885b86ec237b4a1465d80` |

Both use Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
`2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, and Runtime
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`.

The public13 Composition archive is present in the App source at
`vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`:

- `58,477` bytes;
- SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`;
- `77` regular tar members.

The archive is already part of the App source-slot measurement below and must
not be counted again.

## Measured reusable materials

All values are `du -sb` physical-byte measurements unless noted.

| Material | Path | Bytes | Reuse/accounting |
| --- | --- | ---: | --- |
| App source slot, exact `publicTrim0cc` checkout | `/home/user/work/wt/app-m4-main-proof-measured-footprint-r44` | `297,177,147` | One active slot; `node_modules` is a 32-byte symlink and is not dereferenced. This is the conservative source-slot cap for either serial proof; retained automatic-shaped source checkout measured `296,476,091` bytes at `/home/user/work/wt/app-m2-auto-r36-approved-registered-one-actual-r37`. |
| Agent checkout | `/home/user/work/wt/agt-pin-6efc8150` | `110,115,866` | Reuse read-only. |
| Runtime checkout | `/home/user/work/wt/rt-pin-95bd3c5f` | `8,498,820` | Reuse read-only. |
| Private C13 dependency graph | `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules` | `462,723,229` | Reuse only after main verifies its READY/LEASE, exact package versions, archive bytes, and symlink-free condition. Count once for both serial proofs. |
| Agent venv | `/home/user/work/venv-agent` | `599,954,879` | Reuse as `ASTRID_PYTHON=/home/user/work/venv-agent/bin/python`; dependencies-only and read-only. |
| Runtime venv | `/home/user/work/venv-runtime` | `30,200,613` | Reuse as `ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python`; dependencies-only and read-only. |
| Automatic runner physical copy | Vite and Rollup under the private overlay | `15,946,122` | Measured source sizes: `vite` `13,111,496` plus `rollup` `2,834,626`. The runner copies only these packages physically and links the rest; count once for the active automatic proof. |

The existing shared App install at
`/home/user/work/app/node_modules` measured `427,248,646` bytes, but it is a
shared read-only install and is not an approved private proof graph. It is not
counted as a replacement for the C13 graph and must not be written through.

No wheelhouse was found under `/home/user/work` or `/tmp` in the read-only
search. No wheelhouse is needed or budgeted: the two installed venvs above are
the exact reusable Python dependency stores named by the approved packets.

## Node and Chromium

The approved packets require Node `v20.19.4` at the main-owned `NODE` path.
This worker found only `/opt/node20`, which reports `v20.20.0`; its executable
is `97,661,912` bytes and its installation directory is `160,613,507` bytes.
That installation is not an acceptable substitute, so it is not included in
the approved baseline and the source guard must not be relaxed. Main must use
an already-installed exact `v20.19.4` executable and verify its size before
admission. No Node install or copy was performed here.

The required Chromium is reusable from the existing installation:

- executable: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`;
- executable size: `463,227,992` bytes;
- complete Chromium directory size: `624,734,779` bytes;
- executable SHA-256: `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`.

Chromium is preinstalled outside the private run roots and is therefore not an
additional proof copy. Private browser profile and artifact paths remain part
of the transient allowance.

## Per-run transient evidence and limits

The runner sources show the actual transient shape:

- automatic1490 creates a private run root/TMPDIR and private npm, Playwright,
  Vite, XDG, HOME/profile, and browser-artifact paths;
- it temporarily replaces the App `node_modules` symlink with a private overlay,
  then restores the shared symlink in `finally`;
- publicTrim0cc likewise requires private physical run/cache/profile/evidence
  roots and forbids a direct-dist bypass, so its normal setup may build the
  hosted bundle.

Retained evidence gives useful lower bounds but not a peak bound:

| Retained record | Measurement/evidence | What it proves |
| --- | --- | --- |
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public-trim-approved-one-real-r15/log.txt` | Normal global setup reported `built in 1m`; one retained chunk was `2,877.71 kB` with an `11,862.14 kB` source map. | A hosted build is a real transient phase; the complete `dist` size was not retained. |
| Same r15 record | Worker-owned TMP/browser scratch was reported as `1.1 MB` and removed after evidence retention. | A small scratch lower bound only; not a peak measurement. |
| `/tmp/tl-public-trim-reviewed-r26-49eb3f61` | `1,891,724` bytes after cleanup. | Historical private scratch shape only; it is not an approved proof result and is not a peak. |
| Retained overlay record named in prior notes | `8,967,224` bytes for an older thin test overlay. | Historical overlay reference only; the current automatic runner's measured Vite/Rollup copy is the `15,946,122`-byte figure above. |
| Retained automatic/public run roots | The older roots were cleaned or are absent. | No recoverable peak for realm files, build output, browser profile, caches, or failure artifacts. |

Accordingly, the following individual peaks are explicitly **UNKNOWN** from
retained records: complete hosted `dist`, Runtime realm/support data,
Playwright profile/browser artifacts, npm/Vite/XDG caches, and the full
automatic/public transient root. The storage envelope reserves `2 GiB` for
their combined peak and adds a separate `2 GiB` margin; the calculation does
not claim those bytes were observed.

## Arithmetic and serial policy

Known one-slot baseline:

```text
App source slot                 297,177,147
Agent checkout                  110,115,866
Runtime checkout                  8,498,820
private C13 graph              462,723,229
Agent + Runtime venvs           630,155,492
automatic Vite/Rollup overlay    15,946,122
                               -------------
known baseline                1,524,616,676  (1.420 GiB)
unknown transient allowance  2,147,483,648  (2.000 GiB)
required safety margin        2,147,483,648  (2.000 GiB)
                               -------------
planning envelope             5,819,583,972  (5.420 GiB)
```

The graph, Agent checkout, Runtime checkout, venvs, and Chromium are shared
across the two proofs and are charged once. The App source slot and proof-local
overlay are the only proof-specific items in this calculation. Run
`automatic1490` and `publicTrim0cc` serially; release the first App source and
its transient root before materializing the second. If main intentionally keeps
both source slots, use the documented `6,116,761,119`-byte (`5.697 GiB`)
envelope instead.

Do not lower the approved source tuple, archive/member, private-graph,
Node-version, path-ownership, or existing free-space guards. This document
does not authorize a new wrapper, a new graph, a dependency install, or an
exception to the global refusal floor. The source tree also contains an
independent 10 GiB standing free-space assertion for the viewing-parity lane;
that assertion was not changed or treated as waived here.

## Measurement commands and evidence

Read-only commands used:

```text
du -sb /home/user/work/wt/app-m4-main-proof-measured-footprint-r44
du -sb /home/user/work/wt/agt-pin-6efc8150 /home/user/work/wt/rt-pin-95bd3c5f
du -sb /home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules
du -sb /home/user/work/venv-agent /home/user/work/venv-runtime
du -sb /opt/pw-browsers/chromium-1194 /opt/pw-browsers/chromium-1194/chrome-linux/chrome
/opt/node20/bin/node --version; stat -c '%n %s bytes' /opt/node20/bin/node
sha256sum vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz
tar -tzf vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz | awk 'NF && $0 !~ /\/$/ {n++} END {print n}'
find /home/user/work /tmp -maxdepth 3 -iname '*wheelhouse*' -print
```

No source, shared dependency, venv, browser, or cache path was modified by
these measurements.
