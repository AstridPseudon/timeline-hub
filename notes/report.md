# agt-m2-position-set

Implemented the ordinary position family on existing version-1 `clip.set`.
M2 remains held.

- Published `/home/user/work/wt/agt-m2-position-set/design/m2-position-contract.md`
  before implementation with App mapping, units, API exports and golden path.
- Actual App position/updateClip writes are flat `x`, `y`, `width`, `height`;
  reset also removes `cropTop`, `cropBottom`, `cropLeft`, `cropRight`.
  Extended the existing closed args for precisely those eight numeric leaves.
- Existing handler already does the requested stable-ref, leaf-recorded writes
  and clears. Product Python change is one docstring line; no new handler,
  operation, normalization, bounds, timing policy or save dependencies.
- Tests cover App panel/update/reset golden, independent leaves/properties,
  same-leaf conflicts, tagged opaque/null/empty/ABSENT/expression restoration,
  full inverse/redo, occurrence isolation, dependency changes, unchanged writes,
  ABA, rational fps and unchanged compiled timing, unknown namespaces.
- Imported only the test helper and ordinary Runtime 0.2.3 frozen schema from
  `752c43ad55a588de2058ec85218b3f97ebe921b7` to prove schema containment.
  No item-pattern schema import. All 16 existing golden files are byte-identical.

Validation (from `/home/user/work/wt/agt-m2-position-set`):

```sh
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_clip_position.py tests/sdk/test_timeline_clip_position_provider.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_clip_scalar_provider.py tests/sdk/test_timeline_composed_schema.py
```

**316 passed in 18.42s.** Real provider via the suite's existing in-memory Runtime
ABI fixture; no sockets. Earlier development runs had new-test assertion errors
(1 failed / 271 passed, then 3 failed / 313 passed): a nonexistent compilation
attribute, revision-order comparison, and comparing newly published revision IDs
to bootstrap IDs. Corrected the assertions to compare compiled timing independent
of revision sorting and complete owner configs on reset. Exact canonical-document
comparison remains asserted for inverse/redo; no passing behavior tests changed.

```sh
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_clip_scalar_commands.py tests/editing_conformance/test_recipe_clip_position.py tests/sdk/test_timeline_clip_position_provider.py tests/sdk/command_schema_compatibility.py
```

**All checks passed.**

```sh
git diff --check
git diff --exit-code -- tests/editing_conformance/fixtures
git ls-files tests/editing_conformance/fixtures | wc -l
```

**Both diff commands passed; 16 tracked existing fixtures, unchanged.**

Decisions: follow the actual flat App/raw-schema mapping, including reset crop
leaves. Position-pane opacity is a separate property, outside the position/reset
family. Raw schema numbers have no ranges, so preserve negative/offscreen values,
zero/negative sizes and out-of-range crop fractions without clamping. Keep
Runtime-owned generated DTOs/lock untouched; the canonical JSON args are the
closed typed source of truth and must feed the next normal Runtime generation.

Blocked: none in this worker scope. No evidence contradicts the plan.

Not run: full suites, make check, Runtime/App suites, installs, network, browser,
localhost, or live socket tests, per brief. No commits, ref operations or pushes.

Next: manager reviews/integrates while holding M2; App consumes the absolute
contract and portable fixture. Runtime owner regenerates its existing closed
ClipSetArgs/client artifacts from the widened canonical schema during normal
cross-repo qualification. This worker does not claim cross-product qualification.
