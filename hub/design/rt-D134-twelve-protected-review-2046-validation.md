# D134 protected review validation

## Result

FAIL for each of the twelve authors' claimed missing-authority findings: seven inverse cases and five history cases. The failures mean the claimed authority absence is not supported. They do not mean that product behavior passed or that a product fault was proved. All twelve live cases remain unqualified.

The review was read-only over source and test files. No source, test, design, hub, branch, or repository metadata was changed.

## Authority review

- Base was exact Agent commit `a30e74e901a28b39c28facba3deb00d76f186e23`, tree `ece8e0887e48e45cb1fce85b1256c49a0f6126c0`.
- The original evidence directories and all four files in each packet were read. Their hashes are recorded in `source-manifest.json`.
- The historical inverse Agent source is available as Git commit `bd3c95b1cebe3bf27c4a82919e5839efb37519db`; its exact `commit.py` and `inverse.py` hashes match the author's receipt. The current a30 hashes are also available. The mismatch is therefore a finite identity migration seam, not an absent checkout.
- The pinned inverse Runtime source is available as commit `6634a17f3ffd885567ba3c91b6c7a560df7375a4`, with both exact Runtime file hashes matching the author's receipt.
- Gate1's current schema is SHA256 `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`; current `runtime.lock.json` is SHA256 `ad818e99cb0759d1742d9f67b5bb3367b03fd3e88d8f65846253169272b8b6ce` and names source commit `ab1e4f6141987706132916e2da16477f5a019464`. The old literals are stale OUR test guards, not missing source.
- The prepared test's historical Runtime `369ffa7c00bd3d45c610fac7651ff79e7a283a1a` and tree `9bf331d68df8c966e8927a3f083ba03687803c99` are available; the current lock tuple is also available. The hash difference alone does not prove source unavailability.
- The M1 archive exists at the exact reader default path with SHA256 `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`. `test_current_pair_reader.py` authenticates that path/hash and verifies/restores the backup. The original `originals_xml:null` report field is a malformed evidence link/omission, not an absent archive.
- D120 is the applicable authority for a faithful current-contract OUR-test adaptation. No owner approval gate was inferred. No request/reply shape or authority semantics were changed.

## Twelve-ID and predicate conservation

The twelve exact node IDs are listed in `predicate-map.json`: five parameterized inverse forward cases, two inverse refusal cases, three Gate1 frontend cases, one prepared-video case, and one M1 archive case. The original predicate maps were checked against the unchanged base. Parameters, authored inputs, raises, assertions, identity/privacy/no-write predicates, and the M1 opaque/on/anchor purpose are all conserved. No skip, xfail, relaxation, deletion, or replacement was introduced.

The inverse source boundary remains `_assert_source_identity` at lines 78, 90, and 230. The history boundaries remain Gate1 line 67, prepared line 251, and M1 line 133. These are setup/identity boundaries; they are not behavior results.

## Static commands

All commands ran against the exact four assigned files, with private Ruff/compile/mypy caches outside the worktree:

```text
RUFF_CACHE_DIR=/tmp/d134-ruff-cache /home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py tests/editing_conformance/test_prepared_video_birth.py tests/editing_conformance/test_m1_legacy_archive_read.py tests/editing_conformance/test_inverse_stage_runtime_regressions.py
PASS — All checks passed!

PYTHONPYCACHEPREFIX=/tmp/d134-pycache /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py tests/editing_conformance/test_prepared_video_birth.py tests/editing_conformance/test_m1_legacy_archive_read.py tests/editing_conformance/test_inverse_stage_runtime_regressions.py
PASS — exit 0

MYPY_CACHE_DIR=/tmp/d134-mypy-cache /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/d134-mypy-cache --config-file pyproject.toml tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py tests/editing_conformance/test_prepared_video_birth.py tests/editing_conformance/test_m1_legacy_archive_read.py tests/editing_conformance/test_inverse_stage_runtime_regressions.py
PASS — Success: no issues found in 4 source files

git diff --check
PASS — exit 0
```

## Functional status and next step

No pytest, provider, body, collection, browser, socket, RuntimeService, acquisition, family, P1-P5, D130, or full suite was run. Observed free space was `4,662,390,784` bytes, below the mandated 5,000,000,000-byte functional floor but above the 4,000,000,000-byte source-only stop line. The next authorized step is to apply one of the four finite corrections in `findings.json` through the existing approved authority, then run the twelve live cases only when the central test service and disk floor admit it.
