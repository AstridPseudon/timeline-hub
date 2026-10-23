# F legacy admission review

Date: 2026-10-23 UTC

**Source verdict: PASS. Donor packet verdict: HOLD/FAIL for direct merge.**

Reviewed `ae3debdd3` against parent `2e21af300`. The production change is
exactly this one hunk in `astrid/core/execution/generic_host.py`:

```diff
-    if record.adapter.remotion != "selected":
+    adapter = getattr(record, "adapter", None)
+    if adapter is None or adapter.remotion != "selected":
```

Parent and current integration source blob: `195839982f128753bd9bc06d59c43b51fd8912bb`.
Donor source blob: `8f48f8f7c3126df26ab5499f945b48e0c5e5f450`.
Current integration tree checked: `958ccfdd1980062bf3b315c81f8e1a6ad97b14c3`.

The real `_run_task_impl` caller now handles the supported minimal capability
record without an adapter, then preserves the existing immutable original
target refusal before execution. Existing adapter/renderer selection,
scope/fence/lease/security guards, no-execution behavior, and artifact
preservation are unchanged. No default or guessed renderer is introduced.

Independent evidence:

- Requested acceptance plus eight adjacent renderer controls: **9 passed in 36.09s**.
- Ruff: **2149/2149**.
- Mypy baseline: **1912/1912**.
- Vendor lock, artifact manifest, and `git diff --check`: **PASS**.

The donor commit also adds `Externalreport.md` and
`design/agent-F-legacy-admission-0906.md`; those are not production source
and make the donor packet non-mergeable as-is. The clean port is source-only.
No full/browser/heavy/P1/P4 HTTP/native14/crash24/D13 or daemon operation was
run. Full v2 request/reply fields remain outside this one-hunk source diff.
