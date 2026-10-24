## PASS — P2 parent-history reads review

Reviewed exact commit `6b7b6e7a4025e9a1d553a0c1063d758205cba0b6` over parent `1540b3f12ebde61c56a19be9089af2b2f2917e6c`.

The change correctly enforces:

- Submitted request `reads` must be preserved in history by exact deep equality.
- Omitted request `reads` must remain absent.
- Extra/forged reads are rejected.
- Existing command, step, effects, dependencies, receipt, head, canonical-document, reload, undo, and legacy-route checks remain strict.
- No new union, `matchObject`, optionalization, or weakened absence check.

C0 citation: [commit-v2.md](< /home/user/work/runtime/contract/commit-v2.md:717 >) lines 717–985 contain the complete accepted `{data, receipt}` envelope; request-read semantics are lines 112–155, undo is lines 1565–1642, and authenticated history is lines 4609–4695.

Tests passed:

- Parent Node20 control: 7/7.
- Transition Node20 control: 3/3.
- Document Node20/tsx control: 3/3.
- Semantic oracle Vitest using private config override with real project plugins/setup/aliases: 7/7.
- Root, app, node, and fake-runtime TypeScript checks: passed.
- Scoped ESLint: passed.
- `git diff --check`: passed.

Identity and hashes:

- Commit tree: `197c11cd2f7f90be67824148a518ba827ef7fa16`
- Parent tree: `a3b3b97851cacbb1515df36fdb779d42b15dc631`
- `p2-tour.spec.ts` SHA-256: `67662468…c9cd0e0` → `07fe3d84…ed2f3c`
- `p2-parent-oracle.test.mjs` SHA-256: `225a4c43…df47e90` → `98934ece…d1d272`
- Changed helper `assertHistoryMetadata`: `82b78dc1…581304` → `24a5a83e…916474`
- Other protected helpers were unchanged.
- Original parent, transition-single, and transition-bulk case/wait hashes were unchanged:
  `be3db6fe…ba36`, `522c98e2…138c`, `df955842…010f1`.

Worker-authored behavior ledger:

| ID | Behavior | C0 citation | Branch status | Integrated status |
|---|---|---|---|---|
| P2-parent-history-reads | Preserve exact submitted request reads; preserve raw absence when omitted; recorder captures remain separate authenticated history data. | “Store accepted label, steps … requested/effective merge modes and declared request reads…” — C0 §7 | PASS on `6b7b6e7a40`; pending manager merge | Pending integrated/home proof |

No production changes or blockers. Browser, original journey, full, and service suites were not run per task instructions.