## Report

Classification: actual Runtime source bug at the Runtime–legacy ABI1 seam. Not fixture misuse, environment, or the legacy-inverse child.

Both failures submit forward `track.create` commands without `created`:

- `stable-track`
- `historical-track`

Agent’s recorder derives:

- `record["command"]["created"] = ["parent/track:stable-track"]`
- `record["command"]["created"] = ["parent/track:historical-track"]`

Runtime e68 then compares `submitted.get("created", [])` with the recorded value in `timeline_commit_auth.py:290–299`, producing `invalid_records: provider executed a different command`. The inverse exception is correctly inapplicable.

Proof:

- Agent diff from `47b744dfe9` contains only the `_commit_patch.py` inverse condition; it is false for these ordinary forward commands.
- Runtime e68 and becfe have identical `timeline_commit_auth.py` SHA-256: `e172f8c5…dcccb70`.
- Runtime auth was introduced by `9975596`; the affected tests predate it.
- The row `opaque`/`unknown` fields are valid extension data.
- The same production `RuntimeService.commit_timeline` route and provider factory pass the v2 provider controls.

Minimal owner fix: Runtime/Sol consumer should preserve ABI1 omission of `created` for forward commands while retaining core command equality, explicit nonempty claim checks, records, writes, reservations, and all other guards. No Runtime change was applied per task restrictions. No Agent hunk is justified.

Tests/evidence:

- Retained targeted run: `2 failed, 2 passed, 34 deselected`; both named failures had the exact Runtime traceback above.
- `git diff --check`: passed.
- Runtime/Agent source and hash comparisons: passed.
- Original test bodies were not rerun, per instruction.
- No matching XML artifact was retained; classification uses the exact retained log plus source/request/record reconstruction.

Worktree has no source changes. Commit message written and `DONE` created.