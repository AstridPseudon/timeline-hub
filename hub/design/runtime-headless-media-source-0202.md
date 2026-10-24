**Blocked: final targeted run is 11 passed, 1 failed.**

Changed only the headless test family. The positive now ingests a real video through Runtime, deep-copies `AUTHORED`, replaces only `"x"` with its verified digest, and submits `media.admit`. Original constants, historical requests, SQL helpers, and all 11 restored cases remain unchanged. Acceptance and downstream receipt/history/event/closure/digest/reload/retry assertions remain required.

Qualification used Agent candidate `5aee1f361147c7f1b02ba158092889be4efb15da`, without Agent edits.

The remaining blocker is `parent_revision.payload.clips`: `invalid_document: candidate.parent.clips: must be a list`. Agent’s [_doc_patch.py:393](/home/user/work/wt/agt-pin-5aee1f36/astrid/sdk/timeline/_doc_patch.py:393) removes the root mirror when replacing bootstrap config; [native_sites:184](/home/user/work/wt/agt-pin-5aee1f36/astrid/sdk/timeline/_doc_patch.py:184) then supplies no assignment site to recreate it. A remove-config-first trial failed with `missing path ancestor` and was reverted.

Validation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python \
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-5aee1f36 \
/home/user/work/venv-runtime/bin/python -m pytest -q \
-o addopts= -p no:cacheprovider --tb=short \
tests/test_timeline_headless_overwrite_refused.py
```

**11 passed, 1 failed.** Legacy negatives prove the earlier 410 refusal and unchanged state; empty-bootstrap and secondary-creation positives pass. Authored acceptance and downstream assertions remain unverified.

```bash
/home/user/work/venv-agent/bin/ruff check --no-cache \
tests/test_timeline_headless_overwrite_refused.py \
"$TMPDIR/headless-media-checks/original.py"
git diff --check
```

Both passed. Pyright ran separately on original `458595850` and final copies using:

```bash
/root/.local/bin/pyright \
--project "$TMPDIR/headless-media-checks/pyrightconfig.json" \
--pythonpath /home/user/work/venv-runtime/bin/python \
--outputjson <copy>
```

Original: **4 diagnostics**; final: **0**; zero new identities/multiplicities. In-memory compilation and AST/source-byte comparisons passed. No full/browser/gate runs.

Wrote `commit-msg` and `BLOCKED`; no `DONE`. Next: manager resolution of the clips mapping, followed by qualification against independently reviewed and merged Agent source. No final Runtime qualification is claimed.