## Result

PASS — bounded Agent + Runtime joined-source review.

- Agent: `d33fe5f9f0`, tree `c8dcd1e2`
- Runtime repair: `35764ce10c`, parent `1d9ddba546`, tree `c026c3e4`
- Mutable Runtime tip was `becfe6db`; tests used an immutable archive of `35764ce10c`.
- Runtime’s previously reviewed security suite: `177 passed` (reused, not rerun).

Exact diagnostic command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$TMP_RUNTIME" \
ASTRID_RUNTIME_CHECKOUT="$TMP_RUNTIME" \
/home/user/work/venv-agent/bin/python -m pytest -q \
-oaddopts= -pno:cacheprovider --timeout=45 --tb=short \
tests/editing_conformance/test_authoring_item_observation_boundary.py \
--junitxml="$TMPDIR/aba-joined-95.xml"
```

Result: `95 collected: 89 passed, 6 failed, 0 skipped, 0 errors`.

All four shared accept/preview positives and both retained-source-copy comparisons passed.

The six failures are stale diagnostic expectations only:

| Cases | Expected assertion | Actual result | Protected property |
|---|---|---|---|
| Native-item accept/preview | `native write membership differs` refusal | No refusal | Exact authenticated source-stage capture and item mapping |
| Native-item accept/preview historical spelling | `_inverse_stage_ranges()` succeeds | Earlier refusal: `shared inverse native captures differ from authenticated history` | Complete source-authenticated native capture equality |
| Ordinary-media accept/preview | Old shared-root refusal | Accepted | Target-only restoration, retained sibling/root identity and edges |

These are classified under D16/C0 as old or earlier refusal-location mismatches; no assertions were changed. Viewing owns expectation migration.

Reviewed production reachability:

`timeline_document` → `capture_occurrence_swap_media` → `TimelineSession.undo` / `AcceptedRecords` → Agent inverse projection → Runtime authenticated stage validation.

Verified source guards include published-to-local item mapping, missing/duplicate/foreign owner/revision/digest refusal, strict order/range/capture/ABA checks, authenticated materialization pins, and unchanged untouched sibling/root images.

Static checks:

- In-memory Python compilation: pass
- Ruff: pass
- Mypy with explicit Python 3.12 target: `Success: no issues found in 4 source files`

No product, diagnostic, schema, client, or pin files were modified. No HTTP, full-suite, browser, live-image, or original-body qualification was performed. Original qualification remains held pending reviewed home integration.