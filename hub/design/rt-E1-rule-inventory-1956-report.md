## E1 report

- Wrote the paired Runtime/Agent inventory: [E1-rule-inventory.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-E1-rule-inventory-1956/evidence/E1-rule-inventory.md).
- Covered 16 core rule groups, actual production callers, ownership boundaries, existing tests, source hashes, proposed shared-spec grouping, migration constraints, and proving gate.
- Recorded heads:
  - Runtime: `44917baf5976d6a655d582fafc63fde7b6cb242d`
  - Agent: `22d00393f7d944f1d01505637ca00b1995c3e158`
- Recorded the four published divergences: recorder ABI, inverse timeline root, popup physical observation/owner, and private-cache isolation.
- Current source contains the narrow popup projection fix; current behavioral parity remains UNKNOWN.

Source-only checks passed:

```text
git ... rev-parse HEAD
git ... diff --exit-code
git ... diff --check
test -f + sha256sum for all cited production files
rg symbol/path verification
```

No tests, lint, typecheck, browser, daemon, benchmark, or full suite was run; this is justified as a docs-only E1 task. No blockers. Commit message written to the required path and `DONE` marker created.

Recommended next step: Sol should use this grouping as input for the post-ZIP HARD design and add conformance canaries for the four proven seams.