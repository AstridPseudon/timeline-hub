## D128 report

- Completed read-only source diagnosis; no product or kit changes.
- Finding: the refused request followed the no-seed direct source-install branch. Setuptools `egg_info` is the smallest source-proved generator for an extra retained `.egg-info` directory.
- Actual offending path and retained tree: `EXACTMISSING`; candidate paths remain inference only.
- Compared canonical maker, authenticated Agent/Runtime archives, and Farm census source. Archive directory shape was clean.
- No child retry, build, Farm census execution, provider/full suite, or permission/ownership change.

Evidence:

- `evidence/wholepath.json`
- `evidence/source-manifest.json`
- `evidence/validation.md`

Validation commands:

- JSON parsing: PASS
- SHA-256 identity checks: PASS
- Static AST/source checks: PASS
- Authenticated archive parent-closure checks: PASS
- Worktree clean: PASS
- Product tests: not run; prohibited by task scope.

`DONE` marker and conventional commit message were created.