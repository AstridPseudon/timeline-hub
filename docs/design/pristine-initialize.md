# Pristine timeline initialization

`timeline.init` v1 supplies the authored defaults missing from Runtime's legal
empty `createTimeline` publication. It is an ordinary recorded EditCommand,
implemented in `astrid/sdk/timeline/native_initialize.py`. It adds no transport,
provider ABI, persistence table, or replacement-document escape hatch.

The source is App main `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa`,
`src/tools/video-editor/lib/defaults.ts:4-44` and
`src/integrations/runtime/createDefaultTimeline.ts:50-82`. The fixture
`tests/editing_conformance/fixtures/pristine_initialize.json` contains the full
App parent, captured commands, and authoritative records.

## Capture and raw paths

Call `capture_initialize(bundle, name=..., slug=..., output=...)`. The required
closed arguments are `name` (string), `slug` (nonempty string), and `output`
(exactly resolution `1280x720`, integer fps `30`, file `output.mp4`, background
`null`, background_scale `null`). This command initializes today's App defaults;
it is not an output-settings editor. Name and slug are copied exactly. The App
retains its existing slug derivation, including empty-name fallback `timeline`.

The selector is exactly `parent`, version exactly `1`, and intent is empty.
Writes are ordered: `parent.config.output`, `parent.name`, `parent.slug`, then
`parent.registry.assets = {}`. All four original addresses must be absent.
The registry object itself remains at `parent.registry`; there is no new
`config.registry`, and no parent/config/registry root replacement. The entire
empty parent is read and guarded, including its empty collection order. Unknown
or legacy siblings cause refusal and remain untouched.

After this capture, append existing `capture_track_create` operations for the
full App V1 row then full A1 row, capturing each against its preceding local
result. Submit the three commands in one batch. Track rows retain label, scale,
fit, opacity, and blendMode. Theme, theme_overrides, and generation_defaults
remain absent. Normal inverse machinery reverses the entire batch exactly;
inverse-of-inverse redoes it without invoking the initializer again. Original
reads/order/write guards refuse changed opaque data and intervening writes.

## Authority and recovery

State equality alone is insufficient: undo can restore the original empty
revision. The provider authenticates the existing base publication through
`history_entry`, requires `intent == bootstrap` and `previous is None`, and
requires the exact current revision/publication pair to equal that base.
It checks the pair again after acceptance CAS races. Initialization never
rebases across another accepted publication, including edit→undo equal bytes.
Detached capture/replay proves deterministic command meaning only; it cannot
authorize initialization. No caller-supplied pristine flag exists.

Runtime's existing ledger handles accepted exact-key retries before invoking
the provider. The real in-process Runtime regression proves that an old exact
init retry returns its original result after restart and undo while the current
head remains unchanged. A changed payload under that key is refused. Fresh
init attempts after undo are refused; explicit undo/redo remain legal.

The App owner must persist the timeline identity, original name/slug/defaults,
create key and init key before create, then persist the captured init batch,
original base pair and exact in-flight request before commit. Resume a
create→init crash using those facts and verified Runtime history; never guess
from locally default-filled display data. The test models durable caller intent
with the existing Agent Outbox, not an implemented App recovery flow.

Same-ID headless repair stays Runtime-owned. This initializer requires an
already accepted bootstrap and cannot manufacture one. App's old bootstrap
publisher must remain until the Runtime repair and App replacement are paired
and qualified through the real Door, including original positive repair tests.

## Schema successor

The complete schema retains frozen S2 `26ef2bbb` (raw SHA-256
`a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`), adding
only `TimelineInitArgs` and its operation condition: 49 definitions / 23 operation
conditions. The regression removes precisely those additions and verifies the
canonical complete S2 hash, retaining producer, consumed, retained-element,
numeric, inverse and restore definitions. S2 producer implementation remains
its owner's work; this older worker base has no `producer.guard` handler.
The manager must freeze the composed successor before normal Runtime generation
and pin qualification. This change leaves `runtime.lock.json` unchanged.
