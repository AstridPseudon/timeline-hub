# WC3 explicit media-pin type guard

## Exact diff

```diff
diff --git a/astrid/sdk/timeline_media_replacement.py b/astrid/sdk/timeline_media_replacement.py
@@
-    if isinstance(old_media, Mapping) or isinstance(media, Mapping):
-        if not isinstance(old_media, Mapping) or not isinstance(media, Mapping):
-            return False
-        if dict(old_media) != dict(original_old) or dict(media) != dict(original_new):
-            return False
-    return True
+    if old_media is None and media is None:
+        return True
+    if not isinstance(old_media, Mapping) or not isinstance(media, Mapping):
+        return False
+    return dict(old_media) == dict(original_old) and dict(media) == dict(original_new)
```

Tests add one parameterized pending-retry negative matrix for `bool`, `list`,
`str`, `number`, and a `None`/mapping null mix. Each asserts validation failure,
zero `flush` calls, and byte-for-byte unchanged session/outbox state. A second
parameterized positive probe covers the allowed `None`/`None` pair and exact
five-field mapping pair.

## Source

- `astrid/sdk/timeline_media_replacement.py:219-223` now accepts caller
  selections only when both are omitted (`None`) or both are mappings exactly
  equal to the persisted old/new five-field pins.
- Existing owner, clip, source-object, head/publication, pending-count,
  operation, intent, opaque-command, and persisted flight key/body guards are
  unchanged.
- No API, DTO, endpoint, schema, retry framework, source import, or sibling
  WC6 change was added.

## Tests

- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/test_timeline_clip_replacement.py`
  — **20 passed in 1.79s**.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_sync.py::test_lost_ack_reload_retries_exact_request_before_sending_suffix tests/sdk/test_timeline_sync.py::test_changed_intent_key_and_dry_run_cannot_replace_an_ambiguous_request`
  — **3 passed in 1.13s**.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline_media_replacement.py tests/test_timeline_clip_replacement.py`
  — **All checks passed**.
- `git diff --check` — passed.

## Limits and notes

- No full, 165-test, 2478-test, browser, live-socket, integration, or central
  suite was run, per the task limits.
- This proves the adapter’s type guard and fake-session refusal/positive control
  flow only. It does not qualify the separate private Runtime parent-provider
  cohort or claim that this guard alone restores whole WC3.
