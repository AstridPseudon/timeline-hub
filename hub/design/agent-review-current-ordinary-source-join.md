# Agent current ordinary-source join review

## Verdict

**APPROVE** the read-only review of merge `ee896821b502ee4e51211b19d064fa44915f5777` (tree `aa0b15850d4b777b77f54faec189cf7e4c60a7b6`).

This is a two-parent merge of current integration `30fc8dd154015a7c58cf4ce7b065ccc46f470ee8` and frozen ordinary parent `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`. Both parents are ancestors of the target. No source, branch, index, Runtime, App, Composition, or public pin was modified by this review.

## Join findings

- The merge delta from current is limited to the reviewed ordinary Agent source, fixtures, and tests: schema, SDK timeline command/recording/commit/inverse paths, native initialize/occurrence/parent-media/text/word-anchor paths, media replacement, and their conformance tests. No Runtime/App/Composition source was added.
- Current P1/WC4/F1/Scene/Root/service/Sprite/Plate/docs paths remain byte-identical to the current parent where they do not intentionally overlap the ordinary source. In particular `_selected_param_authority.py`, `check.py`, `publish.py`, `store.py`, `transaction.py`, `timeline_elements.py`, `timeline_duplicate.py`, `workspace_client.py`, rendering service/window extraction, Sprite/Plate sources, architecture/docs, `runtime.lock.json`, and `artifacts.json` are retained.
- The public generated client/pin and Composition `0.0.12` artifact are unchanged: `astrid/sdk/workspace_client.py`, `runtime.lock.json`, `requirements/runtime.lock`, `artifacts.json`, and `remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz` match current parent.
- Schema is byte-exact: SHA-256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, with 55 definitions and 29 operations. No private carrier/audio schema or unreviewed WC3/WC6/D13 consumer logic was introduced.
- The two `commit.py` joins preserve current selected-parameter authority and add the ordinary inverse-aware source hydration at both initial and stale-head replay sites. `_inverse_clip_transcripts` only removes authenticated first-use transcript pins for removed created clips; `_hydrate` admits restored pins only from authenticated inverse closures. The reservation replay retains the current root-birth/source marker behavior.
- Duplicate F1 hunks were removed without dropping current behavior: every existing F1 test body in the selected-param, selected-schema, selected-schema-runtime, and clip-element test files is present with identical AST body and assertion count in the target. The target/current comparison found no missing test functions or changed existing test bodies.

## Tests

All tests ran from this worktree with `/home/user/work/venv-agent/bin/python`, `PYTHONPATH` set to the worktree, `PYTHONDONTWRITEBYTECODE=1`, and `-p no:cacheprovider`. No full or full-* suite was run.

- `tests/editing_conformance/test_recipe_scalar_commands.py -k 'inverse_'`, parent auto-completion, native text binding, pristine initialize: **18 passed, 205 deselected**.
- Current F1/selected-param unit lane (`tests/sdk/test_timeline_selected_param_authority.py`, legacy alias inverse, clip-element, scalar inverse/authority/disjoint/birth selection): **43 passed, 90 deselected**.
- Schema/source floors and parent-media completion/literal subset: **43 passed, 76 deselected**.
- Private normally generated Runtime selected-PARAM/F1/legacy-alias native lane: **32 passed**.
- Private normally generated Runtime birth + text joint inverse/redo/reopen/retry lane: **2 passed**.
- Private normally generated Runtime parent auto saved/fallback/stale-read/zero-write lane: **14 passed**.
- Media manifest inverse add/swap lane: **2 passed** using a temporary private extraction of the exact historical seed commit `b2a1d9fd82121a5509769531a2e91aece97d78b` from `/home/user/work/runtime`, while keeping `ASTRID_RUNTIME_CHECKOUT` on the private normally generated 55/29 Runtime fixture.
- `git diff --check`: clean; target worktree remained clean.

The first media retry with the literal `ASTRID_PARENT_MEDIA_SEED_RUNTIME=/home/user/work/runtime` reached the shared Runtime worktree but failed setup because its current fixture module no longer exports historical `_binding_descriptor`; the exact Git seed commit does export it. The temporary historical extraction passed both add and swap cases without changing the shared Runtime or relaxing fixtures. This is a fixture-path caveat, not a product assertion failure.

## Gaps and boundaries

- This is an Agent-source join review only. The normal Runtime 0.2.14-owned pin/private actual pair remains separate and pending; this report is not merge, release, public-pin, or Runtime-candidate approval.
- Full suites, browser/socket journeys, App qualification, renderer/pixel/audio parity, owner-film viewing, and public Runtime publication were not run.
- No source changes were made in this worktree. Next step is the orchestrator’s normal owned-pin/consumer qualification after official Runtime candidate approval.
