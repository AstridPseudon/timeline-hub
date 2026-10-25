# D108 report — FAIL (App), PASS (Composition source accounting)

- Reconstructed both applied trees from fresh upstream plus recorded patches.
- Exact tree matches:
  - App: `204a9216697953f765b5bd550aefa5822503a44c`
  - Composition: `5ab5191a296980a0a6bcd1178ab6902d6478a148`
- App: 14,733 upstream predicates, 15,993 applied; 62 intentional deletions mapped to U3b/D52 decisions.
- Composition: 2 upstream predicates mapped to ledger replacements; 74 applied predicates; no changed upstream predicates.
- Verified `WelcomeConnection.sameOrigin`, `WelcomeJourney.integration`, and incoming/local WelcomeConnection predicates.
- Remaining App gaps:
  1. Project-scoped revision test rewritten to refusal while D01 remains OPEN.
  2. Three timeline label/signature predicates lack an exact approval mapping.

Evidence:

- `evidence/d108_ts_source_audit.py`
- `evidence/d108-ts-audit.json`
- `evidence/d108-ts-audit-summary.md`

Checks:

```text
python3 ast.parse audit script — AST_SYNTAX_OK_FINAL
source audit — App tree_match=true; Composition tree_match=true
```

No product tests, TypeScript checks, lint, browser, provider, build, install, or live-service commands were run.

Commit message written and `DONE` marker created.