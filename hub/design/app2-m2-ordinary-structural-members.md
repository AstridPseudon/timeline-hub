# App AP2 M2 ordinary structural member

The App worktree now contains a bounded ordinary structural batch adapter in
`src/tools/video-editor/commands/ordinaryStructuralMember.ts` with its focused
test in `ordinaryStructuralMember.test.ts`.

It accepts only `track.add`, non-media literal `clip.add`, and `clip.remove`,
preflights all operations atomically, and emits native `track.create`,
`clip.add`, and `clip.delete` records in one reserved-ID ordered command array.
Raw membership/order selections, absent/present guards, authored writes,
bindings, created IDs, opaque row fields, sequential ordinals, and parent clip
mirror writes are retained. Projection copies only authored track/clip
collections and keeps display lanes immutable. Media aliases, selected/unknown
families, timing/source-window/transition shapes, nested ownership, and unsafe
dependency-bearing deletes remain refused.

Evidence: focused Vitest neighbours passed (4 files / 91 tests), a configured
Vitest probe matched the locked Agent `recipe_m2_clip_add.json` native
`track.create` + `clip.add` command array (1 test), and ESLint, TypeScript
no-emit, and `git diff --check` all passed. No full/browser/socket suite was
run. A direct standalone Node fixture comparison remains blocked by the
installed Composition package missing the `computeMediaTrim` export required by
the static projection import; the configured Vitest environment passed.
