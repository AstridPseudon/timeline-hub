# WC10 pristine raw `timeline.init@2` — current source handoff

Date: 2026-10-21. Scope: source-only handoff to the delegated Runtime WC10
migration. This records the already-reviewed unregistered Agent spike and the
existing Runtime carrier; it is not a new design or an activation authority.

## Exact source identity

The final committed source of the structural-smuggling fix is:

```text
Agent commit: 2c93619bf784150fe9e5e319714d86a2aa4630b1
Agent tree:   e10ad19072a4dd1e9cde219299e2f2ff526bca19
Parent:       dfb97311ef54d1ef1706c2228bf2d84514c5b024
Parent tree:  10089dba8ea9471a8b3a6f84ec65ef0b32dbbbec
```

`2c93619` changes only the test-only spike
`tests/editing_conformance/test_pristine_raw_initialize_proposal.py`
(blob `96fa3a94d46d695ff5489f3c7b5c01adec257e21`). The reviewed source
blobs at that commit are:

```text
astrid/core/timeline/schema/edit-command.schema.json
  8cedcd2506e5408e8e96a74adca5abd036d03f7e
astrid/sdk/timeline/native_initialize.py
  7cec29956e0280d8fe682701ab5de42ce5b07edd
astrid/sdk/remote.py
  3f235d25409b0288fc0279cad6d39fb07d732508
astrid/sdk/timeline_duplicate.py
  a780ebe877256c44b48ad89870c18df32fdb0916
```

The command schema blob is byte-identical to the parent and still admits only
`timeline.init` version `"1"` (the `const` at the existing schema branch near
`edit-command.schema.json:1711-1721`). The candidate is not an ancestor of the
current Agent integration head; use the commit/tree above as the reviewed
source identity, not as a claim that v2 is live.

There is no registration, generated artifact, pin, live-caller, Runtime, App,
or frozen-016 change in this candidate. `validate_command(raw_init_command())`
continues to refuse the proposed v2 command. Current status keeps the private
016 source (`da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406`, tree
`486fe045f66182b33520bea971d31add3f713ea9`) and frozen `10226` immutable and
on HOLD. The populated duplicate caller remains live and separate.

## Existing invocation and proposed raw envelope

The live v1 recipe remains the existing `native_initialize.capture_initialize`
call:

```python
capture_initialize(bundle, name=name, slug=slug, output=output)
```

It constructs exactly:

```json
{
  "schema_version": 1,
  "op": "timeline.init",
  "version": "1",
  "select": "parent",
  "args": {"name": name, "slug": slug, "output": output}
}
```

The v1 handler writes only `parent.config.output`, `parent.name`,
`parent.slug`, and `parent.registry.assets`; it is unchanged and does not
preserve the legacy raw canvas path.

The unregistered raw candidate uses the same operation family and existing
provider-backed commit carrier, with this exact envelope:

```json
{
  "schema_version": 1,
  "op": "timeline.init",
  "version": "2",
  "select": "parent",
  "args": {
    "name": "Custom",
    "slug": "custom",
    "config": {
      "tracks": [],
      "theme_overrides": {
        "visual": {
          "canvas": {
            "width": 1920,
            "height": 1080,
            "fps": 30,
            "background": null
          },
          "opaque_visual": {"enabled": false}
        },
        "opaque_theme": [null, false]
      },
      "opaque_sibling": {"literal": "preserve-me"}
    }
  }
}
```

`args` is closed; `args.config` is the intentionally open semantic-JSON
subtree. The candidate writes only, in order, `parent::config`, `parent::name`,
and `parent::slug`. It does not write a root, `output`, registry assets,
tracks, clips, placements, shots, or any other sibling. Semantic JSON and
array order are preserved; Runtime’s existing canonical JSON may reorder object
member text.

Runtime’s ACK (`runtime-wc10-pristine-raw-source-review-0630.md`) confirms that
the existing provider-backed `/v1` carrier already transports this raw config
inside `PreparedCommit.canonical_document`; no Runtime DTO, port, endpoint, or
provider-ABI change is needed. The old `publish_parent_composition` escape
hatch remains refused for tracked publications.

## Admission guards

