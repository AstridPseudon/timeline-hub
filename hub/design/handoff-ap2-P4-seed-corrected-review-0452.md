# Handoff — P4 corrected seed review

PASS for source and offline schema readiness at `5108aaf1438b52be17d5346e04f3dcb590a892b7`.

- Reviewed against `246f92507f15ac16c3bb559b7ce1576a608c86d8`.
- Only `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` changed;
  all outside-file blobs match reviewed `246f`.
- The seed compiles the untouched `tests.sdk.test_timeline_sync.initial_bundle`
  through the normal `compile_authoring_candidate` constructor and adds only
  Runtime’s required empty `registry` wrapper. The normal Runtime
  canonical-document → Agent bundle boundary removes derived `occurrences`.
- Offline checks prove exact authored config/clip order, Unicode `café`, empty
  media manifest, empty Runtime registry, Agent `_verify_document`, and the
  full-parent equality boundary. Existing CLI/native-sheet/request/reply/
  show/history assertions were preserved.
- Exact Runtime checkout `34eac004` schema validation: 49 passed; PreparedCommit
  schema confirms the required registry path. Schema digest matches current
  Runtime.
- Exact integration node collection: 1 test collected. Ruff, private mypy,
  and diff check pass. Source worktree clean.

Live HTTP/socket body was intentionally not run. It remains unverified until
the manager performs the one permitted retry of the existing failed node:

```text
ap2-P4-staged-path-review-0442-p4-v2-http-nodes-1023044414-16765
```

No full suite, browser, HTTP-body, acceptance, merge, or stale-proof-ancestry
claim is made here.
