# G5 inverse reader — independent fixture review

## Verdict

**PASS — the bounded Agent fixture correction is source-faithful. Runtime
observer handback is permitted; this review grants no undo/redo credit.**

Reviewed `tl/agt-G5-inverse-reader-return-1250` at `77ab3908f` in the review
worktree. The candidate changes only
`tests/sdk/test_timeline_restructure_guarded_runtime.py`; the inherited
`restructure_runtime` fixture and the original accepted restructure,
whole-undo/redo, overlap-refusal, and no-write assertions are unchanged. No
production SDK, generated client, Runtime, provider, schema, contract, pin, or
shared dependency was changed.

## Authority and exact-pair review

The new fixture uses the real public `RemoteTimelines` methods at the same
boundary as the generated client:

| Fixture binding | Authority and forwarding checked |
| --- | --- |
| `generated.list_timelines(project_id, *, cursor, limit)` | Delegates to `RuntimeService.list_timelines` and converts the service page mapping to the generated `(items, next_cursor)` shape used by the production resolver. |
| `generated.inspect_timeline(project_id, timeline_id, options=None)` | Delegates the complete options mapping, including `revision_id` and `limit`, to `RuntimeService.inspect_timeline`. |
| `generated.list_timeline_commits(project_id, timeline_id, *, cursor, limit)` | Forwards cursor/limit and the inherited fixture authorization callback to the Runtime history owner. |
| `RemoteTimelines._resolve_timeline` / `open_composition` | Uses the production resolver and inspection adapter, rather than a fixture lambda or private document shortcut. `open_bundle` therefore sends the historical `revision_id` and `limit=1` through the public inspection path. |
| Parent, shot, and internal revision methods | Forward exact project, owner ID, and revision ID to the inherited Runtime service handlers. |
| `RemoteTimelines.open_bundle` | Uses production exact-closure hydration, publication receipt lookup, canonical-document equality, dependency-manifest checks, and content-digest-bearing image data. |

There is no broad `**kwargs` sink, no return-current-head substitution, and no
fixture-supplied `_runtime_document`. The only `_runtime_document` consumed by
the fixture is the source mapping returned by production `open_bundle`.

The new authority smoke selects a historical receipt, calls
`open_bundle(revision_id=..., publication_id=...)`, and proves that the result
is that historical revision (`is_current_head is False`), has the requested
parent revision/publication pair, carries a nonempty parent content digest, and
is structurally equal to the selected receipt's canonical document. It also proves
that pairing the historical revision with the current publication is refused,
that a missing scope is refused, and that both history and the current head
remain unchanged. The history calls use explicit limits; `open_bundle`'s
receipt scan uses its production paged history path, so the test cannot pass by
silently replacing a historical lookup with head.

## v2 request/reply and source-fidelity mapping

The candidate adds only read-boundary setup and authority assertions. It does
not reconstruct, narrow, normalize, or replace the production v2 request or
reply. The retained mutation body remains the source of truth:

| v2 area | Retained source/test evidence |
| --- | --- |
| `api_version`, project/timeline scope, exact base revision/publication pair, commands, label, steps, merge, reads, `dry_run`, `source` | Existing guarded inverse assertions at `tests/sdk/test_timeline_restructure_guarded_runtime.py:181-190`; the fixture's `send` path passes the captured body unchanged to Runtime. |
| `rationale` and `group_id` | Existing explicit absence assertion at `:192`; the inherited preview coverage retains populated `source`, `rationale`, and `group_id` (`tests/sdk/test_timeline_restructure.py:679-691`). |
| Command envelope and step metadata (`schema_version`, `select`, `args`, IDs, intent, tags, ordinals, patches) | Produced by the existing restructure emitter/provider path and retained by the unchanged `commands`/`steps` assertions (`:191-196`); the review adds no alternate executor or synthetic command. |
| Idempotency | Existing calls keep their stable keys (`inverse-name`, `inverse-cut`, `inverse-undo`, `inverse-redo`, `inverse-overlap`, `inverse-refuse`); the inherited `send` records and forwards each key to Runtime. |
| Accepted reply data/receipt, canonical document, accepted revision, merge mode, document digest | Existing assertions at `:201-207`. |
| History records and `undo_steps` | Existing stored-history assertion at `:208-210`; the new smoke additionally snapshots the complete history before and after negative reads. |
| Whole undo/redo canonical closure and dependency manifest | Existing assertions at `:212-256`, unchanged. |
| Intervening overlap conflict and no-write behavior | Existing assertions at `:258-276`, unchanged. |
| Preview `would_status` and structured request annotations | Inherited preview test at `tests/sdk/test_timeline_restructure.py:679-691`; untouched by this candidate. |
| `merged`, `conflict`, `invalid`, and provider-complete `records` fields (`bindings`, `effects`, `dependencies`) | Not newly exercised by this read-only fixture. They remain production/provider contract data and are not altered, dropped, or falsely claimed by this review. A future integrated proof must continue to cover them; this bounded PASS is not that proof. |

Thus the full v2 request/reply contract remains preserved by the existing
caller and test body. This review certifies only the newly repaired public
reader authority and its exact historical closure behavior.

## Evidence

Commands run against the review worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_restructure_guarded_runtime.py -k fixture_reader
1 passed, 1 deselected in 6.98s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_restructure_guarded_runtime.py
2 tests collected in 1.01s

/home/user/work/venv-agent/bin/ruff check --no-cache tests/sdk/test_timeline_restructure_guarded_runtime.py
All checks passed!

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m mypy --cache-dir=<private worker cache> tests/sdk/test_timeline_restructure_guarded_runtime.py
Success: no issues found in 1 source file

git diff --check
passed
```

The first collection attempt used the harness-provided `tmpdir` path, which
is an existing regular file in this environment; it did not run pytest. The
rerun used a private worker cache and passed. No full, browser, HTTP/socket,
P1/P4, native, D17, or the known original 503-body test was run.

## Disposition and next step

No review change is required. Runtime may hand back its single bounded
observer invocation now that the Agent public-reader setup is independently
qualified. That handback must report Runtime behavior only; it does not grant
undo/redo credit. G5 remains draft-only and P1-gated, with the original
inverse journey still pending the explicitly allowed Runtime observation.
