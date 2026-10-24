# P1 report — actual18792 custody

**Result: ACTUAL CUSTODY PASS — P1 RESULT GO.**

- Producer packet present: 2,777 bytes; SHA-256 `60d3f302bc0fe2cc30037305396966e08d18c160b3ba709d87e429871044e789`.
- Retained run: `app-P1-reviewed-leaves-caller-sol-0013-ap2-P1-chain-h6-1024002459-18792`; exit `0`, duration `141s`, Playwright `2 passed`, selectors `1393` and `1561` passed.
- App/Agent/Runtime commit and tree identities match the packet locally.
- Field-consistency checks passed for selectors, counts, pins, bench lease, legacy-route result, and declared scope limits.
- App worktree clean; `git diff --check` passed.
- No source, test, product, configuration, or tracked documentation changes made.

Commands/results:

- `git status --short --branch` — clean.
- `git diff --check` — exit 0.
- `sha256sum`/`wc -c` on producer packet — expected size/hash.
- Local `git cat-file` and `git rev-parse <commit>^{tree}` identity checks — App, Agent, Runtime matched.
- Read-only field checklist — all checks passed.

Limits retained honestly: no raw summary/log byte hashes, fresh direct raw-log/receipt/private-trace audit, or complete exported wire JSON. Optional unasserted fields remain out of scope; success-only absence of failure artifacts is reported as `NOTCREATED`.

No rerun was performed. Commit message written to the required path; `DONE` marker created.