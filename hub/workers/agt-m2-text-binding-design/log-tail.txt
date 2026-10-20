## Report: agt-m2-text-binding-design

The design contract and the executable spike are done. The spike shows the command's round trip, inverse and clear-vs-empty behaviour on the real recipe harness, and it turned up four design-level gaps in the current code. Nothing in product code changed.

**Deliverables**
- `design/m2-text-binding-contract.md` in `$ORCH/design`: command shape, guards and rebase, inverse, the Runtime proposal, gaps, open decisions.
- `tests/editing_conformance/test_recipe_text_binding_spike.py` in the worktree.
- `design/deletion-ledger.agent.md`: row AG-M2-TB01, status `held`. Nothing was deleted.
- `commit-msg` and `DONE` in the workers directory. The commit message omits the model-name line, per the brief.

**Tests (venv Python)**
- `pytest tests/editing_conformance/test_recipe_text_binding_spike.py`: **22 passed, 1 xfailed**. The xfail is `test_runtime_port_declares_exact_text_selection`, strict, with reason G-RT1. It is a presence check on `def text_selection(`, not an acceptance proof.
- `pytest test_recipe_m1_commands.py + spike + test_runner_selftest.py`: **108 passed, 1 xfailed**. The spike's patches do not leak into the neighbouring suites.
- `ruff check --isolated --select E4,E7,E9,F,I,BLE` on the spike: passed.
- No full suite was run, and no `request-test` was submitted.

**What the spike shows.** Round trip, dependency record, inverse and redo, empty text distinct from clear and from absent, same-value recording, ABA refusal, guard refusal and disjoint rebase. Each runs on the recipe harness with a stub descriptor.

**Gaps the spike found** (each is in the contract's §4)
- **G-SCHEMA:** the scoped-ref patterns in `edit-command.schema.json` refuse `occurrence:…/text-binding:…` before any handler runs. The popup worker reported the same gap. Runtime's pinned copy needs regenerating.
- **G-INV1:** undoing a clear goes through `inverse.py:144-146` → `ctx.create`, which needs an authored collection. A keyed binding row has none.
- **G-INV2:** `apply_inverse` crashes on any recorded absent→absent removal at path `[]` (`inverse.py:146`, `KeyError: 'value'`). This is generic and I did not patch it. This op refuses no-op clears instead.
- **G-LEGACY:** main's authoring fixture carries an inline row, `{"slot":"voiceover","text":"hello"}` (`tests/timeline/test_authoring_bundle.py:120`). It has no `kind`, so it is inline text, which the design forbids. The command refuses it as `unsupported_shape`.

**Decisions I made, for you to confirm**
- **`select` is the occurrence, not a clip or element.** The brief says "clip/element ref", but text is shot-owned in main. A clip cannot own it without a new authority field. This is the one place I did not follow the brief's wording (O3).
- **Clear of an absent binding is refused** (`absent_binding`), not recorded as a no-op. This avoids G-INV2 for this op.
- **Authored rows carry identity only.** `head` and `binding_id` are Runtime-derived after acceptance, so the authored doc can't contain them (O1; a compatibility change for pinned readers).
- **The MIME string is `text/plain; charset=utf-8`, per the brief.** Main's preview uses `text/plain`, so Runtime must confirm which exact string it stores (O2).

**Runtime proposal** (§5 of the contract, for the Runtime owner)
- P1: an internal port method `text_selection(TextSelection) -> VerifiedText`, closed types, no bytes returned, project from the commit scope, validated and retained through the existing media-input path.
- P2: a server-derived before/after binding projection in the same acceptance transaction, refusing on before-mismatch.
- P3: identity-only authored rows.

**Open decisions:** O1–O7 in §7 of the contract. These include text ordering for undo (O4), shared-chapter ownership (O5) and the legacy-row migration (O6).

**Blocked or unverified**
- Runtime acceptance, CAS bytes, relational projections, App and any live journey are not proven. The one Runtime-dependent check is the presence xfail.
- **Cleanup incomplete:** the sandbox denied `rm -rf` on `.pytest_cache`, `.ruff_cache` and `tests/__pycache__` in the worktree. All three are git-ignored, so they won't be committed. Please remove them if the brief's "no build output" rule matters for the harness.
