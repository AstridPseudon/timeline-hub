# WC8 retained-parameter current-preserving Agent HOME port

Status: **HELD / prepared in the worktree; staging was blocked by the read-only shared index, and no remote HOME merge was requested.**

## Result

- Captured current Agent base before editing: `b8bbb5cf1d7f64b6a51e762ef394c4278b3e5492` (`tl/integration`).
- HOME font/color commit `b8bbb5cf1` was already present and was not merged again.
- Applied the independently approved c067 product exactly onto current: `c0671afddb34f4fe6b8ca66f511df9fc530cc344`.
- Added the exact corrected actual-only test from `33f88975eea0006a624c5e0a95bd2fd307695028`.
- Final changed paths are only:
  - `astrid/sdk/timeline_sheet.py`
  - `tests/sdk/test_timeline_sheet_native.py`
  - `tests/editing_conformance/test_native_sheet_ordinary_runtime.py`
- `timeline_sheet.py` and `test_timeline_sheet_native.py` are byte-for-byte equivalent to c067; the actual test is byte-for-byte equivalent to 33f.
- No coupled conflict was found. Every path outside the allowlist remains equal to the captured current base; no private017, route cut, whole-WC8 closure, or test weakening was introduced.

The product hunks retain existing parameter-cell presence and permit existing opaque JSON/null/literal values through the live detached NativeSheet caller, while preserving refusal for added cells, selected pack parameters, formulas, expression/elided values, and stale basis. The retained legacy translator now carries existing literal parameter cells beyond the already integrated font/color fields.

## Tests and evidence

Direct permitted lane:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet_native.py tests/editing_conformance/test_native_sheet_current.py
111 passed in 14.99s
```

The exact corrected actual0913 central result was checked, not rerun:

```text
suite: rt-wc8-current14-integration
tree: 45a46eeda044f33c99f0fb118cc6cd0da373d5dd
selector: tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_opaque_null_rename_uses_retained_basis_and_guarded_http
result: 1 failed in 5.62s
```

It reached the intended stale-basis refusal, then failed the unchanged final-head assertion because guarded inverse/redo left the same revision with a new publication ID (`txn-b5bbe938517a481697f64f8f2d4c2bac` versus `txn-2707d8b6c2034f228c55a21858aba84d`). The actual brief authorized no third run. This port therefore does not claim live Runtime qualification or actual PASS.

Normal tuple recorded by the actual-neighbor note: Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d`, published source `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, all 76 contract artifacts, ordinary `6ba7b51e`, Composition C13 / `0.0.13`.

## Handoff

The requested `git add` of the three allowlisted files was attempted, but the worktree’s shared Git index is read-only:

```text
fatal: Unable to create '/home/user/peteromallet/astrid-agent/.git/worktrees/rt-m2-wc8-params-current-home-port-0915/index.lock': Read-only file system
```

The worktree remains clean except for the three intended, unstaged modifications; the harness should commit them. No remote merge is requested while the exact actual proof is failed/held. Recommended next step is an orchestrator/Runtime diagnosis of the publication-identity mismatch before any separately authorized live proof and HOME owner final gate.
