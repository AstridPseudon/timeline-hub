# Root-preparation lifetime extraction

Completed on `tl/vw-m3-root-prep-lifetime-extract`, base `4ef1391c2`; no Git mutation or shared dependency writes. Harness commit message is ready.

Extracted the EXISTING preparation/cleanup block from `_execute_remotion_locked` into private `root_preparation._prepared_remotion_root`. Renderer launch stays in `run.py`. The context yields existing local values in a plain tuple, avoiding a new DTO/API/factory. Existing backend admission/staging/PCM functions remain bound on `run.py`, preserving patched callers and normal authority. No SDK publish/transaction or package-pin edits.

The complete validation, native-window/source/profile, original clips/extent, theme/alpha, managed assets/server, ExitStack, effect staging, normal PCM, props serialization/callback and cleanup sequence is retained. An AST comparison proved admission/preparation/cleanup and the renderer continuation identical after normalizing only the helper's backend-qualified names; yield is the new boundary. Read-only queries hold real resources inside the context and never imply a successful capture or force renderer launch. Exact signature, yielded tuple, locking contract and lifetime are in `viewing-agent-d09-root-prep-handoff.md`.

One necessary adjacent line adds the helper to the existing frame source fingerprint; tests prove changing either `run.py` or the extracted helper changes the frame key. There is no cache-row or D09 deletion work here.

## Validation

All exact commands and full central commands/results: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-prep-lifetime-extract-commands.txt`.

- Correctly provisioned existing targeted lane BEFORE extraction: **208 passed, 37.38s**; AFTER extraction: **208 passed, 37.95s**. Covers Root props/callback, native windows, source joins, Scene labels, PCM and cleanup.
- Expanded direct lane, adding context success/exception/KeyboardInterrupt, PCM lifetime, fingerprint and import-fence cases: **225 passed, 39.55s**.
- Final type-only `cast(Path, cli_video)` preserves existing validation and resolves a scoped mypy inference error. Rechecked new context/fingerprint cases: **11 passed, 5.31s**.
- Central final source tree `tree=e2ac895d16ab205221358aeee9b8540f57f71779`: **82 passed, 63.83s**. Service ID `1020133642-9871`; named suite `integration-viewing-normal-pcm-http-final-current` plus selected existing backend/lock tests. Includes real HTTP/PCM phase checks using the literal private project path; excludes the four browser/real-render tests under this task's no-render grant. Earlier tree also passed 82; final re-run was required by the type-only correction.
- New helper and direct lifetime tests: **Ruff passed**. Existing touched-file Ruff finding counts exactly match HEAD; no baseline edits. Scoped helper mypy: **passed** (`--follow-imports=skip --ignore-missing-imports`); this is not a whole-repository typecheck. `git diff --check`: **passed**.
- Full suites, browsers, rendering/pixel/audio parity, SDK explicit-check integration: **not run or claimed**.

Initial unprovisioned test attempt failed (18 failed / 135 passed / 55 errors) because the Node graph and PCM project environment were absent; correcting environment paths gave the before/after green results. No tests were weakened, skipped or disabled.

## Inventory and remaining gates

The brief's 1,696 count is stale for this actual base: `run.py` had **1,929** physical lines and its rationale recorded **1,851**. Extraction reduces it to **1,797**; helper is **210** lines. Because shrinking made the old record differ by 54, only the owned rationale entry is updated to the actual count, with the extraction reason. Both **1,200/50 thresholds are unchanged**. Against actual `origin/main`, `run.py` is 1,868 → 1,797 (−71); main-versus-current diff is in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-prep-lifetime-extract-main-diff.diff`. No unrelated main feature was cut.

The normal whole inventory test still fails on the separately owned **service.py 2,367 versus recorded 2,314** (+53), as already noted in the Viewing inbox. The owned run.py row passes the unchanged rule exactly. The import-cycle command also fails on existing core **rendering ↔ timeline**; no `astrid/core` file differs from HEAD, and the checker defaults to that core graph. These repository-wide blockers are reported, not changed outside scope.

This worktree actually pins Composition **0.0.12**, despite the prior shared note's “official013” statement. No pin adoption or 0.0.13 qualification is claimed. The tested private source is the existing PCM project path recorded in the commands.

## Handoff

Review/apply the patch, then have Agent consume this exact private context under the existing Remotion lock for its explicit Scene check. Keep Scene/save separation and D09/cache deletion behind their independently required qualification and physical parity. Finish the separate service inventory correction before claiming the inventory gate green. Nothing blocks review of this extraction itself.

Files: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-prep-lifetime-extract-files.txt`. Patch including new helper: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-prep-lifetime-extract-patch.diff`. Shared exact seam: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/viewing-agent-d09-root-prep-handoff.md`. Commit message: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-root-prep-lifetime-extract/commit-msg`.
