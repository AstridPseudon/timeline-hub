# Runtime OPS-retire-venv-v2 fixture reconciliation — 1745

**PASS — fresh private acceptance complete; independent review required. Evidence only, NEVER MERGE, do not install here.**

The predecessor fixture positives now use actual maker source names. Product guards are unchanged: staged handler `a500d2a1`, request `44c61283`, dispatcher `f18bc20b` are byte-identical to 1735. The installed scripts remain `48cac6c7` / `4713b456` / `f18bc20b` before and after.

Fresh results: syntax 3/3; actual adapted guard 37/37; actual adapted unit 7/7; unchanged author 17/17; extra controls 8/8; request writer → exact dispatcher branch → handler 3/3, repeated under `env -i` 3/3 with real process visibility. Old unadapted 37=36/1FAIL and 7=6/1FAIL logs remain preserved and were freshly reproduced, not relabeled.

Only obsolete positive source-name literals changed. Python whole-AST comparison and shell whole-source reversal verify all assertions remain intact. Actual unit source used `-completed`; the shell used `-running`. Separate negatives prove both obsolete names and the exact shell counterpart refuse without target/source/queue mutation. Valid young source retention and stale source retirement remain positive. No skip, xfail, assertion deletion or refusal substitution.

The actual 1534 shell source and the 1740 durable 37-case body differ by an already-settled source-custody positive plus retention assertion; the packet records their complete diff instead of claiming they were identical. No absent guessed harness needs recovery.

Runtime `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` stayed clean; all full v2 request/reply/history/canonical and frozen 34e artifacts remain unchanged. No full/product suite was run. Replacement-race coverage here retains predecessor structural assertions; this is not a new dynamic race-injection qualification. Host installation/daemon behavior remains unverified.

Exact scripts, installed-base patches and source/fixture hashes are adjacent with prefix `handoff-runtime-OPS-retire-venv-v2-fixture-sol-1745-`. Dispatcher patch is empty. Every executable test command and exit is in the [detailed report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-venv-v2-fixture-sol-1745/detailed-report.md) and [command transcript](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-venv-v2-fixture-sol-1745/evidence/commands.json). Canonical kit: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-venv-v2-fixture-sol-1745/evidence/kit`.

Next: independent Luna review, then HOST idle/callshape/backup/atomic-install/publication. Prior permission refusals remain stopped; no production cleanup or retry occurred.
