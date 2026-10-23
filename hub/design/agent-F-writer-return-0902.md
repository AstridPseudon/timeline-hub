# agent-F-writer-return-0902

## Decision

Repair the existing `TimelineSession._bundle()` hydration seam. Every closure read now sends both `state["base"]["revision_id"]` and `state["base"]["publication_id"]` to `fetch_bundle`, so detached document preflight cannot silently fall back to revision-only hydration when it has no pending commands.

No alternate executor, synthetic cache, weakened closure/digest/fail-closed guard, duplicate implementation, or wire/schema/client change was introduced.

## Exact source delta

`astrid/sdk/timeline/sync.py`:

```diff
-source = ({"publication_id": state["base"]["publication_id"]}
-          if any(command["op"] == "doc.patch" for command in commands) else {})
+source = {"publication_id": state["base"]["publication_id"]}
```

The existing detached caller in `timeline_document.py` already calls `session._bundle(session_state)`; no caller rewrite was needed.

## Regression proof

`tests/sdk/test_timeline_sync.py` now proves:

1. clean/no-pending hydration requests `(revision_id="r0", publication_id="pub0")`;
2. a wrong publication for the selected revision is refused before any write;
3. existing peer fixtures preserve their explicit publication identity under the stricter fake transport.

The original author group remains **12 passing and the visible 1 duplicate-owner failure**. The duplicate failure is intentionally left to D17/G5 as directed.

## Results and limits

Targeted Agent neighbours: **111 passed**. Exact new hydration nodes: **2 passed**. Ruff: **2149/2149**. Mypy: **1912/1912**. Vendor lock, artifact manifest, and `git diff --check`: **pass**.

No full/P1/P4HTTP/native14/crash24/heavyjourney/browser/live-socket suite was run. Harness finalization created the worker snapshot `d05fcc076`; the worker did not execute git commit/merge/rebase/checkout or modify shared dependencies.
