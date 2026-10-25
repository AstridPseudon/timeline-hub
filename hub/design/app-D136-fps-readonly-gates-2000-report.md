## D136 report

- No source files changed; worktree remains at `3082cad490ce1cee764ff137f99cb791a67ddd08`.
- G1: `NOTQUALIFIED` — local `origin/main` is `886a3183...`, and the projection test is absent, but remote tip freshness cannot be established without prohibited fetch/acquisition.
- G2: `STOP_REPORT_REGRESSION_D54A` — pristine upstream schema accepts the nested FPS array via open `ThemeOverrides.visual`; its validator falls back to `30.0`. Receiving Agent rejects arrays and supports exact rational objects only.
- Preserved all nine historical setup errors. No fixture conversion, retry, or source adaptation.
- Census records 43 original predicates, 11 test bodies, and 54 fixture statements with AST conservation; no predicate depends on traversing FPS array shape.
- Evidence written under the requested worker `evidence/` directory, including gates, census, predicate map, source manifest, validation, findings, and proposal.
- Exact test command: none run, per task restriction against pytest/service/socket/browser/full reruns.
- JSON evidence integrity check: all JSON files parsed successfully.
- Commit message written and `DONE` marker created.

Required next step: obtain exact current upstream tip provenance/path readback, then Runtime/Agent owners must resolve the D54a regression before any nine-selector rerun.