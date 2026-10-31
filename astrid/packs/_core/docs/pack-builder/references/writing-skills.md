# Writing pack skills

Write one main skill for the pack's common workflow. Add an extra when a
distinct workflow needs separate instructions or should load only on demand.
Keep supporting details, examples, and assets in ordinary reference files
linked from a skill. Split material out when it crowds the normal path.

Point `documentation` at the main skill, usually `docs/SKILL.md`. Declare
each extra under `resources` with `kind: skill` and its `docs/<name>/SKILL.md`
path. References are ordinary files; link to them from a skill, but do not
declare them as skill resources.

The [Timeline pack](../../../../timeline/pack.yaml) uses one main skill and
three extras: `series`, `narrated`, and `review`. Its editing helpers and
guides live in `docs/references/` and are linked from the [main skill](../../../../timeline/docs/SKILL.md).
This excerpt is copied from its manifest:

```yaml
resources:
  - kind: skill
    path: docs/series/SKILL.md
  - kind: skill
    path: docs/narrated/SKILL.md
```

- Put the recommended path first; explain exceptions after it.
- Teach one way to do each thing; put alternatives in a reference.
- Show a short example, then give at most one sentence of explanation.
- Explain each idea once, for the skill's reader; move implementation detail
  to references.
- Use short sentences, plain words, and consistent terms.
- Use tables only to show real choices.
- Keep each skill to one screen. Check that every example runs as written.
