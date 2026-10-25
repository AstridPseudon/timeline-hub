## D100 resume report

Prepared READY source/preflight packet for exact NEW26 only:

- 26 selectors: 4 exact-time, 22 shared-item.
- Rebound Agent: `dd2fc40d…`, tree `757e848d…`.
- Released Runtime: `1daca2a…`, tree `a5225114…`.
- Genuine old baseline: Agent `6aefd117…`, tree `6f6aee59…`.
- Corrected test bytes enforced identically in old-RED/new-GREEN; stale `c485…` fixture excluded.
- Original TEN, P4, observer, prior-passed neighbors, and full-body repeat excluded.
- No product, test, schema, pin, registry, CAS, checkout mutation, or body execution.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D100-new26-resume-0901/evidence` (36 KB).

Checks passed:

```text
bash -n evidence/route/d100-new26-route.sh
selector count: 26
AST/hash verification: 4 reviewed blobs PASS
Runtime receipt/head verification: PASS
git diff --check
```

Remaining ordinary input: no current immutable Agent checkout receipt for `dd2fc40d…` was available; source was verified directly from real Agent Git. Runtime receipt is present. App/Composition SHAs must be captured once at eventual submit.

Critical D112/0850 and D111b/0858 stages are active, so no central request was submitted. Next request is one existing-D73 old-RED run followed serially by one NEW26 green run after both release the >5.2 GB main-heavy slot.

`DONE` and commit message are present.