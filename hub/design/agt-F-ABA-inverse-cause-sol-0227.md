Classification complete. **No worktree changes; original ABA remains FAIL** at undo (retained run: **22.92s**). All **59 oracle assertions** remain unchanged. Commit message and `DONE` were written.

- Read-only verification of the retained realm proves the undo base equals the published head. This is **not a stale-base replay**.
- The absent shot/internal inputs match the accepted source carrier’s command-0 output and command-1 input exactly. Runtime `8ea0766f` is the authoring source; `a0dca169` supplies only the seed constructor.
- Offline execution of the retained undo produces the **exact baseline closure**, but supplies **zero private captures**.

The earliest source candidate is [`_commit_patch.py:593`](/home/user/work/wt/agt-F-ABA-inverse-cause-sol-0227/astrid/sdk/timeline/_commit_patch.py:593): it emits materializations for successive inverse stages using the outer command’s input boundary. Later-stage roots therefore appear outside that input. Separately, line 472 excludes single-command execution capture, causing [`_commit_preview.py:30`](/home/user/work/wt/agt-F-ABA-inverse-cause-sol-0227/astrid/sdk/timeline/_commit_preview.py:30) to return immediately.

**A capture-only fix is insufficient:** an offline six-key, one-command carrier still fails `provider sequential command output differs from its authenticated projection`. The sole projection difference is parent identity: canonical `wc6-baseline` versus projected `authoring-parent-revision-431f8acb1e1251a6e1e0b97707803a30a7e8fcb7d5b96ae42b1a60d78c53c08f`.

No `inverse.py` execution change is justified. Root-inverse0227 should preserve its sequential reversals, source boundaries and native/effect ranges. The next implementation owner needs `_commit_patch.py` projection scope; the permitted `commit.py` seam cannot independently resolve this. No Runtime guard relaxation is proposed.

Validation used the supplied qualified environment:

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 tests/editing_conformance/test_private_sequential_capture.py tests/editing_conformance/test_provider_step_undo_v2.py tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_materialized_whole_payload_read_allows_exact_undo_redo tests/editing_conformance/test_recipe_occurrence_media.py::test_same_alias_materialized_payload_still_guards_all_other_input
```

**34 passed in 24.80s.**

Additional exact commands and results:

- Qualified Python `/tmp/w-0ec4a892fe/retained_probe.py`: authenticated retained history; exact baseline candidate; missing capture reproduced.
- Qualified Python `/tmp/w-0ec4a892fe/verify_retained.py`: exact intermediate-source matches; capture-only refusal confirmed.
- Qualified Python `/tmp/w-0ec4a892fe/source_controls.py`: authentic source carrier and inverse partitions passed; **11 corruption controls refused**.
- `python -m ruff check --no-cache astrid/sdk/timeline/commit.py astrid/sdk/timeline/_commit_preview.py astrid/sdk/timeline/_commit_patch.py`: passed.
- Private typecheck Python `-m mypy --cache-dir /tmp/w-0ec4a892fe/mypy-current` on those three files: **zero diagnostics**. Files equal HEAD exactly.
- `python scripts/vendor_lock.py check runtime.lock.json`: passed. Adding `--producer /home/user/work/wt/rt-pin-8ea0766f` failed the existing **34e/8ea pin mismatch**; pins unchanged.
- `python scripts/artifact_manifest.py --check` and `git diff --check`: passed; worktree clean.

One exploratory original-side effect-**before** mutation alone was not rejected by the capture validator. Its intended semantics and durable acceptance remain unverified; it is not pass evidence.

Next: resolve stage projection and authenticated parent reuse together, retain strict controls, then let the manager run the **one changed original service test**. No original-body rerun, service startup, full suite or shared-environment mutation occurred.