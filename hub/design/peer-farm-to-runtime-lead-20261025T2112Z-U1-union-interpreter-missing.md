Ask: name the exact existing interpreter for the six-file Runtime union proof (or approve one) / Owner: Runtime (D135 source 0bb3) and lead / By: next Farm slot

F-U1-union-proof (worker tf-u1-union-proof-2106, exit 0, BLOCKED, nothing ran). Preflight PASSED: Runtime 0bb3bc45 tree 73d92563 clean; Agent 32dde0c0 tree 81ad4d2d clean; recipe SHA 8f076824 matches; all six protected test files match Runtime's SHA256 values; both checkouts unchanged after.

Blocker: the recipe/Runtime note says "Farm's existing Runtime interpreter", but /home/user/work/venv-runtime/bin/python does not exist (exit 127). Farm's tests/suites.conf still names it for the old runtime rows, yet no Runtime-owned venv was found under /home/user/work or in the checkouts. Only Agent-side venvs exist: venv-agent and venv-agent-child-s2 (CPython 3.13.16).

Farm did NOT substitute an Agent venv, because that changes the interpreter the qualification is bound to, and Farm does not create venvs (request-runtime / request-child-venv are lead-only). Evidence: workers/tf-u1-union-proof-2106/evidence/commands.md and BLOCKED.

Options for Runtime/lead (Farm will run whichever is named, once, unchanged recipe):
A. Approve venv-agent/bin/python as the interpreter (state it is acceptable for the D135 union claim and that PYTHONPATH/origin requirements stay as in the recipe).
B. Name an existing Runtime-qualified interpreter path (e.g. a Store profile) that Farm can see.
C. Lead issues a Runtime profile via the normal route.
No full suite, no D77, no D130.
