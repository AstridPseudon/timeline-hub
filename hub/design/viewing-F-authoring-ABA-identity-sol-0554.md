**NOT IMPLEMENTED — repair requires reserved State/inverse support.** Bounded source work is complete; product files are unchanged.

Added two controls to `test_authoring_item_observation_boundary.py`: published item identity resolves independently of position, including colon-containing IDs; placement-local aliases remain rejected.

The per-item experiment established:

- Numeric reads succeed; `item_id:item-1` reads incorrectly return absent.
- Qualified writes fail with `write requires recorded container creation`.
- Inverse aggregate folding raises `ValueError` while parsing the identity token as an integer.

This establishes why changing native emission alone is insufficient. It does **not** establish that whole-collection replacement is required.

Validation used `PYTHONPATH="$PWD:/home/user/work/runtime"` and `PYTHONDONTWRITEBYTECODE=1`:

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 --tb=short --basetemp="$TMPDIR/final-projection" tests/editing_conformance/test_authoring_landing_projection.py tests/editing_conformance/test_headless_root_mirror_effects.py tests/editing_conformance/test_authoring_undo_projection.py tests/editing_conformance/test_private_sequential_capture.py tests/editing_conformance/test_provider_step_undo_v2.py tests/editing_conformance/test_authoring_item_observation_boundary.py
# 2 failed, 78 passed in 11.35s

/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 --tb=short --basetemp="$TMPDIR/final-media" tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_occurrence_media_manifest_inverse.py
# 113 passed in 8.85s

/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/commands.py astrid/sdk/timeline/_doc_patch.py astrid/sdk/timeline/_commit_patch.py astrid/sdk/timeline/native_occurrence_media_commands.py tests/editing_conformance/test_authoring_item_observation_boundary.py
# All checks passed!

/home/user/work/venv-agent/bin/python -m mypy --cache-dir "$TMPDIR/mypy-final" --follow-imports=silent astrid/sdk/timeline/commands.py astrid/sdk/timeline/_doc_patch.py astrid/sdk/timeline/_commit_patch.py astrid/sdk/timeline/native_occurrence_media_commands.py tests/editing_conformance/test_authoring_item_observation_boundary.py
# Success: 5 source files

/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
# ok runtime.lock.json

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# artifacts.json is current

git diff --check
# passed
```

The two failures remain the saved accept/preview `invalid_records: provider observation has an ambiguous item path` regressions. The prescribed `test_authoring_inverse_observation.py` does not exist; the actual saved regression filename was used. Original media test bytes and all **59 assertions** are preserved.

**Exact UNAPPLIED reserved-seam proposal — Agent R1/R2 owner.** These prerequisite hunks were generated and syntax-parsed only; they were neither applied nor executed. They do not constitute a qualified complete repair.

```diff
--- a/astrid/sdk/timeline/_command_state.py
+++ b/astrid/sdk/timeline/_command_state.py
@@ -287,6 +287,36 @@
         elif value['shot_id'] not in self.bundle['shots']:
             raise CommandError('occurrence references missing shot', kind='identity_conflict', ref=ref)
 
+    def _shot_item_path(self, ref, path, *, authored=False):
+        if (not ref.endswith('/shot') or len(path) < 4
+                or tuple(path[:2]) != ('payload', 'items')
+                or not path[2].startswith('item_id:')):
+            return path
+        identity = path[2].removeprefix('item_id:')
+        shot = self.occurrence(ref.removesuffix('/shot'))['shot_id']
+        source = self.bundle['source_mapping']['shots'].get(shot)
+        if source is None:
+            raise CommandError('shot item source is unavailable', kind='history_unavailable', ref=ref, path=path)
+        mapping = source.get('item_id_map', {})
+        if (not isinstance(mapping, dict)
+                or any(not isinstance(key, str) or not isinstance(value, str) or not key or not value
+                       for key, value in mapping.items())
+                or len(set(mapping.values())) != len(mapping)):
+            raise CommandError('shot item map is ambiguous', kind='identity_conflict', ref=ref, path=path)
+        published = self.get(ref, ['payload', 'items']).get('value')
+        local = self.bundle['shots'][shot]['payload'].get('items')
+        for rows in (published, local):
+            if not isinstance(rows, list):
+                raise CommandError('shot items must be an array', kind='identity_conflict', ref=ref, path=path)
+            ids = [row.get('item_id') if isinstance(row, dict) else None for row in rows]
+            if (any(not isinstance(item, str) or not item for item in ids)
+                    or len(set(ids)) != len(ids)):
+                raise CommandError('shot item identity is ambiguous', kind='identity_conflict', ref=ref, path=path)
+        observed = one(published, 'item_id', identity)
+        stored = one(local, 'item_id', mapping.get(identity, identity))
+        rows, row = (local, stored) if authored else (published, observed)
+        return [*path[:2], str(rows.index(row)), *path[3:]]
+
     def get(self, ref, path):
         if ref == 'parent' and list(path) == ['occurrences']:
             return present(copy.deepcopy(self.bundle['placements']))
@@ -315,6 +345,7 @@
             mapping = self.bundle['source_mapping']['shots'].get(shot, {}).get('item_id_map', {})
             value = {'payload': _remap_known_item_references(self.bundle['shots'][shot]['payload'],
                                                            {v: k for k, v in mapping.items()})}
+        path = self._shot_item_path(ref, path)
         for key in path:
             if isinstance(value, dict) and key in value:
                 value = value[key]
@@ -497,6 +528,7 @@
             elif state["state"] == "present":
                 rows.append(copy.deepcopy(state["value"]))
             return
+        path = self._shot_item_path(ref, path, authored=True)
         value = self.entity(ref)
         if ref.endswith('/shot') and tuple(path[:1]) == ('payload',) and len(path) > 1:
             # Only the occurrence's own shot root; display IDs never select it.
--- a/astrid/sdk/timeline/inverse.py
+++ b/astrid/sdk/timeline/inverse.py
@@ -20,6 +20,7 @@
     equal,
     logical_address,
     overlaps,
+    one,
     present,
     root_identity,
 )
@@ -107,7 +108,8 @@
                 raise CommandError('ambiguous collection alias', kind='identity_conflict')
             node = matches[0]
         elif isinstance(node, list):
-            node = node[int(token)]
+            node = (one(node, 'item_id', token.removeprefix('item_id:'))
+                    if token.startswith('item_id:') else node[int(token)])
         elif isinstance(node, dict):
             if token not in node:
                 if replacement == ABSENT:
```

After release, the native companion must emit `item_id:<published-id>` instead of numeric item indices. Required qualification includes the original two RED→GREEN controls; exact undo/redo; missing/duplicate identities; foreign owner; changed revision; order and ABA; corrupt/nonbijective mappings; and mixed aggregate/leaf folding. **Authored root aggregates require particular care:** the inverse hunk above does not itself translate published IDs inside placement-local aggregate values. Assets/audio-binding numeric paths are outside this bounded proposal.

Recommend handing these precise seams to Agent R1/R2 before further product edits. Actual11466 private custody remains absent; prior candidate/packets were cleaned. No original/live/full/browser run occurred. Commit message and bounded-completion `DONE` were written.