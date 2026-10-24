Implemented the Agent correction in [_commit_preview.py](/home/user/work/wt/agt-F-helper-map-sol-0210/astrid/sdk/timeline/_commit_preview.py), with [12 focused controls](/home/user/work/wt/agt-F-helper-map-sol-0210/tests/editing_conformance/test_sequential_read_replay_map.py). Independent review agrees Agent owns the defect.

The carrier now omits unchanged physical read mappings while retaining all execution/read/dependency/binding facts, patch mappings, prepared digest, and six-key shape. Filtering after replay compares actual original/landing references, including staged outputs.

Validation used the qualified Runtime `8ea0766f` environment:

- `python /tmp/w-ce4c602fe8/replay.py` — exact 0202 packet **old RED/new GREEN** through both unchanged Runtime validators. Map **14 → 5**; every other carrier field identical.
- `python -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-ce4c602fe8/focused-corrected tests/editing_conformance/test_sequential_read_replay_map.py -x` — **12 passed**. Initial run failed on a new fixture’s missing optional `reads` array; corrected before this run.
- Scoped `ruff check --no-cache` — passed. Whole-tree Ruff — **2,145 findings each**, exact normalized parent/current diagnostics identical.
- Parent/current `timeout 45 python -m mypy astrid scripts/reshape --cache-dir=<private-cache> --hide-error-context --no-color-output --no-pretty --show-error-codes` — both **timed out (124)**; **449 partial errors each**, byte-identical. Complete typecheck remains unverified.
- `python scripts/artifact_manifest.py --check` and `git diff --check` — passed.

**Qualification blocked:** the single original helper `[True]` attempt used `timeout 45 … python /tmp/w-ce4c602fe8/observer.py`. Runtime’s sequential validator returned, then the observer refused tuple-key serialization at `runtime_validation_result.binding_pairs`. I stopped without retrying or running `[False]`/existing guard followups. Acceptance and full helper success remain unverified.

The [durable new capture](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-helper-map-sol-0210/helper-true.json) contains **8,151,405 bytes**, five map entries, and expected/seen counts **5/5**. Before/after origins and all six original function-body hashes match. [Validation summary](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-helper-map-sol-0210/validation-summary.json) and observer/replay scripts are retained; worker evidence totals **12 MB**.

Commit message and `BLOCKED` marker written. No integration merge, vendor checker, full suite, shared-environment mutation, or deletion occurred. Next: independent patch review, then separately authorized observer repair and remaining qualification.