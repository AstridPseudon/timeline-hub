---
name: pack-builder
description: "Design and implement reusable Astrid packs and capabilities. Use when deciding whether a missing idea belongs in an existing executor, a new executor, an orchestrator, a visual element, or a timeline rendering extension, and when authoring the corresponding manifests and entrypoints."
metadata:
  short-description: "Build reusable Astrid extension packs"
---
# Pack Builder

Package a repeatable capability as an Astrid extension. Start from the
catalog and reuse what already exists. A pack owns a namespace and public
declarations; it is not a data schema or a new gateway command. For mutable
pack settings in a project, follow the [pack data contract](../../../../../docs/packs/data-storage.md).

Read only the guide needed for this work:
[authoring](../../../../../docs/guides/create-a-pack.md),
[manifest](../../../../../docs/packs/creating-packs.md),
[contribution choice](../../../../../docs/guides/creating-tools.md),
[contract](../../../../../docs/packs/contract.md) and
[taxonomy](../../../../../docs/packs/pack-taxonomy.md),
[discovery](../../../../../docs/guides/discovery-for-agents.md) and
[SDK](../../../../../docs/reference/sdk.md), [testing](../pack-testing/SKILL.md),
[skill writing](references/writing-skills.md).

## Choose the contribution

1. **Existing capability:** inspect `astrid.sdk.discover()` and
   `astrid.sdk.get_capability(...)`; compose what fits.
2. **Action:** expose a callable function under `actions/`.
3. **UI:** bind a contribution to a host under `ui/`.
4. **Rendering:** declare renderer support under `rendering:`.
5. **Shared library:** put private support used by contributions under `shared/`.
6. **No new pack:** keep one-off experiments in a run directory.

Declare public contributions in `pack.yaml`; a path alone exports nothing.
Keep implementation in the matching role folder. Reuse capabilities through
`astrid.sdk.invoke(...)`; do not open the Runtime database or invoke `run.py`.

## Write the pack's skills

Give the pack one main skill for its common workflow. Add a declared extra
when a distinct workflow needs separate instructions or should load only on
demand. Keep supporting details, examples, and assets in ordinary references;
they accompany the main skill but are not skill exports. Split content when it
would crowd the normal path.

The [Timeline pack](../../../timeline/pack.yaml) shows the pattern: its main
skill covers everyday edits; `series`, `narrated`, and `review` are extras;
helpers and other guides are references. The main skill is `docs/SKILL.md`.
Declare each extra as a `kind: skill` resource at `docs/<name>/SKILL.md`.
These five lines show two declared extras:

```yaml
resources:
  - kind: skill
    path: docs/series/SKILL.md
  - kind: skill
    path: docs/narrated/SKILL.md
```

The [main skill](../../../timeline/docs/SKILL.md) links to ordinary files in
`docs/references/` for editing details.

## Verify

Validate the manifest and paths using the pack guide. Confirm an agent can
discover the contribution, links work, and examples run as written. Run a
smoke invocation for runtime changes when Runtime and dependencies are
available. Regenerate the capability catalog when a manifest changes.
