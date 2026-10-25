# D134 validation

Source checks pass; this is a source-only correction. No pytest selector, live service, HTTP/socket body, dependency acquisition or central test request was run.

Exact commands, from the assigned worktree unless an absolute script path is shown:

```sh
/usr/bin/python3.11 /tmp/w-fd40272e29/d134-conservation.py
```

PASS (exit 0): Python 3.11 AST and compile; sole inherited delta is the HTTP baseline assignment RHS; all 99 assertion ASTs identical; all request helpers and behavioral bodies byte-identical to inherited; seven UNKNOWN instances byte/AST-identical against original, first-return and inherited source; two existing merged constants retained. Source and AST hashes are in source-manifest.json and predicate-map.json.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-ab1e4f61" /home/user/work/venv-agent/bin/python /tmp/w-fd40272e29/d134-setup-probe.py
```

PASS (exit 0): full commands.execute source probe with the exact extracted fixture request, current Runtime pure empty bootstrap, and the physical baseline operand. Both actual sequential before states validate, and canonical final parent equals the original retired-caller payload exactly. Input dictionaries and baseline remain unchanged. Inherited and naive-present-guard variants fail as independently expected. The complete reproducer and captured states are embedded in setup-proof.md. This is not Runtime acceptance or HTTP gate evidence.

```sh
PYTHONPYCACHEPREFIX=/tmp/w-fd40272e29/pycache /usr/bin/python3.11 -m py_compile tests/sdk/test_timeline_selected_schema_runtime.py
/root/.local/bin/ruff check --no-cache tests/sdk/test_timeline_selected_schema_runtime.py
git diff --check
git diff --check a30e74e901 -- tests/sdk/test_timeline_selected_schema_runtime.py
git merge-base --is-ancestor 4073fb0f84 HEAD
```

All PASS (exit 0). Ruff: `All checks passed!` Private compilation/cache paths only.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-fd40272e29/mypy --config-file pyproject.toml tests/sdk/test_timeline_selected_schema_runtime.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-fd40272e29/mypy-baseline --config-file pyproject.toml /tmp/w-fd40272e29/baseline/test_timeline_selected_schema_runtime.py
```

Both exit 1 with the identical known baseline only: line 15 `Library stubs not installed for "yaml" [import-untyped]`, `Found 1 error in 1 file (checked 1 source file)`. Baseline is a byte copy of `git show HEAD:tests/sdk/test_timeline_selected_schema_runtime.py` in private TMPDIR. No dependencies were installed or modified; no new type errors.

Immutable Runtime source checks: required checkout completion exists at queue/done/checkout-runtime-ab1e4f6141987706132916e2da16477f5a019464; clean `/home/user/work/wt/rt-pin-ab1e4f61`, commit `ab1e4f6141987706132916e2da16477f5a019464`, tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`. Source-only imports resolve Astrid from this worktree and runtime_protocol from that checkout. Origin and source hashes are recorded in source-manifest.json. Read-only free space observation: 5,835,771,904 bytes, above 5 GB; no heavy work.

Live disposition: NOTRUN. No supported central immutable-ab1e own-node route or protected review receipt for this correction has been received. Runtime2053 remains the operational owner. Existing selected4-review2053 prerequisite refusal was not repeated. No mutable Runtime, near-match recipe, alternate producer, or default-deselecting targeted suite was used. `suites.conf` observed SHA-256: `84d3045878ea806439b73b0a5ca983c06371fcac2d42bc8c7e8add0ebfbd3988`.

Next: independently protect-review this two-line previous-value correction, then consume Runtime's supported exact-selector route once with `-o addopts= -m integration`, exact own3 and HTTP own1 selectors, immutable source/origin guards and at least 5 GB free. Stop on any source/prerequisite refusal. No family/full suite is authorized.
