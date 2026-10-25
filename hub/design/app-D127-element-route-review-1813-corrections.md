# D127 finite corrections

Result: `FAIL`. The route and selector source are valid, but the published recipe is not source-ready for a protected normal submission.

1. Runtime provenance/path: use the already qualified App Runtime lock tuple `ab1e4f6141987706132916e2da16477f5a019464` / `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657` at `/home/user/work/wt/rt-pin-ab1e4f61`. The recipe's e319 tuple is not the App's qualified `runtime.lock` source, and `/home/user/work/wt/rt-pin-e319fdbd` is not the source-derived path (`e319fdbc`).

2. Helper custody: restore/access the previously reviewed external regular non-symlink helper with SHA-256 `4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e`; pass its absolute path and hash explicitly. The 4ee copy is not currently present in custody, and the qualified ab1e checkout's helper is `6c9daef2...`, so do not silently substitute it or use mutable `/home/user/work/runtime`.

3. Detached admission: retain real receipts and App target metadata for App d5a1d1ab, Agent 070dfc5e, Runtime ab1e4f61, and Composition 635f4de0. Agent, Runtime-ab1e and Composition receipts are present; App d5a1d1ab receipt/target metadata is missing. No body before all four D66 receipt checks pass.

4. Submit handoff: publish the exact corrected one-command controller call ending in `d66-plain-stack.mjs p2-element --submit`, including fixed private output and submit-plan paths. The current text supplies only the service row and says a later controller must submit, so the normal caller/provenance flow is not reproducible from the recipe.

5. Documentation: unescape the published Markdown fences.

Non-blocking source findings: `p2-element` intentionally selects watchdog 2 seconds while full `p2` selects 20; the source test and bootstrap forwarding support this. The existing selector count is one, its native lifecycle/5-second expect timeout, v2 request oracle, canonical/history/reload/guarded inverse checks, and legacy-route guard are unchanged. The retained bootstrap is source-only with raw capture absent; historical request 3 remains pending and its wall denominator is UNKNOWN.
