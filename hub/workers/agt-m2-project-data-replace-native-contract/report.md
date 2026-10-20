## Report

Implemented a private Agent candidate for bounded authored `project-data.write`:

- Added schema and registry support.
- Added native recording, inverse, rebase, ABA, opaque-key, and atomicity behavior.
- Added compiler-canary fixture and focused tests.
- Added design handoff: `handoff-ap2-m2-ordinary-projectdata-native-contract.md`.
- No new store, endpoint, public registration, or App changes.

Sources:

- [Project-data command]( /home/user/work/wt/agt-m2-project-data-replace-native-contract/astrid/sdk/timeline/_project_data_commands.py )
- [Schema]( /home/user/work/wt/agt-m2-project-data-replace-native-contract/astrid/core/timeline/schema/edit-command.schema.json )
- [Focused tests]( /home/user/work/wt/agt-m2-project-data-replace-native-contract/tests/editing_conformance/test_recipe_m2_project_data.py )

Tests:

- Focused pytest: `16 passed`
- Ruff check: passed
- `git diff --check`: passed
- Frozen union suite: `30 passed, 4 failed`, expected because the private candidate changes the frozen operation inventory; frozen tests were not modified.
- Full, Runtime, App/browser suites: not run per instructions.

Runtime schema/provider pairing and App migration remain for peer review and joint follow-up.

Commit message written and `DONE` created.