The candidate must be interpreted with all of these boundaries:

1. The command record has `ordinal == 0`.
2. The authenticated input parent is exactly the empty bootstrap parent:
   `parent.config.clips == []`, `parent.config.tracks == []`,
   `parent.registry == {}`, and top-level `clips == []`.
3. Top-level `placements` and `shots` are empty (the no-shot guard).
4. `parent.name` and `parent.slug` are absent, not merely equal to the
   requested values.
5. The open config has no structural birth. Each known structural path is
   absent or empty (`[]`/`{}`): `tracks`, `clips`, `occurrences`, `placements`,
   `shots`, `groups`, `pinnedShotGroups`, `media`, `references`, `reference`,
   `assets`, and `registry.assets`. Nonempty values require ordinary recorded
   creation/input facts and are refused as `unrecorded_birth`.
6. The provider boundary remains authoritative beyond ordinal zero: the
   authenticated bootstrap intent, `previous is None`, exact base-head pair,
   and CAS recheck must hold. A new init after init→undo, even if bytes are
   equal again, is `not_pristine`.

The structural boundary is path-bounded. It does not reinterpret
`theme_overrides`, opaque siblings, namespaced metadata, explicit nulls, or
array order as structure. Runtime’s source review notes one limitation in the
test-only spike: `_capture_raw_init_unchecked` performs its three local
in-memory writes before `_require_empty_structure` is called. The 14 refusal
controls prove the resulting candidate is rejected, but not a pre-write
product admission ordering. A future Agent handler must check the structural
boundary before any scoped write; this handoff does not change that source.

## Legacy positives and mapping

The original `tests/v10/test_timelines_create.py` source uses the raw config
path directly. The default shape is:

```json
{
  "tracks": [],
  "theme_overrides": {
    "visual": {"canvas": {"width": 1920, "height": 1080, "fps": 30}}
  }
}
```

The CLI constructs that shape at `astrid/packs/timeline/cli.py:175-192`, and
the legacy SDK `RemoteTimelines.create_empty` copies it unchanged into
`parent_composition.config` at `astrid/sdk/remote.py:482-552`. The specified
canvas/fps positive (`640x360`, `24`, caller idempotency key) is the same raw
shape with those authored values. The generated-ULID/no-id positive and
shell-refusal positive remain distinct controls; the approved native fixture
maps only the ordinary default/no-config path to the existing v1 command and
does not close the custom raw positive.

The raw round-trip fixture additionally proves the original-sensitive cases:
`theme_overrides.visual.canvas`, explicit `background: null`, absent
`background_scale`, opaque sibling values, opaque `[null, false]` metadata,
and canvas array/member sequence `width, height, fps, background`. The custom
canvas positive remains OPEN; it must not be converted to `config.output` or
turned into a refusal. `astrid/sdk/timeline_duplicate.py:194-200` is a genuine
nonempty caller that deep-copies a populated source config into `create_empty`;
it remains live and is not a pristine-init positive or a migration target for
this handoff.

## Evidence and next dependency

The prior source reports retain the following evidence:

- raw proposal/provider-boundary lane: `8 passed` for the proposal plus
  provider guard tests; the exact command was
  `PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_pristine_raw_initialize_proposal.py tests/sdk/test_timeline_pristine_initialize_provider.py`;
- structural-smuggling refinement: `14 passed` targeted controls, plus `4
  passed, 113 deselected` on the `create_empty`/duplicate positive lane;
  Ruff and `git diff --check` passed. The refinement report did not retain the
  full shell command, so that count is reported as prior evidence rather than
  a rerun here;
- Runtime’s raw-carrier ACK and empty-structure review were source reviews;
  no Runtime product test or installed/socket proof was run for this source.

One next normal-cohort dependency remains: Agent must supply a committed v2
handler/schema/registry cohort with the structural check before scoped writes.
Only after that exact cohort exists can Runtime and App perform the paired
normal provider-backed qualification of the custom raw positive, including
authenticated bootstrap/CAS, retry/restart, inverse, and later-edit refusal.
Until then this is a bounded Runtime source handoff only: no implementation,
activation, generated pin, generation, Runtime/schema edit, route retirement,
or live caller migration is authorized.
