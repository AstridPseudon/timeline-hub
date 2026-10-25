# D117 D77 footprint assessment

Assessment date: 2026-10-25 UTC  
Scope: source-only planning for one future owner-authorized private stage

## Result

The retained ordinary run reported `1,168,669,468` bytes in its private
staging root before automatic temporary-tree cleanup. That is `418,669,468`
bytes above the requested `750,000,000`-byte bound (1.5582259573 times the
bound). The 750 MB bound is therefore not safe and is not a usable admission
cap.

The only honest finite admission requirement available before a later stage is
the unchanged D89 heavy gate: free space must be strictly greater than
`5,200,000,000` bytes before admission, with the existing `5,000,000,000`
start-source floor, `4,500,000,000` stop floor, and fixed 8 GiB bench-store
reserve/no-init unchanged. The strict integer minimum is `5,200,000,001`
free bytes. This is an admission budget, not a claim that the stage peak is
5.2 GB.

## What the arithmetic proves

The retained record does not identify whether its reported bytes were apparent
bytes or allocated blocks, and it does not retain a peak sample. The exact
applied Agent tree's source size is also unavailable in the read-only source
objects, so it is not replaced with a current or near-match checkout.

Two exact retained source trees can be measured from their Git trees:

| component | exact tree | tracked apparent bytes |
| --- | --- | ---: |
| Runtime | `a522511414947e48e317a5e5c2103483b121a750` | 19,938,578 |
| VibeComfy | `101744f0d87eebe5ddf6752c10f01f52dc94e3e9` | 169,901,555 |
| Agent | `523893dcf54dbe756db8fe2915d14055b1da660b` | unknown |

Known-source sum: `19,938,578 + 169,901,555 = 189,840,133` bytes. Adding
that sum to the retained reported value, without assuming overlap, gives a
known-only additive planning figure of `1,358,509,601` bytes. At the existing
5.2 GB floor this leaves `3,841,490,399` bytes above that known-only figure
(`3,841,490,400` at the strict integer minimum).

This is deliberately not presented as a complete peak bound. It is a
conservative planning addition around the one retained measurement. A complete
finite bound remains unknown because the following are unmeasured: source
archive/extraction duplication, the exact applied Agent source, uv/wheel build
temporaries, the venv and locked dependency closure, Bun/Node/ffmpeg/tool and
OMP source/native materialization, Remotion `node_modules`, cache/hardlink
sharing, and any later phase. No cache or shared dependency has valid
provenance for credit.

The existing source shows the normal path creates three source trees, a Python
environment, hash-locked dependencies, tool roots, OMP source/native
materialization, and Remotion dependencies through
`Installer.run → Backend.stage → install_tools`; it does not supply size
bounds for those operations. The actual pinned OMP fetch reached HTTP 403 and
remains stopped. Classifier refusal also remains stopped. No retry, probe,
alternate source, cache reuse, stage, install, build, profile, carrier,
render, package fetch, benchmark, deletion, livekit change, or registry change
was performed for D117.

## Proposed private-run preflight

For any future owner-authorized actual run:

1. Require already supplied exact pinned source/artifact permission and verify
   the applied Agent/Runtime/VibeComfy identities and hashes. Do not retry or
   probe the denied source, substitute a mirror/near-match, or reuse an
   unproven cache artifact.
2. Use a private staging root on the intended filesystem. Do not borrow shared
   venvs, node_modules, runtimes, caches, or bench-store contents.
3. Require the existing heavy admission result with no live heavy slot and
   `free_bytes > 5,200,000,000`; preserve all existing floors and the fixed
   8 GiB reserve/no-init.
4. Record pre-run free bytes plus both apparent-size and allocated-block
   measurements for the private root. During the authorized run, retain phase
   measurements for source/archive, uv/wheel, venv/dependencies, tools/OMP,
   Remotion, and the final root so a real peak can be established.
5. Stop on unreadable/invalid free-space data, identity or provenance gaps,
   missing source permission, or any bound violation. Do not delete shared
   state as a workaround.

Until that measurement exists, the run-specific recommendation is the honest
larger `>5.2 GB` per-run free-space budget plus cleanup of unrelated private
temporary state before admission; it is not a reduction of the global floor.
The actual rerun remains source-permission-held and STOPPED.

Inputs and arithmetic receipt: `workers/rt-F-D77-footprint-bound-0947/evidence/`.
