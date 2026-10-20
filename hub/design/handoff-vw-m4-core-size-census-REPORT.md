# Viewing size census handoff

Authoritative repo file: `/home/user/work/wt/vw-m4-core-size-census/design/viewing-size-census.md`

Added the read-only manifest/count script at
`/home/user/work/wt/vw-m4-core-size-census/scripts/viewing-size-census.mjs`.
It measures committed blobs at the actual Agent/App/Composition `origin/main`
and `tl/integration` SHAs, with authored bytes and nonblank lines separate from
generated schemas/registries, tests, vendor duplicates, and package archives.

Canonical Viewing slice: main 143 files / 2,036,935 bytes / 46,000 lines;
current 208 files / 2,208,967 bytes / 49,161 lines; delta +65 files /
172,032 bytes / 3,161 lines. This does not claim the 20–26k target: D08, D09,
VW-AUDIO-STEP/App D08b, and D10 remain open or held as stated in the repo file.

Validation:

```text
node --check scripts/viewing-size-census.mjs                         PASS
node scripts/viewing-size-census.mjs --json                         PASS
repeat command + cmp JSON outputs                                    PASS
git diff --check                                                     PASS
```

No product code, tests, dependencies, shared graph, browser, socket, install,
network, or full suite was touched or run.
