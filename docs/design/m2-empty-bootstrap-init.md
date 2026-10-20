# M2 empty-bootstrap initialization (`timeline.init` v1)

Runtime creates a timeline as the exact empty parent
`{config:{clips:[],tracks:[]}, registry:{}, clips:[], occurrences:[]}`. The App
authors more than that on a fresh timeline: output, name, slug and the asset
registry container (then V1/A1 through `track.create`). Those fields have no
legal edit. `timeline.init` is the one guarded write that supplies them. It is
not a root replace and not a general setter.

## Contract

| Field | Value |
|---|---|
| op / version | `timeline.init` / `"1"`; `select` is exactly `"parent"`; no intent overrides |
| args (closed) | `name`, `slug` (non-empty strings); `output` with exactly `resolution` (`WxH`), `fps` (integer ≥ 1), `file` (non-empty), `background` (string or `null`), `background_scale` (number or `null`) |
| writes, in order | `parent::config.output` (whole object), `parent::name`, `parent::slug`, `parent::registry` = `{assets:{}}` |
| capture | `astrid.sdk.timeline._init_commands.capture_timeline_init(bundle, name=, slug=, output=)` |

Schema: `TimelineInitArgs` in `edit-command.schema.json`, with an `allOf` branch
that pins version, select and the empty intent.

## Guards

* **Pristine-init.** The handler refuses (`not_pristine`) unless the parent is
  exactly the bootstrap bytes (extra keys such as `theme` or opaque fields
  fail) and the bundle has no placements or shots. A second init, or an init
  over a timeline that already has any authored content, is refused.
* **Null / absence.** `background: null` is a present value; every other
  output field is required, so absence never stands in for `null`. `output`,
  `name`, `slug` are recorded as `absent` before; `registry` as present `{}`
  before, so `{}` and `{assets:{}}` are never conflated and resource names are
  not payload metadata.
* **Opaque.** Anything beyond the bootstrap bytes makes the parent non-pristine
  rather than being merged or overwritten.
* **Order.** One batch `[init, track.create V1, track.create A1]` keeps command
  order; each later capture is taken against the state left by the previous one.
* **Inverse / redo.** Recorded writes carry first-before/last-after, so undo
  restores the bootstrap bytes exactly and redo restores the initialized ones.
  Init's addresses are disjoint from track rows, so it can be undone without
  touching tracks created after it.
* **Rebase.** Reads of `config`, `registry`, `clips`, `name`, `slug` plus the
  four write addresses are the guard set: an intervening write to any of them
  is `intervening_write`. Replaying onto a head that already carries the
  defaults, or that was edited and undone, is `not_pristine`; defaults are never
  re-applied over later edits.

## Not covered (other owners)

* Runtime same-ID headless repair and crash-resume of create→init: Runtime owns
  proving the shell pristine; the Agent guard only accepts exactly-empty bytes.
  State alone cannot tell "never initialized" from "initialized, then fully
  undone"; the caller must resume only from proven bootstrap history.
* App `createDefaultTimeline` replacement and outbox wiring.
* Theme, `theme_overrides`, `generation_defaults` stay absent.

## Evidence

`tests/editing_conformance/test_timeline_init.py` and the golden
`fixtures/recipe_m2_timeline_init.json` (bundle, command, after-bundle, records).
