# D141jj validation

## Static checks performed

- `PYTHONDONTWRITEBYTECODE=1 python3 - <source-root> ...` parsed `check_jj.py` and all candidate Python files with `ast.parse`, parsed the scoped JSON inputs, and checked all 11 manifest hashes and modes — **exit 0**: `PASS static AST/JSON and immutable 11-file source-manifest hash+mode check`.
- `sha256sum`/`stat` on all 11 candidate files — **PASS**, matching the immutable original manifest. Original manifest SHA256: `7c3fa7c10dd4afb7e01f6af32aaf28ffb94a16c81730095d36bc514683b27852`.
- Read-only `git rev-parse HEAD`, `origin/main`, `tl/integration`, and `git status --porcelain` for all four integration worktrees — **PASS**; heads remain the authorized tuple and statuses are clean.
- `rg`/`nl` source tracing — **PASS**; evidence is recorded in `source-map.json` and `purpose-map.json`.

One initial static command used the wrong path for `install-map.json` and exited 1 with `FileNotFoundError`; it was immediately corrected and rerun successfully. No product or fixture command was run as a consequence.

## Explicitly not run

No `check_jj.py`, `check.sh`, D68 staging, builder, installer, service, browser, socket, full suite, source authoring, canonical install, product import, or packaging command was run. The prior actual positive and same33 PASS remain historical retained evidence and were not duplicated.

## Contract observations

The C0 v2 request/reply fields and closure remain normative and untouched. Packaging is not treated as a commit wire request. The stale control must observe the current caller's nonzero code plus FAIL diagnostic receipt rather than demand a Python exception and absent receipt.
