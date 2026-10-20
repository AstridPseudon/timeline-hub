Fixed all three findings within `tests/packs/rendering`. Adoption now requires locked PID/birth/own-child proof; replacement markers never become cleanup handles. Signal handling protects adoption, production retirement, and reaping. The helper is 218 lines.

Validation:

- Focused pytest: **25 passed, 3 deselected**.
- Central `real-pack-host-integration`: **3 passed, 25 deselected**—explicit stop, EOF, SIGTERM, and competing-CLI refusal.
- Ruff and whitespace checks passed.

`start_real_pack_host` now requires context-manager use to retain ownership across handoff. Full-suite, render/browser, and App-wrapper qualification remain unverified.

Updated the coordination page and both commit-message files. [Report with exact commands, SHA/tree, decisions, and limits](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-pack-helper-ownership/notes/report.md).

No implementation blocker remains. Next: owner review and harness commit. **M2 merges remain HELD until PLAN records M1.**