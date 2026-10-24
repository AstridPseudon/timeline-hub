## Report — app-F-final-caller-whole-path-1245

No source changes made. Worktree clean; `DONE` and commit message written.

### Concrete contradictions

- Current caller `0cf4dd0` hard-codes App `cca3deb…/911956…`, but `/home/user/work/app` is clean `73aa558…/4d4d4e…`; `python3 caller-publication.py` therefore refuses immediately before row generation. Do not silently relabel this; refresh against the manager-selected final App head.
- `facts()` returns refs but never requires `tl/integration`; Runtime parents are not supplied to `facts()` at preparation. `normal_refs_authenticated: true` in custody JSON is only a declaration.
- `installed_rows()` accepts the live P2/P3 rows dynamically. Recorded row/registry hashes are not compared, duplicate selected rows are not rejected, and the registry is not reread after generation.
- `SOURCE_PATHS` is unused. No exact protected body/tail/native-stage digest is checked. `rebind()` checks only generic markers and broad token replacement.
- Actual dry execution covers P2 decoded source only. P3 is syntax-checked, not dry-executed. Wrapped candidates receive `bash -n` only; no bounded wrapped `bash -c` argument proof is present.
- App symlink identity is not rejected: `caller-dry-preflight.py` resolves the target before checking `is_symlink()`, making that check ineffective.
- Custody JSON claims `legacy_route_traffic: 0`, `registry_mutation: false`, and authenticated refs without execution-backed checks.
- Full run `16138` is recorded as `RUNNING_OR_UNVERIFIED`, but the retained test-service record is terminal `fail`, exit `1`, requested `2026-10-24T12:05:56Z`, snapshot tree `3311baa…`. It predates the current caller and cannot qualify it. No request/snapshot exists for `0cf4dd0`.

### Existing dependencies actually named by the caller

The templates require existing, authenticated child/client/backend/Remotion/graph inputs after the source phase:

- P2 child `venv-agent-child-app-popup-333b-37eb-1016`; P3 child `venv-agent-child-app-ready-079-37eb-0256`.
- Remotion producer remains historical `079…`; it must not be relabeled as current Agent `333b…`.
- Both phases use Agent/Runtime checkouts, child Python/client imports, Runtime backend/environment, and retained output paths. P3 explicitly checks the Composition graph package.
- These are custody prerequisites, not authorization to create a new child or use the stopped schema/child route.

### Smallest reusable prior solution

Reuse the guard mechanics from `47ca6f2` / preflight `1202`, adapted to the final selected source:

1. Exact selected-row hashes, duplicate rejection, outside-registry hash, and a second registry read after generation.
2. Explicit P3 source/tree/parent extraction and per-file blob/SHA guards.
3. Protected body/tail/native-stage preservation checks.
4. Actual bounded dry guards for both P2 and P3, plus `bash -c` positional-argument proof.
5. Keep future service snapshots post-request only; they are not preflight inputs.

### Bounded checks run

- `python3 caller-publication.py` — expected refusal on stale App identity.
- `python3 -m py_compile caller-publication.py caller-dry-preflight.py` — PASS.
- `python3 -m json.tool caller-custody.json` — PASS.
- `git diff --check` — PASS.
- Current registry snapshot matches recorded bytes: 249 lines, 569825 bytes; outside rows 247 / 465609 bytes; P2 row `6a45d056…`; P3 row `1b7c7996…`.
- No full, browser, service, schema, child, backend, or original journey run.