# D108 Report — FAIL

Created source-only evidence in:

`/tmp/.../workers/rt-F-D108-python-citations-0700/evidence/`

Outputs:

- `d108_citation_crosswalk.md`
- `d108_citation_crosswalk.json`
- `d108_citation_crosswalk.py`

Findings:

- Manifest SHA verified: `37e559e6…a4504`.
- Source receipts verified: Agent `917/917`, Runtime `311/311`.
- Runtime: all 10 predicates reconciled; 9 reuse exact D69 function-body mappings, 1 uses the approved split-source handoff.
- Agent: raw AST finds 105 selectors; durable audit declares 104, but only 103 are reconstructable. The Windows installer selector remains an unresolved count discrepancy.
- Five viewer selectors clear via `VW-DEAD-INSPECTOR`.
- Three D07 retime/ripple predicates remain restore/approval gaps.
- Changed-assertion signals fully counted: Agent `113 removed/287 added`; Runtime `72 removed/205 added`. No per-assertion map exists, so none were blanket-cleared.
- D107 legacy ten is separately recorded as `SEPARATE_LEGACY_ONLY_GAP`, not PASS.
- Actual fresh Agent 08e6 installer cases are recorded.

Verification:

```text
compile(d108_citation_crosswalk.py): PASS
python d108_citation_crosswalk.py: PASS
```

No product tests, imports, builds, renders, installs, or ledger/source edits were performed.

Commit message written: `docs(D108): reconcile Python citation crosswalk`

`DONE` marker created.