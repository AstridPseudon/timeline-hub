## Report — agt-G4-continuation-whole-path-1238

Read-only investigation completed. No product/test changes; worktree is clean. `DONE` and commit message were written.

### Causal verdict

- **Fork continuation:** Sol1221 fails because `_fork_shared_aliases()` emits a valid `occurrence.fork`, but the following patch reaches `State.shot_item_map()` with the new engine-created shot while `source_mapping` still describes the original shot. The strict guard correctly refuses it as `shot item source changed`.
- Sol1231’s `_command_state.py` fix correctly authenticates `_CopiedShot` provenance and passes focused controls, but real publication then fails in `_check_reservations.scan`: replayed fork births are reconstructed as plain dicts, losing `_CopiedShot`.
- **Exact unapplied fork seam:** the existing `astrid/sdk/timeline/commit.py::_check_reservations.scan` owner should apply the retained companion hunk:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-fork-continuation-sol-1231/evidence/unapplied-reservation-fork.patch`
  
  It reattaches authenticated `_CopiedShot` provenance immediately after replaying a recorded `occurrence.fork` shot creation. It remains unapplied and untested.

- **Duplicate continuation:** `duplicate_authoring_shot()` only mutates the detached candidate. `authoring_commit.py:102–104` rejects the new occurrence before any `capture_occurrence_duplicate()` reservation is consumed. The minimum production seam is therefore the existing authoring caller, before that closure-membership guard; helper-only wiring cannot solve it safely. This seam remains reserved until the active fork owner exits.

### Safeguards verified

Existing controls preserve:

- exact project/timeline and parent revision/content digest;
- authenticated source occurrence, source shot, source revision and verified closure;
- explicit destination identities and item-ID correspondence;
- untouched sibling physical identity, order, original shot/internal revisions and media manifest;
- strict foreign/stale/owner/source-pin/item-ID forgery refusals;
- duplicate source/order/history, equal-state and ABA protections.

No broad engine-ID exemption, equal-byte matching, caller map authority, or stale closure reuse is acceptable. The sourceSol focused test does not itself qualify the full production publication until the `commit.py` replay seam is applied and tested.

### Retained evidence

- Sol1221 retained failure:  
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-alias-source-sol-1221/continuation.xml`
- Sol1231 old/new/focused XML and exact unapplied patch:  
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-fork-continuation-sol-1231/evidence/`
- Luna1231 duplicate diagnostic:  
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-duplicate-command-1231/log.txt`

Retained results:

- Sol1221 production path: **4 failed, 19 passed, 1 deselected**.
- Sol1231 after `_command_state.py`: **4 failed, 19 passed, 1 deselected**, failure moved to reservation replay.
- Sol1231 focused fork controls: **8 passed**.
- Source controls: **79 passed, 1 deselected**.
- Luna1231 duplicate diagnostic: **73 passed, 2 failed, 3 deselected**.

No original tests, full suites, ABA body, network, acquisition, installation, or source execution were rerun. The stated R4 control-doc path was absent; matching `BOARD-HEADER.md` and `commit-v2.md` were read from `/home/user/timeline-hub/hub/design/`.