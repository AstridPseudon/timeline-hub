## PASS — agt-P4-facade-final-port-0416

Ported the exact committed `Timeline.undo` facade and `tl.undo(...)` caller-test delta from donor `9fbb84ac89c3bd5e6c7ef5e38dc3f0fed243226f` onto base `38b72402e485d4049eafd50179dcbf570b6f4be5`. Only `astrid/sdk/timeline/commit_session.py` and `tests/sdk/test_timeline_open_commit_v2.py` changed; both resulting blobs match the donor exactly. The five P4 donor test blobs inherited from base are untouched.

Evidence: P4 SDK **15 passed**; public sync/open-commit plus inverse-schema controls **107 passed**; local numeric undo controls **2 passed**; Runtime HTTP gate **1 collected only** with no body execution; scoped Ruff/private mypy, normal Ruff ratchet (**2149/2149**), normal mypy ratchet (**1915/1915**), artifact manifest, vendor lock, and diff checks passed.

The broader checkout diagnostic has four inherited failures in unchanged boundary assertions; they are reported in the worker report and do not block this scoped port. No HTTP body/full suite/browser/live socket was run.
