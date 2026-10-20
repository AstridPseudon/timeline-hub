The audit is written to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-area-size-and-ledger-audit-0905.md`, and the DONE marker is created. No repo files were changed and no commit message was written.

## Results

**1. Size (Agent HEAD 931d7ec5).** Product Python in the requested paths totals about **41.7k lines** in 132 files: sdk/timeline* 19.9k, packs/timeline 7.0k, core/timeline 14.8k. That is about 1.6–2x the whole-product PLAN target of 20–26k, and it is an upper bound. `tests/editing_conformance` is 47.9k lines: 11.3k Python in 44 files and 36.5k JSON fixtures in 26 files. Physical line counts, not PLAN "authored" lines. The top 15 files are in the report. The largest is `packs/timeline/cli.py` at 4,067 lines.

**2. Deletion ledger.**
- D05 and D06 are consistent. Their code is gone, their commits are ancestors of HEAD, and all named replacement tests exist.
- D06's note "not physically merged" is stale.
- No row is "DELETED but present" or "held but gone."
- Rows with no replacing test named: D07, D13, D01a/b, AG01–03, WC1, WC2 (only test callers), and WC9.
- Several WC rows have wrong paths or drifted line numbers. D13 points at `astrid/sdk/generic_host.py`; the real file is `astrid/core/execution/generic_host.py`. WC7 cites `tests/test_timeline_publish_connection.py`, which lives at `tests/sdk/`. WC9 names `document-checkout.md`, which does not exist.
- WC10 is missing several Agent-side `publish_parent_composition` callers.

**3. Dead code.** I found no provably unimported product module. The first-pass scan's 0-importer hits (`cli_working`, `moments`, `text_fit`, `arrangement_rules`, the events payloads) are all live through indirect imports I checked by hand. The deletion candidates for M4 are legacy surfaces inside live modules: the `timeline_checkout.py` re-export shims, `timeline_editing.py` retime helpers (D07), and `shot_composition_migration.py` after WC10 callers move.

**4. Second writers and history paths.** The report lists `file:line` for every `publish_parent_composition` caller, the whole-candidate writers, the whole-document checkout publish, and the direct text-binding writers. Two legacy history paths also remain: the whole-file local undo/redo in `checkout.py:160–258` (reached from `cli.py:_cmd_undo`), and sheet restore from local history in `timeline_sheet.py:621–638`. Publication-undo in `sync.py:261` is the command path and is not a duplicate.

## Unverified and open
- **Corrected dead-code rerun did not finish.** I stopped waiting on it. The report marks section 3 as based on manual checks of the first pass. The scanner process (`scratchpad/deadcode.py`) is still running. My attempt to kill it needed approval and was not run, so it is still alive and writes only into my scratchpad.
- I did not verify the App and Runtime halves of D01 and D13.
- The `ReadNotifications` and monitor waits did not produce a completion event for the rerun.

The audit report is finished at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-area-size-and-ledger-audit-0905.md`. The DONE marker is in place. No repo files were changed and no commit message was written.

The corrected dead-code rerun finished. Its zero-importer list matches my manual checks: only package `__init__` files and the events payload modules reached through `events/schema/__init__.py`. So no product module in the area is provably unimported at HEAD.

## Findings

- **Size:** about 41.7k product lines in the requested paths, against a whole-product target of 20–26k. That figure is an upper bound. `tests/editing_conformance` is 47.9k lines, mostly JSON fixtures.
- **Deletion ledger:** D05 and D06 are consistent. Their code is gone and their replacement tests exist. D06's "not merged" note is stale, since its commit is now an ancestor of HEAD. Several rows name no replacement test: D07, D13, D01a/b, AG01–03, WC1, WC2, and WC9.
- **Ledger paths:** several rows have wrong paths or drifted line numbers, and WC10 is missing Agent-side callers. The report lists each one.
- **Second writers and history:** the report lists `file:line` for every `publish_parent_composition` caller, the whole-candidate and whole-document publishers, and the direct text-binding writers. Two legacy local-history paths remain: whole-file undo/redo in `checkout.py` and sheet restore in `timeline_sheet.py`.

## Limits

- The importer scan is text-based. It can miss dynamic loading that is not written as a module path.
- I did not verify the App and Runtime halves of D01 and D13.
- A scanner process from an earlier run may still be alive in my scratchpad. My attempt to kill it needed approval, so I left it. It writes only into my scratchpad.

The dead-code rerun finished earlier and its results are already in the report, so the expired monitor needs no action. The check above only matched its own shell, so no scanner process is still running.

The report is final at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-area-size-and-ledger-audit-0905.md`, and the DONE marker is in place. Nothing in the audit has changed since my last message.
