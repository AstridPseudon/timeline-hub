# D77 independent input/footprint review

## Verdict: PASS

The permanent D77-2218 evidence is internally correct as a `NOT_READY`
handback. The reviewed result is not a Farm-ready input bundle and does not
claim to be one. No finding authorizes a run or changes the settled plan.

## Findings

1. **Tuple custody is correctly separated.** D139 is Agent
   `4c4ee35d5687c4cd40a0e5395efda53aa56f939d` / tree
   `d50fd98f7d1bc6860de810f38e8a0b3a55ca224e` plus Runtime
   `ab1e4f6141987706132916e2da16477f5a019464` / tree
   `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`. The older Agent
   `91398e9d...` / Runtime `1daca2a...` tuple resolves to distinct historical
   trees and is not reused as current qualification. The Remotion lock is the
   exact `...18d` value; the `...18e` near-match remains rejected.

2. **Arithmetic is reproduced, but it is not a bound.**

   `1,168,669,468 + 19,938,578 + 169,901,555 = 1,358,509,601`.

   Adding the exact OMP archive only as a non-overlap planning case gives
   `1,524,776,481`. The OMP archive may overlap the retained observation, and
   Agent materialization, allocated bytes, build/cache/temp, backup, browser,
   render input/output, and cleanup timing are not bounded. The prior
   `1,623,728,128` OMP-phase observation is a lower bound, not a complete peak.
   Therefore the honest status remains `UNKNOWN_UNBOUNDED`.

3. **The overlap model is conservative and complete enough to refuse a
   guessed bound.** The handback identifies archive/unpack, UV/wheel/venv,
   Bun/OMP native, Remotion `npm ci`/node_modules, backup, and preflight/render
   overlap. It names the exact missing maxima and their Farm/installer owners.
   D89's 5.2 GB admission floor and the 4.6 GB/4.0 GB operational floors are
   admission/stop rules only; none is a footprint limit.

4. **Required input coverage is present and the missing state is accurate.**
   The handback covers 24 required-input rows and a 10-step ordered gate. Farm
   inventory says no installed `ASTRID_RUN`, no authenticated
   `INSTALL_MANIFEST`, no browser matching `85918a99...`, no private
   PROGRAM/DATA/RUN/RESULT root receipts, no current installed profile or
   seven-key carrier, and no complete stage/preflight/render receipts. UV and
   ffmpeg/ffprobe remain unverified. These are blocking, not inferred from
   an imagined carrier or old checkout.

5. **The ordinary source path is correctly traced.** Static inspection of the
   D139 Agent source confirms `run-astrid` → `cli.main` → manifest validation →
   `Installer.run` → `Backend.stage`; stage materializes Agent/Runtime/VibeComfy,
   creates the pinned UV environment, installs locked Python dependencies,
   invokes `install_tools`, runs frozen Node `npm ci --no-audit --no-fund`, and
   writes service/profile/version metadata. The D13 consumer source names
   `test_d13_installed_native_preflight` and
   `test_daemon_backed_host_executes_authoring_and_final_render`. No installed
   output exists, so the trace is source evidence only. The generated stage
   profile carries fields beyond the D13 selector's exact four-key input shape;
   this compatibility remains an open seam to reconcile during a future
   authorized qualification, not evidence of a passing profile.

6. **Guard evidence is correctly scoped.** Sol1243 is the author; Luna1257's
   independent receipt is the PASS/18-control review, and the custody receipt
   is source-only. This proves wrapper custody and controls, not live stage,
   installed tools, browser, or render. The retained normal stage stopped at
   the pinned OMP archive with HTTP 403; no retry, alternate source, or
   permission bypass is credited.

7. **Redaction holds.** The reviewed JSON/Markdown contain no credentials,
   private paths, private identifiers, raw payloads, or raw URL/traceback. Safe
   public hashes, role names, and status are retained.

## Disposition

`PASS` means the permanent evidence review passed. The operational disposition
remains `NOT_READY`, with `UNKNOWN_UNBOUNDED` peak footprint. The next step is
an owner-authorized, normal-path completion of current-D139 custody and
authenticated installed receipts plus a measured finite phase bound. Do not
start piecemeal staging, fetch a replacement, reuse the old tuple, claim a
staged-render credit, or perform D130 qualification.
