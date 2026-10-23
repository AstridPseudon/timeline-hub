# G5 publish idempotency fixture handoff

Worker: `agt-G5-publish-idempotency-1612`

PASS: exact joined G5 blobs plus a fixture-only Runtime idempotency model produce 76/76 passing tests. The same scoped key/request replays the original result and receipt without a second write; a changed body under the same key is refused before transport with unchanged realm state. The additional G3 frontdoor suite is 12/12 passing.

See the complete command, hash, mypy-baseline, and scope record in [worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-publish-idempotency-1612/report.md).

Only these assigned test files are changed. No product or shared dependency changes; no full/P1-P4/HTTP/browser/native suite was run.

