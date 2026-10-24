## Report: FAIL

Reviewed `0cf4dd0768bdd92415e0d64c224cadf050711b66` (tree `9f5418ef3b52f66a984fa46ace9083f20969b143`, parent `50d971541ba3eb50247b2ba611e86367e66cfef1`) against product base `d99396bca7c3853435cfa5a5991f5b1073187be4`.

Source dry guards:

- P2 decoded: PASS, 0.257s; authored record: 0.248s.
- P3 decoded bounded source/Agent/Runtime/tree/target phase: PASS, 0.255s.
- Not run: child, backend, schema, native, build, browser, HTTP, original body.

Prepared tuple:

- App `cca3deb…`, tree `911956…`, parents `d99396… 8a712d…`
- Agent `cba425…`, tree `d19ce2…`, parents `de2d1a… 9746c9…`
- Runtime `becfe6…`, tree `7edc08…`, parents `46eb06… c021f1…`
- P2 decoded/wrapped: `750944…` / `869879…`
- P3 decoded/wrapped: `ff773d…` / `ebf045…`

The App checkout advanced during review to `8f20ec…` (tree `89dc9c…`, parents `cca3d… 0c1e81…`). Candidates are therefore stale; I did not rebind or relabel them.

Findings:

1. `caller-publication.py:125-139,447-448` does not enforce Runtime parents or `tl/integration` refs for App, Agent, or Runtime, despite `caller-custody.json` claiming `normal_refs_authenticated: true`.
2. Installed P2/P3 rows are accepted dynamically. `rebind()` only checks generic markers; it does not pin exact protected row/body/tail digests. `SOURCE_PATHS` is unused, and concurrent registry changes are not detected.
3. Manifest fields such as `legacy_route_traffic: 0` and `registry_mutation: false` are declarations, not execution-backed evidence.
4. App target symlink/path identity is not strictly authenticated: `app_facts()` accepts a symlink path, while dry preflight resolves it.
5. The committed dry helper is P2-specific; P3 required an ad hoc bounded extraction and is not recorded in custody JSON.

Checks:

- `TMPDIR=/tmp/w-9eb993accf python3 caller-publication.py` — PASS, PREPARED/NOT_GRANTED/NOT_RUN.
- Negative matrix — all correctly refused, rc 0: wrong-source, stale, app, agent, runtime, tree, target, body, receipt, registry.
- Normal and `-O` Python compilation — PASS.
- JSON validation — PASS.
- `bash -n` on both decoded and wrapped candidates — PASS.
- `git diff --check` — PASS.
- Static wrapper checks found current tuple bindings, no known stale identities, single `bash -c`, eval suffix, port/export markers, and refusal markers.

No product files were changed. No full/browser/HTTP suite was run. The specified R4 docs directory was unavailable; PLAN, MANAGER-COMMON, contract §4, and BOARD-HEADER D54/D56 were read.

Recommended next steps: freeze the final normal App tuple, fix exact parent/ref/path and registry/body authentication, obtain genuine missing child/client/backend/Remotion/graph/service/full-run custody, then regenerate and rerun both candidates.