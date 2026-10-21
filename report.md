# WC8 literal text data-safety review

## Verdict: APPROVE

Approved exact Agent commit `c723cbbd8ee51dde0a507cefd5a61ff62c957107`
(`tree 1bb8c44a8e93ae74ea8bef2771e553db351df5c3`), reviewing the bounded
combined WC8 delta from hub base `18a89a0d29766bd3cec31391042836ba7c951fa1`
through retained-basis commit `f4ddce5cc204e6d4b0695fb4f869697be192320a`
and the literal-replacement fix in `c723`.

## Scope and source review

The candidate changes exactly three existing Agent files relative to `f4dd`:

- `astrid/sdk/timeline_sheet.py`
- `tests/sdk/test_timeline_sheet_native.py`
- `tests/editing_conformance/test_native_sheet_ordinary_runtime.py`

No other blob differs from the reviewed parent. The `f4dd` translator is
bounded to retained detached type rows: it requires the same `(cut, row name)`
keys, resolves the owner through the retained artifact binding, reads the
clip from the retained `NativeSheet._bundle`, and refuses unsupported timing
grammar (`on`/`until`, missing/non-string text, non-type clips) before staging.
After translating only the recognized text/duration cell, the semantic
comparison must match the original sheet, so unrelated or mixed grammar cannot
silently fall through to a partial local writer (`timeline_sheet.py:862-918`).

The fix at `timeline_sheet.py:895-898` changes only the `re.subn` replacement
from a replacement string to a callback returning `new_token`. That preserves
JSON-encoded backslashes, `\\n`, `\\1`, quotes, and other replacement syntax as
literal text. `ensure_ascii=False` preserves declared non-ASCII text. Empty
strings remain represented by the existing JSON token path.

The retained basis/outbox path remains authoritative: `_stage_sheet` reopens
the existing outbox, constructs `NativeSheet` from `state["sheet"]["bundle"]`
and its saved basis, then stages `native.preview(translated)`; it does not
fetch a current head or recapture from a snapshot (`astrid/sdk/timeline/checkout.py:561-603`).
The normal session commit then sends the saved base pair and pending command
through the existing HTTP commit/outbox path. No new schema, operation, pin,
metadata authority, client authority, snapshot-diff path, or legacy writer was
introduced.

## Evidence inspected

The existing offline neighbors retain the original behavior and guards:

- `tests/sdk/test_timeline_sheet_native.py:74-89` checks `CHANGED`, empty, and
  escaped newline/backslash text capture, exact pending native command, and
  unchanged sibling occurrence.
- `tests/sdk/test_timeline_sheet_native.py:99-152` checks retained original
  basis, reload, lost-ACK exact retry without recapture, disjoint/same-peer
  behavior, and guarded inverse/redo.
- `tests/sdk/test_timeline_sheet_native.py:155-181` checks refusal leaves
  draft/outbox unchanged and target identity changes do not queue or read.
- `tests/sdk/test_timeline_sheet_native.py:279-297` checks unbound, altered,
  extra, and mixed native-row grammar is refused before queueing.

The actual current014 HTTP test is a real current Runtime path: its fixture
builds the historical seed through the frozen Runtime API, migrates it through
the current Runtime, and preflights current closure/owner/opaque-field
identity (`tests/editing_conformance/test_native_sheet_ordinary_runtime.py:166-243`).
The test then asserts:

- exact declared value: `line\\nnext C:\\tmp\\file \\1 — café "quoted"`;
- exactly one captured `clip.set-params` command with `clear=[]`;
- retained `base_revision_id` and `base_publication_id`;
- normal HTTP source `{"via": "sheet"}`;
- exact post-commit value, opaque fields, and unchanged sibling;
- exact value after Runtime restart;
- guarded inverse to the original entity and redo to the accepted entity
  (`tests/editing_conformance/test_native_sheet_ordinary_runtime.py:416-466`).

## Test evidence reused

Per the task instruction, I did not requalify or rerun the existing test
results. The recorded results are:

- Before the callback fix: focused regression `2 passed, 1 failed`.
- After the fix: `PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/pytest -q tests/sdk/test_timeline_sheet_native.py -k 'detached_static_text' --disable-warnings --maxfail=1` — **3 passed**.
- Neighbor lane: `PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/pytest -q tests/sdk/test_timeline_sheet_native.py tests/editing_conformance/test_native_sheet_current.py tests/editing_conformance/test_native_sheet_ordinary.py --disable-warnings --maxfail=1` — **114 passed**.
- Exact current HTTP node, central service: `env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-current ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-current/node_modules /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_text_literal_uses_native_http_and_guarded_inverse` — **1 passed in 4.37s**, exact tree `1bb8c44a8e93ae74ea8bef2771e553db351df5c`.
- `git diff --check` — **passed**.

No full, browser, render, install, native-socket, generation, or old duration
matrix rerun is claimed. No tests were removed, skipped, weakened, or marked
xfail. I found no data-safety counterexample within this bounded slice.

