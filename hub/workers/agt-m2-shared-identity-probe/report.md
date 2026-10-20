# agt-m2-shared-identity-probe — report

## Status: BLOCKED. The probe is written but was never run, so no bug is proven or ruled out.

Every attempt to run Python was refused with "This command requires approval". That covered `/home/user/work/venv-agent/bin/python -B <file>`, `python -B -c "print(1)"` and `python3 -B -c "print(1)"`. No approval path was available in this session. I did not use `dangerouslyDisableSandbox` or any other workaround: it is an override of the permission guard, and the task didn't authorize it.

**Nothing below is observed behaviour.** The static notes are leads, not findings. The worktree is untouched: I only read it, and the only files written are `notes/probe.py` and this report. I wrote no commit-msg file, because the repository has no changes.

## What exists

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-shared-identity-probe/notes/probe.py`

- **To run it:** `/home/user/work/venv-agent/bin/python -B <that file>`. It sets `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime` itself, so no environment prefix is needed.
- **Environment:** it builds a temporary realm under `/tmp` and removes it afterwards.
- **Stack used:** the real `RuntimeService`; the real Agent provider (`commit.create_runtime_commit_service()`, registered startup-only as in `tests/sdk/test_timeline_commit_provider_runtime.py`); and `capture_move` for the M1 occurrence `clip.move` (`occurrence:<id>/clip:<id>`). It uses no sockets and no invented receipts or provider.
- **Fixture:**
  - Project p1 has timeline `t-main`. There `shot-a` is shared by `occ-1` and `occ-2`, and `shot-b` has `occ-3`.
  - Project p1 also has timeline `t-alt`, with its own `occ-1` (the same occurrence id as in `t-main`) on `shot-a`.
  - Project p2 has timeline `t-other-project`, with `occ-1`/`occ-2` over `shot-x`.
  - Every internal timeline reuses the clip id `c1`.
  - Heads are built through the legacy publish path first, then reopened with the provider so baselines are installed.
- **Scenarios:**
  - **S1:** move `occ-1/c1`. It compares the sibling `occ-2`, the unrelated `occ-3`, the whole `t-alt` and p2 snapshots (head, canonical document, history), project shot heads, and duplicate stable IDs within the closure. `t-main`'s own history prefix is compared as well.
  - **S2:** move the same-id occurrence in the other timeline, then undo S1's move after the other timeline's activity. It checks that `t-main` is untouched by the other timeline's move, and that undo restores `occ-1`.
  - **S3:** re-move `occ-1`, then attempt to unshare `shot-a` through the Runtime API. This is the rematerialisation check.
  - **S4:** project isolation, probing duplicate timeline and shot ids across projects.
  - **S5:** a stub; it records SKIPPED and does not probe two shots carrying the same raw item id.
- **Reading the output:** `unchanged(...)` compares head, document and history. A FAIL status or any `dup_*` entry under `identities_after` would be the evidence of a collision.
- **Untested code:** it was never executed, so expect small API-shape fixes. The likeliest are `list_project_shots` row keys and the exact `publish_parent_composition` body fields. S1 and S2 do not depend on those.

## Static leads (not proven)

1. **Per-occurrence authoring identity.**
   - `authoring_bundle._authoring_shot_id` gives a shot that is used by more than one occurrence a hash id, `shot-placement-<sha(project, timeline, occurrence, source_shot)>`. A shot used once keeps its source id.
   - Shot item ids for shared shots are remapped the same way, including the timeline id. Cross-timeline item ids therefore can't match, even when the occurrence id is identical.
   - `open_authoring_bundle` also raises `independent shot identity collision` or `authoring shot item identity collision` if two distinct shots end up with the same id. If that happens, the user-visible effect is a refusal to open, not silent aliasing.
2. **Clip addressing is scoped by occurrence.**
   - History records use refs like `occurrence:occ-1/clip:c1`, so the reused clip id `c1` inside different shots should not alias.
   - `State.entity` raises `identity_conflict` if an occurrence id or clip id is missing or ambiguous.
   - `State.entity` handles `occurrence:o/shot` specially. It accepts only the source shot id or the exact materialised id.
3. **Possible rematerialisation hazard (S3), unconfirmed.**
   - The authoring shot id depends on share count: it is a hash while shared and the source id once a sibling is gone.
   - If the sibling occurrence is removed, history that recorded the hashed id could be compared against the source id. Whether this refuses or mis-targets is unknown.
   - The `matches()` special case only admits the exact materialisation of the original source. That points to a visible refusal, not a wrong-entity write.
   - The Runtime also refuses non-commit publication once a head is tracked (`timeline_commit_required`, `service.py` around line 3182). Removing a sibling may therefore not be reachable through supported M1 operations at all.
4. **Realm-global ids in the Runtime (S4).**
   - `create_timeline` rejects an existing timeline id across projects (`SELECT 1 FROM timelines WHERE id=?`, "timeline already exists").
   - `create_project_shot` does the same for shot ids (`SELECT 1 FROM project_shots WHERE id=?`).
   - Project isolation of these ids is therefore by global uniqueness, not by scoping. Two projects cannot hold the same timeline or shot id.
   - Scoping is enforced separately on reads and commits (`WHERE id=? AND project_id=?`).
   - This reads as a design choice. It would need an executable counterexample to become a finding, such as a cross-project read or commit by id.

## Decisions and recommendation

- I wrote no product, test or repository change. The shell would not let me run anything, so I did not claim evidence.
- Next step: someone with permission to run Python runs `/home/user/work/venv-agent/bin/python -B <probe>` and pastes the output. About 15 minutes of fixing for API-shape mistakes is likely. The most informative outputs are `S1` (`sibling_occ2_unchanged`, `identities_after`, the shot ids before and after) and `S3` (whether the unshare can happen at all).
- Alternatively, re-dispatch this task with Python execution allowed.
- Not covered by the probe:
  - A case where a shared-shot occurrence move itself publishes a new project shot or revision that needs a fresh stable id. S1 reports the shot ids before and after, so it would show up there.
  - S5 (two distinct shots carrying the same raw item id) is only a stub and records SKIPPED.
