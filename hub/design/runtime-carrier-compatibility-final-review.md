# Runtime carrier compatibility — independent final review

Date: 2026-10-20 UTC

## Decision

**APPROVE** exact repair commit `62b5f8ea1a177879be8ddabf045795b735924e1f` for composition review. This is approval of the conservative compatibility-proof repair only; it is not public pinning, merge, activation, or release approval.

## Exact source/tree reviewed

- Runtime review tree: `62b5f8e` (`fix(generator): prove historical schema containment through widenings`), parent `7f6dd8920e1ceec41b137358df5e7fecc304888d`.
- Diff is limited to `generators/command_schema_compatibility.py` and `tests/test_command_schema_compatibility.py`.
- Exact Agent private source: commit `3730d0bd51686a1692450359482205df64dcc839`, `astrid/core/timeline/schema/edit-command.schema.json`, SHA-256 `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`.
- The public Runtime 0.2.13 schema remains the distinct S2 fixture/current artifact, SHA-256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`; public artifact manifest SHA-256 remains `129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497`.
- Frozen floor hashes verified: 0.2.2 `460e61c7…`, 0.2.3/0.2.10 `472622c4…`, Agent `0a0ac7ba` `30da4fde…`, Agent `26ef2bbb` `a6f1aaa9…`.

## Soundness review

The repaired historical path is a valid transitive proof. For exact digest-checked 0.2.2 floor A, it constructs B by copying A and adding exactly the five already-approved historical alternatives: `asset` to the four identity patterns, standalone `shot` to those patterns, and occurrence tracks to `track.set`. It then runs the existing complete conservative checker on B versus the candidate. Therefore A ⊆ B and B ⊆ candidate imply A ⊆ candidate. The direct check runs first, so unchanged 0.2.2 remains accepted without invoking the compatibility exception.

The candidate is never rewritten, and no allowlist, regex inference, sample proof, new snapshot, or fixture mutation is used. The whole `track.set` v1 branch is retained and checked, including `select`, version, args reference, closed argument properties, and sibling constraints. The `.get()` equality repair distinguishes absent keywords from explicit `null`, so unknown-key presence/removal is reviewed rather than silently treated as equal.

Independent adversarial probes accepted the exact 0.2.2-to-f802 proof, rejected all 32 `$ref` uses and all 16 referenced definitions when given deliberate missing-target/unknown-key mutations, rejected each of the four historical patterns when narrowed, and rejected loss/narrowing of the complete `track.set` clause, closed args, and operation inventory. Inputs remained unchanged after proof calls. The five floors all pass the retained-branch positive tests.

## Evidence

Focused targeted command (shared Runtime venv, no pytest cache/bytecode):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-carrier-compatibility-independent-review-pytest tests/test_command_schema_compatibility.py tests/test_artifact_manifest.py tests/test_generated_client.py::test_generator_is_reproducible tests/test_generated_client.py::test_python_client_source_is_tracked_and_generated_check_is_not_self_referential
```

Result: **169 passed**, exit 0.

Public artifact preservation:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B generators/generate.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B scripts/artifact_manifest.py --check
git diff --check
```

Result: exit 0, `contract/artifacts.json is current`, clean review tree, and the public schema/manifest hashes above unchanged. The explicit `generators/generate.py --check` was also run successfully.

Private f802 archive qualification used an isolated copy of the retained archive under this worker's evidence directory. All four commands passed: normal generation, `generate.py --check`, normal artifact-manifest generation, and `artifact_manifest.py --check`. The generated private schema remained SHA-256 `f80215f2…`; its private artifact manifest was regenerated and checked in that isolated copy.

No full, broad, matrix, localhost, browser, or whole-169 suite was run beyond the requested focused compatibility/artifact lane. No product files, public pins, refs, branches, merges, or shared dependencies were modified.

## Limitation / next step

This review does not qualify the separate carrier peer, native paired integration, public S2 fixture resolution, or composition/release activation. Composition may proceed only under manager/orchestrator review of the approved repair, with the private Agent `3730`/f802 evidence kept distinct from public S2/a6f evidence.
