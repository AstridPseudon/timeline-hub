---
name: pack-builder
description: "Design and implement reusable Astrid packs and capabilities. Use when deciding whether a missing idea belongs in an existing executor, a new executor, an orchestrator, a visual element, or a timeline rendering extension, and when authoring the corresponding manifests and entrypoints."
metadata:
  short-description: "Build reusable Astrid extension packs"
---
# Pack Builder

Package a repeatable capability as an Astrid extension. Start with the
catalog and reuse what already exists. A pack owns a namespace and its public
declarations; it is not a data schema or a gateway command. For a new pack,
follow the [authoring guide](../../../../../docs/guides/create-a-pack.md) and
the [manifest reference](../../../../../docs/packs/creating-packs.md).

## Choose what to build

1. **Existing capability:** inspect `astrid.sdk.discover()` and
   `astrid.sdk.get_capability(...)`; compose what fits.
2. **Action or UI:** declare the public contribution in `pack.yaml` and put
   its implementation under the matching role folder.
3. **Rendering:** declare it under `rendering:` and follow the authoring guide.
4. **Shared code:** put private support used by contributions under `shared/`.
5. **No new pack:** keep one-off work in a run directory.

Reuse capabilities with `astrid.sdk.invoke(...)`. Do not open the Runtime
database or invoke `run.py` directly. See [creating tools](../../../../../docs/guides/creating-tools.md)
for the contribution choice and [pack data storage](../../../../../docs/packs/data-storage.md)
for mutable project settings.

## Give the pack useful skills

Give each pack one main skill for its common workflow. Add an extra skill when
a distinct workflow needs its own instructions or should load only on demand.
Keep supporting details, examples, and assets in ordinary references linked
from a skill. Move content out of the main skill when it crowds the normal
path. The [skill-writing guide](references/writing-skills.md) explains the
split and manifest declarations.

The [Timeline pack](../../../timeline/pack.yaml) is the worked example: its
main skill covers everyday edits; `series`, `narrated`, and `review` are
declared extras; its helpers and guides are references. The main skill lives
at `docs/SKILL.md`; each extra is a `kind: skill` resource in `pack.yaml`.

Validate the pack and inspect its declarations with the pack CLI. Use the
[pack testing guide](../pack-testing/SKILL.md) for test lanes. Regenerate the
capability catalog after changing a manifest.
