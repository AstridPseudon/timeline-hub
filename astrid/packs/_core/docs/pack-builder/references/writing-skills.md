# Writing skills

Use one main skill for the pack's common workflow. Add an extra skill when a
distinct workflow needs separate instructions or should load only on demand.
Keep details, examples, and assets that support a skill in ordinary references.

Declare the main skill with the pack's `documentation` pointer to
`docs/SKILL.md`. Declare each extra as a `kind: skill` resource at
`docs/<name>/SKILL.md`. A reference is an ordinary file linked from a skill;
do not declare it as a skill resource. The [Timeline manifest](../../../../timeline/pack.yaml)
shows one main skill and three declared extras.

- Put the recommended path first; explain exceptions after it.
- Teach one way to do each thing. Put alternatives in a reference if needed.
- Show a short example, then give at most one sentence of explanation.
- Explain each idea once, in words suited to the skill's reader.
- Move implementation details to references.
- Use short sentences, plain words, and consistent terms.
- Use tables only to show real choices.
- Keep each skill to one screen; move material that crowds it to an extra or
  reference.
- Check that every example runs as written.
