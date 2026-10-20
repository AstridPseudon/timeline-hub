The schema delta report is written to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-edit-schema-delta-for-runtime.md`. The DONE marker is created. The worktree has no changes and I wrote no commit-msg, as the brief asked.

## Findings

1. **Runtime's pin is behind Agent integration.** Runtime's `contract/schemas/edit-command.json` (sha `472622c4…aee9`) equals Agent commit `d4743e29`. It lacks `placement.create`, `placement.unplace` and `occurrence.duplicate`, which are already on Agent `tl/integration` (`408f3ba3`). So one release regenerates six ops, not three.
2. **The three pending ops are purely additive over integration.** `clip.set-element`, `shot.set` and `shot.pool` each add one op branch and one or two `$defs`. Nothing existing changes except appending to `EditCommand.allOf`.
3. **No conflicts.** Each branch's parent is integration's schema (`429283b2…`). A textual 3-way merge exits 0 for all three, and the defs have unique names.
4. **Union file sha256: `48becd142070d3336868b2aa7716a372034594b4c8822e816a3a036a69ad02bc`.** This is a scratch merge, not a committed branch. Agent still has to commit the same bytes for Runtime to pin them byte-for-byte.
5. **No Runtime port, validator or DTO code change is needed.** Command meaning comes from the Agent provider, and Runtime has no op-keyed logic. The only Runtime work is regeneration plus the manifest update. `shot.pool` uses the existing `selected_media` port call. `shot.pool` add also records a `created` asset identity, which Runtime stores generically.
6. **Runtime's compatibility check passes** against the `runtime-0.2.3` floor for integration and for the union (0 errors).

I regenerated Runtime's artifacts by running Runtime's own generators on a scratch copy. On the current pin they reproduce the tracked files byte-for-byte, so the new hashes are trustworthy. The report has the full table for the four artifacts that change: the schema file, the bundle, the Python types and the TS types.

## Decisions for you

- **One release covering all six ops.** Regenerating only the three pending deltas would leave the pin behind integration.
- **`ShotSetArgs` shape.** Its `anyOf` makes the generator duplicate the object into two near-identical variants. The output is correct but verbose. Any Agent change to it changes all the hashes, so decide before regenerating. I recommend keeping it.
- **Compatibility floor.** At release, add a `runtime-0.2.4` fixture, add it to `sources.json`, and advance the floor, per the `generate.py` docstring. I did not apply this.

## Not verified

- I did not run Agent's suites or Runtime's test suite. I only ran read-only git, structural diffs, the textual merge, Runtime's generators on a scratch tree, and its compatibility function.
- I did not check whether `runtime_protocol/timeline_commit_types.py` is covered by `scripts/artifact_manifest.py`. It is not listed in `contract/artifacts.json`, so check it before release.
