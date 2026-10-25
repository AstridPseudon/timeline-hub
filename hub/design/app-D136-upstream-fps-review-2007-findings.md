# D136 source findings

## Verdict

`PASS_REGRESSION_SOURCE`.

G1 is qualified only by the supplied App lead readback at 20:22: it reported
both the upstream Agent `origin/main` and actual `git ls-remote` at
`886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55`. This worker performed no fetch and
claims no live freshness check. The local object matches that supplied tip and
the authored projection path is absent at that exact object.

## Decisive G2 chain

The exact authored input is at
`tests/sdk/test_timeline_capture_projection.py:418-420`:
`parent.config.theme_overrides.visual.canvas.fps` has shape `[30000, 1001]`.
The receiving source is unchanged at the reviewed commit. Its
`astrid/sdk/timeline/validation.py:53-64` `_fps` accepts only a positive finite
scalar or an exact positive integer `{numerator, denominator}` mapping. The
`_fps_values` traversal at lines 81-92 reaches the authored path, so this is a
known typed parameter and not an opaque field carried through untouched. The
final candidate call at `validation.py:537` invokes that check before candidate
publication.

The captured pristine upstream object is decisive in the other direction. Its
`timeline-config.schema.json:434-458` defines `ThemeOverrides.visual` as an
object with `additionalProperties: {}`. Direct validation of a minimal valid
timeline containing the exact nested shape produced zero schema errors. The
pristine public caller `banodoco_composer.py:182-185,263-272` calls
`validate_timeline` on construction and serialization. That validator keeps the
path in the shared-schema view, then its `_timeline_fps` helper at lines
178-187 reads `visual.canvas.fps`; a list does not satisfy its scalar branch and
falls back to `30.0`. It is therefore an upstream-accepted input that the
receiving provider refuses, not an unconsumed path inferred only from missing
validator code.

This applies the settled D136 conditional ruling: upstream acceptance plus
receiving refusal is a D54a regression finding. It does not authorize changing
the authored value, converting it to a rational object, approximating it,
widening the guard, or rerunning the nine selectors.

## Contract and caller boundary

C0 §1 requires provider validation of final timing/structure/parameter schemas
and says unknown control fields are invalid while open document fields remain
preserved. C0 §§2-3 require closure-root resolution and the existing previous
value, membership/order, dependency, and atomic guards. C0 §6 requires opaque
`meta` namespaces to be preserved verbatim and ignored by Composition/renderers;
that preservation rule does not turn the provider's explicitly traversed FPS
parameter into opaque `meta`.

The public publication path is unchanged: `publish_authoring_candidate` builds
the v2 request and calls `writer.commit_timeline`; independent D1001946 source
evidence establishes the registered RuntimeService route used by production.
The request/reply path remains under Runtime ownership. No refusal bypass,
alternate writer, or D130 release was introduced or credited.

## Conserved proof and disposition

The authored source hash is
`6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436` and the
receiving diff has only that test path. The protected census remains 43 original
predicates, 11 test bodies, and 54 fixture statements; the current module has
44 assertions because one setup assertion is excluded from the original
predicate count. Historical independent evidence remains separated as 27/27
PASS and 9 setup errors; no nine-selector body ran here.

Owning seam/direction only: Runtime/Agent should reconcile the pristine public
FPS semantics with the provider's typed rule under D136. The original nine
setup errors remain visible pending that owner decision.
