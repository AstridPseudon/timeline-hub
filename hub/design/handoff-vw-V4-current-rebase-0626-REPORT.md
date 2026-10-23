# V4 current retained rebase pair — blocked

## Change

On Agent base `3e4261e9694c7bd7c1b5fada9bf01d91007bcc80`, changed only the
allowed fresh C0 assertion in
`tests/editing_conformance/test_native_word_anchor.py`:

```diff
-    assert accepted["data"]["status"] == "rebased"
+    assert accepted["data"]["status"] == "merged"
```

The fixture and test blobs were initially exactly the required `5292b388a`
blobs. No product, fixture, recipe, Runtime, pin, generated, package, schema,
undo, provider, or other test files were changed.

Fresh Runtime authority was inspected at
`ad823e0a0f5be4a7acf1d3006df6f794709da63d`: current v2 records use
`accepted`/`merged`; historical ABI-1 receipt tests retain `rebased`.

## Required pair execution

Command, run once:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py -k follow_rebases_original_choice_after_source_move_and_reorder
```

Result: exit `1`; `1 failed, 53 deselected in 1.91s`.

The real provider failed before the stale acceptance assertion, during the
`move-source` commit for `[True]`:

```text
runtime_protocol.errors.RuntimeErrorBase: candidate.timing: legacy word anchor is missing
```

Traceback frames identify `astrid/sdk/timeline/commit.py:1159` and pinned
Runtime `runtime_protocol/service.py:2483`. The full first-run harness trace is
in the worker `log.txt` at this directory; no rerun was performed.

## Limits / next step

Per the task contract, this real source/guard failure is a blocker. No product
fix, assertion weakening, rerun, full suite, native14, 54-case, browser, or
heavy test was run. Scoped Ruff and `git diff --check` were not run after the
failure because the instruction required stopping immediately. Typecheck is
N/A for the one literal assertion correction.

The source owner should repair or qualify the pinned native word-anchor replay
input/guard path, then rerun this exact pair once. The status correction should
remain `merged`; historical exact-receipt `rebased` expectations must remain.
