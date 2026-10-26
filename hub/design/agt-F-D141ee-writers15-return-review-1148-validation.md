# Validation

All commands were read-only source/evidence checks. No product or test suite
was executed.

| Command | Result |
|---|---|
| `git status --short` | PASS: empty |
| `git rev-parse HEAD` / `git rev-parse HEAD^{tree}` | PASS: `445b9c1a7f8d0e7e3405ad01f4475b9af02acfaf` / `6806fec5657f26097d0d0f3da29082907e6faadd` |
| `git diff --exit-code --quiet` | PASS: repository unchanged |
| `git cat-file -e` for all seven original test blobs | PASS: every blob present |
| Python `ast.parse` over the seven protected test files | PASS: all original and proposed selector functions found; spans recorded in `source-manifest.json` |
| Exact-ID manifest check | PASS: 15 assigned, 15 unique, IDs 4–18, no omissions or duplicates |
| `sha256sum` over seven protected test files | PASS: hashes recorded in `source-manifest.json` |
| Python AST/source trace for `_PublishMixin`, WorkspaceClient, RemoteTimelines and Runtime methods | PASS: all named methods and spans recorded; call literals confirm `session.submit/flush` and Runtime refusal |
| `python3 -m json.tool evidence/review.json` | PASS |
| `python3 -m json.tool evidence/source-manifest.json` | PASS |

The Runtime source was read from `/home/user/work/runtime` at commit
`95d98f038320d5d46bd679ac000ab3e15825c935`, tree
`78df31d62c5b9ba4c84dee4ea346e43a767718c1`.

Not run by instruction: pytest/collection, typecheck, lint, Vitest, browser,
render, install, profile/dependency, live request/CAS/registry/body, child,
full suite, or behavior verification. Existing retained XML/hash/count evidence
was not rerun or republished.
