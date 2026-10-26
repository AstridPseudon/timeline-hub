# F D141i Farm artifact publication validation

## Acceptance checks

| Check | Result |
| --- | --- |
| Exact physical schema directory, no-follow, mode | PASS; physical directory, 0755 |
| Schema RECORD closure | PASS; 18 unique rows, 12 hashed rows, six approved unhashed rows |
| RECORD content hash | PASS; `844b2a2e1ee19d7a1656d57cb49c2bc8febf67295e653f93ff8f96217a0c7220` |
| RECORD file existence/regularity/hash closure | PASS; every row is a regular non-symlink file and every hashed row matches |
| Private direct_url binding | PASS; 254 bytes, 0644, SHA `b7a0a4f90218d54bc1fb118609d40a381f5762650f8e5863ec39098ec269165e` |
| D139a source identity | PASS against approved URL, commit, subdirectory, and source-tree values |
| Trusted manifest physical availability | NOT READY; approved canonical identity is known, but no standalone physical producer file exists |
| Original 2149 census | PASS on source venue; 10,686,270 bytes, 0644, regular/no-follow, SHA `be9e8bc9c6d2411809da2d99126a9b3eef72678de2066bb6ad196d5d16ebcd30` |
| 2216 relationship | PASS; finite reconciliation retained as supporting provenance only |
| D139a installation receipt | PASS as source evidence; 3,587 bytes, 0644, regular/no-follow, SHA `82bdfab2c3ec483261126b3446aacf7d1ee9df6d38e1c2491b33e3927c60f5a4` |
| Current Farm kit summary pair | NOT READY; summary missing, so receipt is not promoted to Farm closure |
| Original67 wheelhouse | NOT READY; no physical wheelhouse found |
| Bootstrap exclusion | PASS; bootstrap archive was identified and excluded, not unpacked |
| Source-only shell/AST/diff checks | PASS; see `commands.md` |
| Full/97-control tests | NOT RUN by task scope |

## Integrity notes

The exact schema RECORD mismatch in `venv-agent-child-s2-c13` and
`venv-agent-child-s2` was a stop condition for those candidates; neither was
used. The installed `venv-agent` closure passed. No source-only evidence was
silently treated as a Farm-bound input, and no output contains raw private
direct_url content.

The 10,686,270-byte census is below the 50 MB split threshold. No split,
archive, ZIP, build, or alternate transfer route was invented.
