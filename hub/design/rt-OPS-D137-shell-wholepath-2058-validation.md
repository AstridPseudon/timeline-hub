# D137 whole-path source validation

## Result

`SOURCE_CLOSURE_DEFECT_PROVED`. The production child-shell context at
`ops-child-custody/make-child-venv:385` is not transitively closed. It exports
`failure`, `run_stage`, `progress`, and `source_state`, but `run_stage` calls
`stage_stderr_path` and `failure` calls `retain_stage_stderr`. The first recipe
stage is `venv`, so the reported `venv-log-setup` refusal is explained by the
source. The later nonzero/timeout path has a second independent handoff defect.

The smallest proved author seam is the existing `declare -f` list: add exactly
`stage_stderr_path` and `retain_stage_stderr`. This worker did not apply that
change. No verifier relaxation, trust change, ownership change, source-control
change, reserve change, registration change, Store change, result-reader change,
or source-writer change was made.

The actual Agent2044/peer2047 result remains authoritative input: one ordinary
request refused at `venv-log-setup`, exit 2, with the safe error
`environment: line 60: stage_stderr_path: command not found`. The actual stderr
payload remains `EXACTMISSING`; no reconstruction and no retry were performed.

## Exact source checks run

All commands were read-only source/hash checks. No unittest, fixture, body,
provider, Store, child, acquisition, full suite, profile, install, or real
request ran.

```text
bash -n ops-child-custody/make-child-venv
PASS (exit 0)

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY' ...
  extract STORE_PY, STORE_VERIFY, STORE_BUILD
  compile embedded Python blocks in memory
  compare each block with HEAD^
  enumerate STORE_CONTEXT functions and variables
  hash protected live helpers
PY
PASS: embedded Python compile; STORE_PY parent_equal=True;
STORE_VERIFY parent_equal=True; STORE_BUILD parent_equal=True

git status --short --branch
PASS: clean worktree on tl/rt-OPS-D137-shell-wholepath-2058

df -h . /tmp
OBSERVED: approximately 4.5 GB free, below the 4.6 GB source floor;
no heavy or body execution was attempted.
```

Computed hashes:

| item | value |
| --- | --- |
| maker source | `4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`, 75,503 bytes, `0755` |
| source commit/tree | `0c4170e42d2ff435ea855a54c940299619f6a285` / `b43a840b75bf895f9789732c56585175c4b367bf` |
| `STORE_PY` | `0889b24010e67bd31f28f5efbaec37fed43adf1a0d5ebe8c4fcd57a8248ca50c` |
| `STORE_VERIFY` | `f7c7ebcc26221958ce24e36025faad167c6015a2889202752d267e03d5eda209` |
| `STORE_BUILD` | `729036a7bca12cba36b87e39c556a82859d2e5fe76fba102cc6c7b5f86c253c3` |
| live `bench_store.py` | `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2` |
| live `verify_dependency_seed.py` | `116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2` |

## Existing passing evidence and blind spot

The repository validation records 44/44 existing controls passing. They were
not rerun under this read-only assignment. The relevant tests extract a
contiguous range from `failure()` through `run_stage()`, which supplies the two
helpers absent from production `STORE_CONTEXT`. The Store cleanup test also
uses a test-defined `build` callback and manually sets `build.failure_evidence`;
it does not launch the actual embedded `STORE_PY` build shell boundary.

Therefore those passing controls do not qualify the real serialized recipe
closure. A static transitive-closure assertion is the smallest safe regression
shape for this investigation; any later behavioral regression must preserve the
task's no-body/no-Store/no-real-request restrictions until separately authorized.

## Evidence files

- `source-manifest.json`: source, commit, hashes, boundary, and protected-state census.
- `shell-dependencies.json`: exported closure, omitted callees, variable analysis, branch trace, and test blind spot.
- `findings.json`: finite findings and source-owner handoff.
