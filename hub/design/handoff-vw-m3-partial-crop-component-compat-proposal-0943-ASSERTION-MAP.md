# Retained assertion map

| Assertion | Owner/source | Disposition |
| --- | --- | --- |
| explicit `{x:151,y:104,w:19}` maps to 799 | `motion.ts:49-61`; retained 32349 | retain exact |
| partial `{x:151,y:104}` omits width and maps to legacy 697 | `motion.ts:55-60`; retained 10870 | retain actual result |
| semantic public mouth stays normalized width 19 | `motion.ts:28-42`; `scene.ts:17-28` | independent; do not replace |
| absent/default compatibility result is `null` | `motion.ts:50-52` | retain exact |
| malformed/raw-invalid compatibility result is `null` | `motion.ts:56-58` | retain honest refusal |
| private/public/erase statistics and fallback | retained partial JSON | unchanged |
| strict threshold | existing comparator, `fraction > 0.02` | unchanged |
| `CHANGE_LEVEL=18` | existing comparator | unchanged |
| semantic UNKNOWN for mosaic/outer geometry | existing `scene.ts` path | independent; unchanged |
| separate public compatibility carrier | Composition `ComponentDiagnostics` | missing; blocker |
