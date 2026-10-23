# G3 independent joined-source review — PASS

Reviewed `5a313eb88e8ddce1e9e033ed9cfde7ef433f7c55`, a documentation-only tip
over joined commit `374e86919` (`44b46935a` G3 plus `4454a7a2f` R2), with G3's
production fix reviewed against `a92e08093`.

The public publisher now hydrates from the exact original revision/publication
pair. It validates the historical receipt, uses the retained canonical document
or exact immutable image fallback, compares the hydrated closure, and refuses
changed pairs or canonical sources. It does not recapture from the latest head.
The caller and session staging both pass that exact publication. The emitter
performs the verified same-alias media swap before residual `doc.patch` changes
and resolves child roots through sequential physical owner bindings.

The compound regression covers old/new five-field media selections, retained
media, timing, order, opaque values, explicit null, absence, immutable reload,
exact inverse/redo, stale source/publication refusal, and exact canonical
restoration. No fake authority, raw inverse, inferred continuation, or second
writer was added. Current R2 physical-binding and later-history guards are
unchanged from `4454a7a2f`.

Evidence:

- Original compound inverse: **1 passed in 1.94s**.
- Changed authoring-media/emitter/session/revision-diff/sync set: **265 passed,
  2 deselected in 15.95s**.
- Focused physical-root/media/inverse guards: **162 passed in 13.17s**.
- Changed typed modules Ruff: **passed**; private mypy: **passed**.
- Normal ratchets: Ruff **2150/2150**, mypy **1915/1915**.
- `git diff --check`: **passed**.
- Retained unchanged v2 evidence: **425 R2 tests** and **274 G3/emitter tests**.

Including unchanged `store.py` in scoped tools reproduces pre-existing Ruff
E731 at line 227 and mypy `float(raw)` at line 563; no ratchet growth occurred.

The frozen Runtime v2 wire and live-process restart remain intentionally
unqualified. Verdict: **PASS for joined G3 source review; Runtime wire/restart
qualification remains separate.**
