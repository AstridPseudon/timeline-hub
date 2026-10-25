# D117 independent review of D77 footprint bound

Review date: 2026-10-25 UTC
Result: **PASS**
Scope: read-only review of `rt-F-D77-footprint-bound-0947`, retained D77 stage evidence, and source trees. No test body, stage, install, acquisition, render, or probe was run.

## Finding

The prior D77 footprint assessment is arithmetically correct and makes the required safety distinction. The retained ordinary `Installer.run("install", manifest)` record reached `Backend.stage`, stopped at the first pinned OMP source transfer with HTTP 403, and reported a staging-root size of `1,168,669,468` bytes before temporary cleanup. The retained record does not establish a successful installed candidate or a render.

The requested `750,000,000`-byte bound is exceeded:

```text
1,168,669,468 - 750,000,000 = 418,669,468
1,168,669,468 / 750,000,000 = 1.5582259573333333
```

The known-only additive planning figure is also correct:

```text
19,938,578  Runtime retained tree tracked bytes
169,901,555 VibeComfy retained tree tracked bytes
-------------
189,840,133 known source sum

1,168,669,468 + 189,840,133 = 1,358,509,601
```

This additive figure is deliberately not a measured peak and does not claim that the source trees were simultaneously additional to the reported staging root.

## Exact-source review

- Retained Runtime tree `a522511414947e48e317a5e5c2103483b121a750` was independently remeasured from the available Git object: 528 tracked blobs, 19,938,578 apparent bytes.
- Retained VibeComfy tree `101744f0d87eebe5ddf6752c10f01f52dc94e3e9`, 3,857 tracked blobs and 169,901,555 apparent bytes, agrees with the retained D117 evidence. That exact object is not available in the current source repositories, so this value is retained evidence rather than a new local checkout measurement.
- Retained applied Agent tree `523893dcf54dbe756db8fe2915d14055b1da660b` remains the exact identity for the run, but its complete tracked-byte size is unavailable. The current `tl/integration` Agent tree is `68df11fad2b082fa12d99ca20404e1e40e350cd7` and is not substituted for it. The current installer route source hashes match the prior source-only inventory; this verifies route text, not the missing complete applied-tree size.
- Current Runtime `tl/integration` is `d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e` / tree `6283b5fbb128447f1b333e0e6af334d35637cf69`; it is not substituted for the retained applied Runtime tree.

The current Agent source still shows the production route `Installer.run` → `Backend.stage` → `install_tools` → `_install_omp_source` → `fetch_archive`. No source or product file was changed by this review.

## What remains unknown

The retained byte report does not identify apparent-size versus allocated-block semantics and does not retain a phase or peak sample. Exact sizing remains unresolved for:

- the applied Agent tree;
- source archive and extraction duplication;
- uv/wheel/build temporaries;
- the venv and locked dependency closure;
- Bun, Node, ffmpeg, OMP source/native materialization and other tool roots;
- Remotion `node_modules`;
- cache, hardlink, and shared-dependency allocation/provenance;
- later profile, service, and render phases, which were not reached.

Therefore no complete finite run-specific peak bound is proved by D77. The existing D89 heavy admission predicate (`free_bytes > 5,200,000,000`) remains an admission gate only; it must not be reported as a measured or proved D77 peak. At that gate, the arithmetic headroom over the known-only planning figure is:

```text
5,200,000,000 - 1,358,509,601 = 3,841,490,399
5,200,000,001 - 1,358,509,601 = 3,841,490,400
```

Those numbers are not safety margin against the unknown components. The `5,000,000,000` start-source floor, `4,500,000,000` stop floor, and fixed 8 GiB bench-store reserve/no-init remain unchanged. No reserve reduction, bench initialization, or new resource rule is justified.

## Minimal future-run correction

Before any owner-authorized actual run, require a supplied exact pinned OMP source/artifact with permission and hash, verify the exact Agent/Runtime/VibeComfy identities, and use a private staging root without borrowed environments, caches, node modules, runtimes, or bench-store contents. Admit only through the existing D89 gate and preserved floors. Record both apparent bytes and allocated blocks before the run and at source/archive, wheel/uv, venv/dependencies, tools/OMP, Remotion, and final-root phases; retain the maximum and headroom. Stop on any identity, provenance, source-permission, free-space, or bound failure.

The actual HTTP 403 and classifier refusal remain STOPPED. No retry, probe, alternate source, mirror, near-match, cache bypass, stage, install, render, or related operation was performed for this review.

## Contract and scope guard

The review read `contract/commit-v2.md` in full, including the request/reply examples required by C0: the `commitTimeline` request fields, `Idempotency-Key`, accepted/merged canonical result and receipt, conflict head/reason, invalid code/path/hint, and dry-run form. No contract shape or guard was changed. The production path remains the mounted `commitTimeline` → registered Agent provider → `RequestCommitPort` → authenticated store path; this footprint review has no authority to alter it.

No product tests, typecheck, lint, body, or full suite was run; they are not evidence for this read-only assessment.
