# VW-D09b/c partial-crop component compatibility proposal

## Verdict: blocked; no unapplied production patch

The actual partial result is retained, but the current Agent/Composition seam
has no permitted carrier for a separate compatibility inspection rectangle.
Do not change `diagnostics.mouth`: it is the component's semantic capability
region and must retain its independent known/unknown rules. Do not add a
`legacyInspection` diagnostic: the installed public Composition contract has
no such field, and adding it would be a public type/API change explicitly
outside this task.

This is the exact blocker requested by the brief. No repository source or test
was changed, no caller was activated, and no private crop/statistics path was
deleted. The worker's proposed patch is intentionally absent; the companion
`*-NO-PATCH.md` records why a git-applicable patch would be misleading.

## Source-backed seam audit

Worker tree: `c4b964f6a050edf63a4278d35717e46a88a80386` /
`d7796be264c341adbcb9765aae374b832dede144`.

- `motion.ts:28-29` owns the drawing normalization through `mouthAnchor`:
  omitted/partial input draws with `{x:151,y:104,w:19}`; malformed input is
  safely normalized for semantic motion.
- `motion.ts:33-42` owns the same-drawing `mouthEraseRect` and padded semantic
  `mouthStateRect` geometry.
- `motion.ts:49-61` already owns the granted legacy compatibility seam:
  explicit width 19 stays explicit, omitted width uses legacy width 16, absent
  input returns `null`, and malformed/non-integral/out-of-range raw input
  returns `null`. This is the right component-owned helper and must remain
  separate from semantic normalization.
- `scene.ts:17-28` currently projects only `mouthStateRect` into the existing
  public `diagnostics.mouth` field. That field is the normal public scene
  carrier for semantic capability, not a second crop/statistics channel.
- The read-only installed public declaration
  `/home/user/work/app/node_modules/@banodoco/timeline-composition/dist/scene-capabilities.d.ts:25-35`
  defines `ComponentDiagnostics` as only `motion`, `face`, `mouth`, and
  `text`. There is no existing compatibility field. A `legacyInspection` key
  would require a public type/API update; reusing `mouth` would conflate the
  two contracts and break the required UNKNOWN semantics.
- `tests/packs/rendering/presenter_crop_geometry.mjs:15-20,43-45` already
  carries the compatibility helper result alongside the pure public-scene
  `diagnostics.mouth` answer for direct crop mapping. It is a test-side
  observation carrier, not a production/public capability field. The current
  direct crop suite already asserts this split.

## Retained evidence and exact values

The original explicit proof `...32349` proves only the explicit
`{x:151,y:104,w:19}` case: old/private/public compatibility crop
`(298,202,345,219)` / 799 pixels, separate erase crop
`(300,206,343,215)` / 387 pixels. Its natural fractions are
`0.42052565707133915` for all three adjacent pairs; its retained controls use
the unchanged `CHANGE_LEVEL=18` comparator and strict `fraction > 0.02` rule.

The actual partial proof `...10870` is retained and remains authoritative for
the partial input `{x:151,y:104}` (omitted width):

| crop/statistic | retained value |
| --- | --- |
| private partial crop | `(298,202,339,219)` / 697 px |
| public compatibility crop | `(298,202,345,219)` / 799 px |
| erase crop | `(300,206,343,215)` / 387 px |
| natural private fractions | `0.44763271162123386` × 3 |
| natural public fractions | `0.42052565707133915` × 3 |
| natural erase fractions | `0.8682170542635659` × 3 |
| planted 8 private/public/erase | `0.011477761836441894` / `0.010012515644555695` / `0.020671834625323` |
| planted 15 private/public/erase | `0.021520803443328552` / `0.01877346683354193` / `0.03875968992248062` |
| planted 16 private/public/erase | `0.02295552367288379` / `0.02002503128911139` / `0.041343669250646` |
| planted 20 private/public/erase | `0.028694404591104734` / `0.025031289111389236` / `0.05167958656330749` |

These values retain the original denominator and threshold. They show why the
private 697 and public 799 results cannot be relabeled as equivalent: the
strict boundary decisions differ at 15 pixels, while both detect 16 pixels.
The private fallback, all statistics, and all threshold controls remain
unchanged.

Input disposition remains exact:

| raw input | semantic public `mouth` | compatibility helper |
| --- | --- | --- |
| explicit `{x:151,y:104,w:19}` | known normalized 799-pixel footprint | known 799-pixel footprint |
| partial `{x:151,y:104}` | known normalized width 19 | known legacy width 16 / 697 pixels |
| absent/default (`None`) | known semantic normalized footprint | `null` / no inspection |
| malformed `{x:'bad',y:null,w:900}` | known semantic normalized width 40 | `null` / honest refusal |

`public799` and `defaultNone/publicnull` therefore remain exact; raw-invalid
remains honest. Semantic capability UNKNOWN rules for mosaic/outer geometry
remain independent and are not changed by this compatibility disposition.

## Test/patch disposition

No red-before/green-after run is claimed because there is no permitted patch
to apply. The existing pure direct crop path already exercises the shared
helper and exact mapping; its result is the retained 10870 JSON above. A
future owner-approved change would first need a Composition-owned contract
decision for a separate compatibility carrier, then a public13-compatible
type/package unit. That is outside this bounded Agent task and must not be
smuggled in as a presenter-only field.

Commands/results for this worker:

- `git status --short --untracked-files=all` — clean before handoff; no repo
  files were edited.
- `git diff --check` — pass; no repo diff.
- Read-only source/type/evidence inspection — pass.
- An attempted direct Node query from this worktree stopped before execution
  because this worker has no local `node_modules` and ESM could not resolve
  `@banodoco/timeline-composition`; no dependency or cache was modified.
  The retained 10870/32349 pure-path evidence above is not relabeled as a new
  run.
- No browser, helper capture, Runtime, socket, central, render, full suite,
  install, graph copy, or package mutation was run.

## Owner next step

Keep the current component helper, semantic `diagnostics.mouth`, private crop,
statistics, fallback, and thresholds. Escalate only the missing public
compatibility carrier to the Composition/API owner if separate inspection
facts are still required. Do not activate a production caller from this
worker.
