# OPS H validation

All checks were read-only against the named input roots and exact Git blobs.

| Command/check | Result |
|---|---|
| Python stdlib `json.loads` / `python3 -m json.tool` on correction and review JSON | PASS |
| Python stdlib SHA-256 comparisons for current author custody files and both raw worker logs | PASS |
| Exact L15 commit, parent, refs, Git blob hashes and cited source coordinates | PASS |
| Python AST parsing of the four cited L15 Python blobs | PASS |
| L15 0.0.13 artifact and sidecar hash comparison | PASS |
| Retained logs `22278`, `16353`, and `23676` hash comparison | PASS |
| L16 worktree separation/status check | PASS; dirty separate WIP, no L15 credit |
| `git diff --check` | PASS |
| `git status --short` | clean; no product changes |
| pytest, renderer, browser, service request, full suite | not run; out of scope |
| typecheck/lint | not run; not applicable to documentary evidence |

## Input hashes

The following are current bytes verified before and after this check. The
author evidence files are explicitly post-review custody files; these hashes
are not claimed to be original author preimages.

| Input | SHA-256 |
|---|---|
| author `evidence/review.json` | `bbb6c75a9a1a338ab68b27c9ebc9d026afb53146b0d9aa8690a6535d972c741b` |
| author `report.md` | `53d3a69d345ab3200561eb33296daaafff0774b0baeb69b90f91ab8b5bcb1e4e` |
| author `evidence/findings.md` | `7ef0b086bc6a2e624d3182dc7a030ae68d1174977fad4274ce6f1570d9db7d83` |
| author `evidence/source-map.json` | `e5b5f003bb820fe6d4bcdb9fceba6cfc0fb18de63e589b1bfad813fbf4ee07e5` |
| author `evidence/validation.md` | `b81453e068567ef25627a293c8235b68b010477634117875727ea4f0bca70d0e` |
| author `evidence/handoff.md` | `54d8775bab0a4268f9858deb5d52340d955ab2eceaa1e8fe7f39e1a9afe852ca` |
| author raw `log.txt` | `da9775c04d0e1b56db4b5111e6d16cfce7c8c3ac4a759faee394bb3ebaa8ff70` |
| reviewer raw `log.txt` | `5bb1940de8dc6f2d8f8e509edbcf7eafc9da78ccf9a8390e45d0ceccc25fb4d2` |

## Output boundary

Only these requested output files were created under the assigned output
root:

- `report.md`
- `evidence/review.json`
- `evidence/findings.md`
- `evidence/validation.md`

No product commit is expected. The validation file intentionally does not
embed its own SHA-256 because that would be circular.
