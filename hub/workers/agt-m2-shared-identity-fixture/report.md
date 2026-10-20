I wrote the probe, but I haven't run it. My sandbox refuses Python, so nothing here is a measured result.

Run it with:
```
/home/user/work/venv-agent/bin/python -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-shared-identity-fixture/notes/probe.py
```
Exit code 0 means every intended check ran and passed. Exit code 1 means every check ran and at least one failed, which would be a real finding. Exit code 2 means the probe aborted or couldn't reach a check, and that is never a pass. Any typo or API mismatch in the untested code lands there.

The repo is untouched. Because nothing in it changed, I did not write a commit-msg file. Files:
- Probe: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-shared-identity-fixture/notes/probe.py`
- Report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-shared-identity-fixture/notes/report.md`

**What was wrong with the old probe.** `_validate_published_shot_payload` requires each shot item to have a string `item_id` and a `media_id`. The old probe's note items had no `media_id`. The new items follow the shape in Runtime's film fixture, with opaque metadata, and no validator was changed.

**What the probe does.** It runs three fresh temporary realms:
- **control:** nothing occupies the destination id. It checks that:
  - a dry-run leaves no trace;
  - the move is accepted and lands on the id the provider's bundle predicted;
  - siblings and the other timeline and project are untouched;
  - a retry replays;
  - reloading keeps the id stable;
  - a second move of the same occurrence onto its own id is valid;
  - the first move's pinned closure is preserved.
- **same-project:** before the move, a distinct valid shot with exactly the destination id is published in another timeline of the same project.
- **other-project:** the same, but in a different project.

For the occupied cases it classifies the outcome as a clean refusal, a refusal that still changed state, an accepted move that overwrote the occupant's shot, or an accepted move with no unrelated change. It reports two layers separately:
- **Physical projection:** the mutable shot row, items and head.
- **Immutable film:** the occupant timeline's pinned closure and history.

A projection overwrite is not called film corruption unless the second layer also changes.

**Hypothesis from reading the code, not a result.** `TimelineCommitStore._persist_closure` upserts the shot row by id, deletes and reinserts its items, and moves its head, without checking who owns the existing row. So I expect the same-project move to be accepted and overwrite the occupant's mutable shot while its pinned closure survives. The other-project case may be worse. The report has the details and an optional bounded fix, to be considered only if the run proves real data loss.

**Most likely things to break on the first run:**
- The shape of the dry-run and replay responses.
- Whether `shot_items.media_id` has a foreign key to media.
- The `publication_id` key name in the history entries.
