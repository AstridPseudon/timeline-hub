## FAIL — F-D52-core-five independent review

- Diagnosis accuracy: **FAIL on limits**. The failure location is proved, but “provider incorrectly requires an after pin” is too broad. The retained source has authenticated earlier `commit.materialization` custody; the later inverse record simply does not carry that custody across its stage boundary.
- Retained behavior: **FAIL** — three selectors passed, two failed:
  - PASS: native-order captured config, nested config history, retained fork source baseline.
  - FAIL: independent parent edit + preview redo; retained-sibling redo.
  - Both fail at Agent `_commit_patch._materialization_sites` with `history_unavailable: inverse stage image differs from authenticated effects`.

Evidence verified:

- Exact five selectors in durable `evidence/assigned.xml`/`assigned.log`; no original body rerun.
- Test files unchanged, including author before/after file and AST hashes; current worktree is clean.
- Agent imports resolve to this worktree; Runtime imports resolve to `/home/user/work/runtime`.
- Production path is live: Runtime `commit_timeline` → coordinator/provider → Agent `commit()` → `commands.execute(..., commit_request=request)` → materialization/acceptance.
- Accepted records show publication-1 materialization from shared `shot-rev-1`/`internal-1` to fork roots, with both occurrence owners. Undo publication-3 records parent-edge restoration and old fork-root effects, but no after-side `commit.effect` for the retained shared source. That absence is a no-write observation, not proof that the source is unauthenticated.
- The precise Agent seam is inverse-stage materialization custody in `_commit_patch._materialization_sites` / `inverse_address_resolver`; no Runtime attribution or fix is proposed.
- The passing source-copy/fork path proves pure source reconstruction and exact closure restoration only; it does not qualify durable accepted-history redo with a retained sibling.

Checks:

- `git diff --check`: PASS.
- Ruff/mypy: N/A; no files changed.
- No code, test, product, schema, generated, package, or fixture changes.
- No HTTP/authentication, installed-runtime, browser, full-suite, or original known-failing rerun performed.
- `DONE` marker created.