# A4 integrated parent-raw witness — PASS

## Result

Verified the integrated Agent head without changing repository files. The head
is `92d0413ae9565f151560faf7814be84e079d3110`, tree
`91653330b6a6614a70968b5286e7d6d4d06118f2`, with Runtime pin
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.

The delta from `9a095a95178e0bb89ef3b2024d6502d47b35ac25` is exactly the one
reviewed test path:
`tests/editing_conformance/test_a4_parent_media_raw_witness.py`.

- Git blob: `5aafdc44f52008625a66797ac6aaa928e6bf7f9c`
- SHA-256: `59365260cd8ca828b6b1298c610a775a73611e92b96e914372da4c851f615c29`
- 13 collected and 13 passed
- Worktree clean; no product, schema, Runtime, pin, vendor, or artifact changes

## Verification

Exact integrated run, once:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider tests/editing_conformance/test_a4_parent_media_raw_witness.py
.............                                                            [100%]
13 passed in 1.61s
```

The prior independent review’s unchanged-file checks were reused, not rerun:

- Scoped Ruff: `All checks passed!`
- Scoped mypy: `Success: no issues found in 1 source file`
- Credential scan: `0 matches`

Read-only hygiene checks run on this integrated tree:

```text
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
ok runtime.lock.json
/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current
git diff --check
clean worktree: PASS
```

## Coverage and limits

The witness covers the registered `clip.add-media` provider through
`DetachedPort`, including accepted literal-row receipt/replay, raw video/image
hold validation, null field refusals, duplicate source identity, unsupported
`at_ms`/transition input, subminimum/zero timing refusals, structured refusal
details, request-body identity, and source/head/document/history no-write
guards. The accepted case checks preserved opaque/unknown values, canonical
mirrors, created refs, bindings, reads, and `ABSENT` writes.

The settled scope remains unchanged: this does not claim mounted App A2,
HTTP/Runtime auth, obsolete after-anchor capture acceptance, source-clone or
ripple parity, or the old positive cases that remain explicitly unproven.
Existing App implementations/tests and the P1 NO-GO/A4-G5 gates are retained.

No blocker. Recommended next step is normal integration handoff; no additional
neighbor, current-parent14, original-four, browser, HTTP, full, or gate suite
was run.
