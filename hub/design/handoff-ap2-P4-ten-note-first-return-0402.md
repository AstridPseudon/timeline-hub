# P4 first return — ten-note public undo source handoff

## Packet

Import only the new test file:

`tests/editing_conformance/test_p4_ten_note_v2_runtime.py`

This is a test-only source packet. It is based byte-for-byte on donor
`b4f4ba00e` except for the two intentional edits below:

```diff
-from typing import Any, cast
+from typing import Any
...
-        session = cast(Any, reloaded.session)
+        session = reloaded.session
```

The test calls the real public Agent API and retains all original positive
assertions. It does not add a transport or executor and does not call a
private provider.

## API/source identity

Agent source is `a568c4ebf804119e3e21a1644b6d6068ed037380` (tree
`73e56c0cbb21037bae9a90bf7bcbd9654c017757`). The API is
`astrid/sdk/timeline/sync.py` blob `5e7dfeec3b2a7f03849b58e5d09a5456b81a0a7b`:

```text
TimelineSession.undo(self, publications, *, steps=None,
                    idempotency_key=None, dry_run=False, via="python")
```

The method emits `timeline.inverse` and sends through the existing public
session flush/generated HTTP path. Runtime collection used normal34e at
`34eac0041b0891e9011966b39bcbd26053fde5bc` (tree
`9853574865f25e08284e82ffb26c0bdecaa16a30`).

## Qualification status

Pure source controls pass: marker-enabled collection collected 1 test, Ruff,
mypy, and `git diff --check` passed. The exact unmarked collection command
returned exit 5 only because the repo's default addopts deselect integration
tests. No HTTP/body or service-heavy execution was run. Actual acceptance is
held for the compatible normal34e/G3/R2 joined source and the later owner
run.

