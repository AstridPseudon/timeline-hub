Implemented F-authoring-ABA diagnostics on Agent base `d33fe5f9f0e69d874ff60fe1ea513fc3bbe11190`.

Changed only [test_authoring_item_observation_boundary.py](/home/user/work/wt/vw-F-ABA-diagnostics-0744/tests/editing_conformance/test_authoring_item_observation_boundary.py):

- Native current-site accept/preview: refusal expectations → positive authenticated range validation.
- Historical native spelling: now expects the earlier `shared inverse native captures differ from authenticated history` refusal.
- Ordinary shared-media accept/preview: old refusal expectations → positive boundary validation, retaining target-only restoration and sibling/root edge checks.

Runtime source used: `460c2d397e9beb052a5d03d70123ba8776f22d01`, tree `c026c3e486c03513a90176550f26befd74bde4ea`; module paths resolved from the immutable archive.

Checks:

- Targeted pytest: `95 passed`
- Ruff: passed
- Mypy: `Success: no issues found`
- `git diff --check`: passed
- Original oracle file byte-identical; no product or Runtime changes.
- Completion marker and conventional commit message written.