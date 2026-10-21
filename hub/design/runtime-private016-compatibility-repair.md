# Runtime PRIVATE016 compatibility repair

## Result

Repaired the singleton-to-enum compatibility proof on Runtime base
`8610056a330563d4f80be06f19ad4b21076117ea` / tree
`0dbe6ed69c2a3d8ce8e8ad08305233c5ceb8d960`.

The checker now reuses Runtime's existing `value_equal` JSON comparator, which
distinguishes booleans from numbers, compares numeric values semantically, and
recurses through JSON objects/lists. Both const-to-enum waiver branches use
that comparator and require the new schema to omit `const`, so a conflicting
new const cannot be hidden by an enum containing the old value. Existing
required/enum/const/unknown-keyword null-presence strictness remains intact.

Only these repository files changed:

- `generators/command_schema_compatibility.py`
- `tests/test_command_schema_compatibility.py`

## Identity and artifact preservation

- Base commit/tree: `8610056a330563d4f80be06f19ad4b21076117ea` /
  `0dbe6ed69c2a3d8ce8e8ad08305233c5ceb8d960`
- Exact frozen Agent schema source: commit
  `10226a7f08a739ba3e41f8e91de6971eed63aa9d`, tree
  `e2c08fbe9b21a3082db7bcf62d9677babfc15e98`
- Prospective successor source tree after harness commit:
  `671532c57c04ff9b9a9c232f29753fc46d82f423`
- Actual successor commit SHA: pending harness commit; manager must read it
  after worker exit and verify its tree equals the prospective tree above.
- Artifact manifest: 76 artifacts, version
  `sha256:b045b4ecc9bfc026de12b64defa31b064b1187c3638554a129403e6a6356e7d5`.
- Before/after artifact digest comparison: 76/76 byte-identical.

## Tests and checks

- Planted Draft202012 witness (inline Python): PASS for both
  `boolean const false -> enum [0]` and `boolean const true -> enum [1]`;
  each was old-valid, new-invalid, and refused by the checker.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_command_schema_compatibility.py`
  — **134 passed**.
- Exact frozen Agent schema check-only generation using
  `generators/generate.py --check --agent-command-schema <git-show 1022 schema>`
  — **exit 0**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check`
  — **current**.
- `git diff --check` — **passed**.

No actual generation, broad/287/136/native/socket/browser/render/full suite,
pin, merge, or release claim was made. Final combined fix/conversion review
and harness successor verification remain required.
