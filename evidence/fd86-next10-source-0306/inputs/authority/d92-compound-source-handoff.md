# D92 compound source authority

This packet consumes the existing flat normal handoffs
`agt-F-D92-protected-review-0243.md`, `agt-F-D92-clean-join-0250.md`, and
peer return 0254.

- verdict: `PASS_SOURCE`
- normal home: Agent `562ee30b6e`
- reviewed blob: `113994232e2c21279967c3954811f095d9e7ffef`
- source SHA-256: `dd18f9bce71355a655413c6534c66300e29c2da1e42ff59bc3515b5727f8f634`
- selected originals: sequential-closure `[True]`, sequential-closure `[False]`, compound inverse
- excluded originals: atomic and ABA remain separate LIVE
- behavior: full `import_media` helper path remains unexecuted; MAIN3 remains open

The three selectors are recorded in `../selector-argv.txt` and
`../membership.tsv`. The earlier `f6d` ancestry is not imported.
