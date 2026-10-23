# V4 D16 stale-window test adaptation — FAIL

## Change

Changed only `tests/editing_conformance/test_native_word_anchor.py`, function
`test_stale_anchor_refuses_when_intervening_window_excludes_selected_word`.
The test now accepts the D16 earlier refusal point: it first accepts the
selected authored anchor, then submits the `fixture.window` edit changing the
source window to `4..6`, which excludes the retained word at `3..3.5`.

The original protected refusal reason and no-write/head behavior remain
asserted, the status is relocated from the old later replay classification
`conflict` to the D16-required earlier classification `invalid`, and the
selected word/source facts remain asserted. The new exact path assertion is:

```python
["parent", "clips", "id:card", "app", "astrid", "word_anchors", "on"]
```

### Old assertion → new location

| Original assertion | D16 adaptation |
| --- | --- |
| `match="outside the half-open source window"` on the stale anchor submit | Same message predicate on the earlier `window-orphans-anchor` submit. |
| `details["reason"] == "invalid_anchor"` | Retained on the earlier window-edit refusal. |
| `details["status"] == "conflict"` | Re-expressed as D16's earlier `details["status"] == "invalid"`; the same refusal reason and no-write guarantee are retained. |
| `case.head() == head` | Retained after the window-edit refusal. |
| No prior authored anchor before the window edit | Replaced only as required by D16 with an accepted `selected` anchor, so the source-window edit has an authored reference to orphan; the selected word and source facts are then explicitly preserved. |

## Test evidence

Preflight confirmed Agent base `3e4261e9694c7bd7c1b5fada9bf01d91007bcc80`,
Runtime checkout `ad823e0a0f5be4a7acf1d3006df6f794709da63d`, and only the target
test file modified.

Exact allowed targeted command (run once, after adaptation):

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py -k stale_anchor_refuses_when_intervening_window_excludes_selected_word
```

Result: **FAIL — 1 failed, 53 deselected in 1.53s.** The real native
provider/Runtime path returned `reason == "invalid_anchor"` and
`status == "invalid"`, but returned `details["path"] == []` instead of the
required exact anchor-reference path. The full first-run log is
`targeted.log` in this worker directory. No behavioral rerun was performed.

Independent static checks:

- `ruff check --no-cache tests/editing_conformance/test_native_word_anchor.py` — PASS.
- `git diff --check` — PASS.
- Typecheck — N/A; this is a test expectation adaptation only.

## Source gap and next steps

The required path assertion is intentionally retained and is not weakened to
accept the empty path. The source gap is in the Agent provider's structured
error path: the earlier native anchor invalidation is raised as an
`invalid_anchor` command error without an anchor-reference `path`, and the
commit error conversion therefore publishes an empty path. This worker made
no product/provider change, as prohibited by D16. The Agent provider owner
should add the exact anchor-reference path before this test can pass, followed
by one fresh targeted run.

Delivery behavior change: **source-window edits that orphan an anchor are
refused at edit time.** This result does not claim the targeted case passes,
nor any broader V4/52/54 qualification.
