PASS_SOURCE

- Reviewed `ef3d6c0b60c87601b6ba0adb415609e585d33e3e` against parent `6aefd11766c019f8deff0ca5a1bfe18e9e730822`.
- Confirmed only authorized setup changes: PNG → tracked `main.mp4`, `video/mp4`, `picture.mp4`; all timing, inputs, branches, assertions, guards, and retry/undo/no-write behavior remain unchanged.
- Verified MP4 blob `c54c64...`, 102,248 bytes, genuine ISO BMFF/H.264/AAC; `mvhd` duration is 42 seconds and `mdat` ends at EOF. Bounds covered: source end 6, move end 11/2, title end 6.
- Caller audit found no PNG or old-extent dependency. Service checkout contains the same blob.
- Static AST/compile checks passed; assertion and comparison node counts remain identical.
- Ruff candidate/parent: PASS. Mypy candidate/parent: PASS. `git diff --check`: PASS.
- No pytest, collection, helpers, services, ffprobe, or media execution run per brief. Behavior remains unqualified; meaningful MAIN3 is next.
- Used the available mirrored docs at `/home/user/timeline-hub/hub/design`; requested R4 docs path was absent.
- Wrote commit message and created `DONE`.