**FULLFINAL READY — caller controls passed; journey GO remains unverified.**

Updated only the existing P2/P3 rows in shared `tests/suites.conf`, using fresh-read atomic replacement. App worktree remains clean.

Both rows bind:

- Source: `804134d74782d40855146aa568ff289200b79142`
- Tree: `8437e47666853b62e03a58af3716235346316fba`
- Actual parents: `22efcda3da4005f8663c078439ff0edbfade69be` and `42db156ede0d0192ec4176a2edd29b366b552a8d`

Rebound file guards through actual Git reads, including hook `e79e083d…`, handoff `551f2fa7…`, producer test `e2fa3c3a…`, current readiness controls, and P1 spec/cases. Preserved pinned dependencies, original bodies/final tails, native/history assertions, selectors, and exact ephemeral allocation code.

SHA256 values include each row’s newline:

| Projection | SHA256 |
|---|---|
| P2 | `3bfc5116c898fd8faf380175df2e4e7f89a614bf0e9f42b65db75310ac3013bb` |
| P3 | `0667c756b4e009f7fe437fdaaa42831a87e28c4c15cfb23f8571a980b698a4ba` |
| Outside rows | `4e199c21da8b793d0598e6c84d18f2821a1e3864484a2ed5b01706bc681a9756` |

All **245 outside rows / 462225 bytes** remain byte-exact.

Validation commands used `TMPDIR=/tmp/w-8748e38c12`:

- `python "$TMPDIR/prepare.py"` — Git bindings and outer/inner `bash -n` passed.
- `python "$TMPDIR/qualify.py"` — **24 controls passed**, including actual source and real-Git single-parent/same-tree snapshot positives.
- `python "$TMPDIR/stages.py"` — **28 controls passed**: exports, ordering, failure closure, consistent mocked port, invalid allocations.
- `python "$TMPDIR/extra.py"` — **4 controls passed**: hook and graph-byte corruption refused before stages.
- `python "$TMPDIR/install.py"` — atomic replacement, outside-byte equality, final Bash syntax passed.
- `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — passed.
- `git diff --check` — passed.

Controls read real source, receipts, import origins and all 80 graph-file bytes. Diagnostics used private scratch; snapshot mounting and live stages were intercepted.

**NOT RUN:** build/setup/native/list/browser/backend/HTTP/journey/service/provision/dispatcher/full body or real network allocation. The initially pending integrated0046 report is now present and reports PASS; I did not rerun it. Upstream `f38e` remains HOLD.

Proof/App may use the existing API for the authorized run:

```bash
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
"$O/bin/request-test" app-P2-P3-fixed-source-caller-sol-0053 full-e2e-three-products
"$O/bin/request-test" app-P2-P3-fixed-source-caller-sol-0053 ap2-P3-gate5-h6-0348
```

Follow each returned `wait-test` command. No requests were submitted here. No implementation blocker; commit message and `DONE` written.