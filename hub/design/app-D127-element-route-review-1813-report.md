# D127 review report

Result: **FAIL** — selector/source is valid, but recipe is not ready.

Verified:

- App d5a1 source/tree and single `p2-element` selector unchanged.
- Original lifecycle, 5-second expect timeout, v2 request/reply/history/undo guards retained.
- Watchdog `2s` for `p2-element` is correct; `20s` applies to full `p2`.
- Agent 070dfc and Composition 635f source accepted.
- Raw capture remains absent; historical request 3 remains pending with unknown denominator.

Finite corrections are recorded in `evidence/corrections.md`:

1. Use qualified Runtime ab1e4f61/tree, not e319; recipe path is also misspelled.
2. Restore explicit reviewed external helper SHA `4ee0424b…`; current custody is absent.
3. Obtain missing App detached receipt/target metadata and retain all four receipts.
4. Publish the complete `p2-element --submit` controller command and fixed output/plan paths.
5. Unescape Markdown fences.

Evidence:

- `evidence/verdict.json` — parses successfully.
- `evidence/source-custody.json` — parses successfully.
- Worktree remains source-clean.
- No tests, lint, typecheck, preflight, service, browser, or profile runs performed per task scope.
- No source commit created.