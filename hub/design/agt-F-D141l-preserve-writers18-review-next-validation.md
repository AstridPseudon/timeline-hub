# Validation record

All work was read-only against frozen Git blobs and supplied XML. No product source, tests, providers, imports, generated files, pins, Git refs, shared dependencies, request-test run, browser, live socket, or full/heavy suite was used.

1. Author's same checker, run from this review's isolated `evidence/ownchecker` output directory:

   `cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-preserve-writers18-review-next/evidence/ownchecker && python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-preserve-writers18-1104/evidence/check.py`

   Result: exit `0`, `result=PASS`, exact assigned packet membership `18`, no checker failures, all 18 pristine and current XML statuses `PASS`. The checker is read-only; its terminal output is retained in the review transcript and the command record is in `ownchecker/run.txt`.

2. Independent frozen-Git/AST/XML comparison:

   `python3` read `ROWS` from the author checker, loaded each source with `git show <ref>:<path>`, parsed the pristine/current functions with `ast`, hashed function bodies and assertion nodes, and parsed both XML files. Result: 18 assigned rows; 3 exact body+assertion matches; 15 non-matches; 18 pristine `PASS`; 18 current `PASS`; current counterpart IDs unique count `17` because rows 12–13 share one generic test. Source and AST details are in `map.json` and `source-manifest.json`.

3. JSON syntax:

   `python3 -m json.tool` on `review.json`, `map.json`, `restoration-manifest.json`, and `source-manifest.json` — all passed.

4. Raw XML hashes:

   Cut `6710f7fe1b4b1a0b4d43614f0fe58d437b0b6fff76990e4a717022cef773fcd5`; pristine `9d36fcecf662cc9138cd30cb6ad674a57db30209b18593f29da08ed961792bba`.

5. Sustained disk trace:

   Six one-second terminal samples ran before review work. Available bytes ranged from `7392407552` to `7392411648`, always above the `4000000000` stop threshold. The trace is in `disk-trace.txt`.

6. Product worktree:

   `git status --short --branch` remained clean. This task made no repository changes.
