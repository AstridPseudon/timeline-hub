# Validation

Read-only review only; no product test, browser, service, or body rerun.

- `sed -n '1,260p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md` — read governing plan.
- Read every file under the author evidence root — complete.
- `sha256sum` accepted prep packet — `bdf548ac4498d08dd38f2b7eb0664f7a862c4ad109a39fd48d91db46062f194e`.
- `sha256sum` author packet — `e6b63540d9f8c57643ab184a5306f9742e3a72892f55f84ef05079c1aa07fd85`.
- `diff -u <(jq -S . accepted) <(jq -S . author)` — only private future path values differ.
- Original Sol recipe dispatch 2 SHA-256 — `d665c4907abd063edc9da0f29c887b56f7b66fb80febbe52f14732ea66e95d0d`.
- `wait-test app-pin-82e9e13d-full-d141-p2-transition-none-single-82e9e13d-submit-single-scope-2-1026114726-24271` — cached same-ID PASS, exit 0.
- Authenticated result checks — request, snap, status, exit, summary, d66 manifest, readiness XML, body XML, trace validation, and plan IDs match the packet.
- `sha256sum /home/user/work/wt/app-pin-82e9e13d/tests/e2e/local/three-products.p2-tour.spec.ts` — `83948c53c7990824fce81be7f0db2b4f947837c66a827abf2ffb08492f09bee4`, matching before/after manifest hashes.
- `git -C <each pinned checkout> status --short --branch` — all four clean; detached pin identities match.
- Builder SHA/Git blob checks — `2032f308...7602f` / `59b65214...480a93`, matching packet and manifest.
- Native TSV arithmetic — 54 samples, min `5029826560`, max `5477560320`, max gap `5.006048s`, stop false.
- Author trace arithmetic — 158 `/dev/vda` rows, min `5029302272`, max `5479276544`; session-only.
- Prospective raw KEEP receipt — both IDs had `preexisting_keep: false`; manager added them at `2026-10-26T11:49:29.082850Z`.
- `git diff --check` in this review worktree — run after evidence creation; expected clean.

The earlier wrong-SHA attempt is retained as distinct `FAIL_CUSTODY` / `NOTRUN`; it has no request, row, artifact, body, or test verdict and was not retargeted.
