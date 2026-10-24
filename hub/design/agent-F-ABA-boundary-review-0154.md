## Report

Verdict: **PASS — stale assertion/oracle boundary; no provider defect evidenced.**

- Reviewed plan, full integrated worker report/evidence, source, emitter, fixture setup, and durable log. No production/test edits.
- Integrated tree: `bc38aa3eb37008e97bcd85833ac9001eb6523d5f`, clean.
- Existing run: `1 failed, 87 passed, 0 skipped, 0 xfailed, 0 deselected`.
- Failure: `tests/timeline/test_authoring_media.py:941`; Runtime had already accepted publication.
- Authoritative base was `wc6-baseline` / `txn-dc108423b1244c3da45a36e12fd25956`. Trusted setup explicitly seeded `clip-1.hold = 0.9` at line 775. The authenticated working base and emitted patch both correctly used `before = 0.9`; unchanged assertion expected `1.8`.
- Accepted publication: `txn-b4c82d1ed17744b09b42defba627bd0f`, revision `authoring-parent-revision-b092947614b682c515cc76789ccf8b60cbce6c0fa33fdc8573e45b956be9dafe`, actor `owner`.
- Request facts: API v1, timeline `film`, label `Publish document`, merge `atomic`, dry-run false, source `{"via":"script"}`, idempotency `wc6-publish`; commands were `occurrence.swap-media` then `doc.patch`; auto steps were `step-1`/ordinal 0 and `step-2`/ordinal 1. Declared reads were absent. Exact project UUID and full media pins were not retained.
- Patch facts:
  - `clips/id:clip-1/at`: present `0` → `0.125`
  - `clips/id:clip-1/hold`: present `0.9` → `0.75`
  - both changes shared one closure ref.
- Source repair `61d53fa452` coalesces only identical authenticated track observations. It does not infer identity from alias or byte equality. Runtime `8ea0766f` strict authentication remains unchanged.
- Downstream reload, undo, retry, invalid no-write, and ABA assertions are **UNQUALIFIED** because execution stopped at the stale assertion. No later write occurred after the accepted publication.

Unapplied oracle-only hunk:

```diff
@@
-    base_bundle = fetch_bundle(project, 'film', revision_id='wc6-baseline', client=client)
+    base_bundle = fetch_bundle(
+        project, 'film', revision_id='wc6-baseline',
+        publication_id=baseline_publication, client=client,
+    )
@@
     changes = publication['data']['commands'][1]['args']['changes']
+    raw_internal = next(
+        row for row in baseline['internal_timeline_revisions']
+        if row['revision_id'] == checkout_shot['internal_timeline_revision_id']
+    )
+    raw_before = next(
+        row for row in raw_internal['payload']['clips']
+        if row['id'] == 'clip-1'
+    )
+    authenticated_before = next(
+        row for row in base_bundle['shots'][first_id]['internal_timeline']['clips']
+        if row['id'] == 'clip-1'
+    )
+    assert authenticated_before['hold'] == raw_before['hold']
     assert [(change['op'], change['path'], change['before'], change['value'])
             for change in changes] == [
@@
         ('set', ['clips', 'id:clip-1', 'hold'],
-         {'state': 'present', 'value': 1.8}, 0.75),
+         {'state': 'present', 'value': authenticated_before['hold']}, 0.75),
     ]
```

This preserves the existing after/children/raw/registry/canonical predicates and makes the before-value derive from authenticated canonical input.

Evidence:

- `/tmp/.../workers/agt-F-ABA-integrated-0150/report.md`
- `qualification-summary.md` SHA256 `e4650e50...`
- `qualification.log` SHA256 `51e98a57...`
- full worker log: 670,939 bytes, SHA256 `ecb27506...`

Static evidence passed: Ruff `2147/2147`, mypy `1911/1911`, vendor lock, artifact manifest, and `git diff --check`. No rerun performed by this review.