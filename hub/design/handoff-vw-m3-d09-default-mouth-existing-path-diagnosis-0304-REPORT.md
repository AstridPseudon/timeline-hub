# D09 default-mouth source diagnosis

The current presenter has two deliberately different facts:

- `component.tsx:88-108` → `motion.ts:28-29` normalizes omitted `mouth` to the
  real drawing anchor `{151,104,19}`; `scene.ts:15-29` therefore reports public
  `diagnostics.mouth.status = "known"` and `(894,606,1032,654)`.
- `motion.ts:44-61` keeps the old compatibility footprint: omitted raw mouth
  returns `null`; partial `{x,y}` retains width 16; malformed raw input refuses
  a compatibility crop. Python `model.mouth_box` separately returns `None` for
  omitted, the width-16 partial box `(894,606,1014,654)`, and the existing
  coercive raw-invalid box `(-12,-18,5412,30)`.

`render_lipsync` (`builtin.py:369-441,450-527`) only accepts public rows when
raw integer `x/y/w`, one source-bound evidence mode, exact frame/basis/address,
and component-zero `KNOWN` ROI all qualify. Omitted/partial/raw-invalid remain
on the existing private state/crop fallback. In particular, omitted default
must preserve no selected legacy crop; public `KNOWN` is semantic normalized
component geometry, not automatic legacy-crop qualification.

No deletion is safe: `mouth_box` remains needed by the retained unqualified
pixel fallback, and `mouth_state` is also used independently by
`model.py:600-603`. Do not repeat the accepted 0244 physical proof or invent a
component geometry correction. The one next proof is a focused omitted-mouth
consumer test asserting public `KNOWN` does not select a legacy crop and the
existing state strip remains; no matrix and no physical run.

