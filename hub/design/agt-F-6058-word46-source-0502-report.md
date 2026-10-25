## Report

Changed [native_word_anchor_fixture.py](/home/user/work/wt/agt-F-6058-word46-source-0502/tests/editing_conformance/native_word_anchor_fixture.py) so the subprocess reuses the parent-selected current Runtime/provider instead of incompatible historical Runtime `80973d34` (3 ops vs current 30).

Preserved all seed data, media bytes/MIME, transcript words/IDs/pins, timing/FPS, topology, assertions, and original tests.

Checks passed:

- In-memory compile: parent/candidate
- Ruff: parent/candidate
- Mypy: parent/candidate
- AST/predicate conservation
- `git diff --check`
- Safe packet: 37 word + 9 next-cohort selectors, request `agent-fd86-current96-body-0415-1025041953-6058`

No pytest, fixture execution, imports, services, or MAIN suite run per SOURCEONLY constraints.

Protected independent review and meaningful MAIN46 proof remain pending downstream. Commit message and `DONE` marker created.