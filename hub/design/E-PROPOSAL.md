# E-plan: consolidated proposal for the owner (20:25Z, 24 Oct). Implementation happens after the ZIP.

Three designs came back (Codex, design-only, with independent review for E3).

| Row | What | Estimate | Code saved | Risk | My recommendation |
|---|---|---|---|---|---|
| E1 | One shared Python rules module (in Runtime, imported by Agent): 16 duplicated rule groups → 6 pure helpers | 6–10 worker-hours | 4–19 lines net | medium | **DO IT.** The value isn't the lines saved. It ends the Agent/Runtime drift that caused most of today's defects, because one copy of each rule means they cannot disagree. Prove it with the replay corpus (D79) and P1–P5. |
| E2 | Retire the legacy ABI1 format plus a one-time history conversion | ~52 worker-hours | ~23 lines net | **high** | **DON'T, for now.** That's a big cost and real risk to immutable history for almost no simplification. Revisit only if legacy entries cause actual bugs. |
| E3 | Prune custody safeguards | 2–4 worker-hours | 1–5 lines | medium | **Fold it into E1** where E1's proof already covers it; otherwise leave it. The independent review found the safeguards are mostly load-bearing, so there is less over-engineering to remove than I estimated. |

**Net:** roughly a day of Codex work after delivery (E1 plus whatever E3 rides along), proven by the same gates.

Sources: design/runtime-E1-shared-module-design-2001.md, design/agent-E2-legacy-abi-design.md (plus -sizing.md), design/runtime-E3-audit-revised-2009.md and design/runtime-E3-final-review-2011.md.
