# Runtime carrier final source review

Date: 2026-10-20 UTC

## Decision

**APPROVE — INTERNAL corrected carrier only.**

Reviewed Runtime commit `83fe4a1cc8e79ba6db2f06271097a96ff2e7c59a`, tree
`2d9d740ef22eea3b9ec4899bb8e400251bd6d444`, against `16acbb6ef94a6d8e226ccdc351ba0d96e0b09ea5`.
This approves the corrected private source composition for manager use; it is
not a merge, public pin, release, activation, or native Agent/Runtime pair
qualification.

## Scope and source identity

- The 17-path allowlist is respected. A blob audit found **414 tracked paths
  outside the allowlist with zero mismatches** against `16acbb6`.
- `tests/test_door_transport.py` is allowlisted and byte-identical to the
  base; therefore 16 paths differ in the candidate diff.
- The composed product source has no delta from the prior reviewed composition
  `1cac679992a24b5a28080e15cc76a37e3d060265`; the resume delta is only the
  door-audit test's asynchronous-write wait.
- Carrier hashes are unchanged from the reviewed composition: port
  `28968f683c064af54da4b767618880781a6ec66e80586d462b8b7e2b1f96ee86`, store
  `11252cf2cb3dc5c8fc83cb447d238cd3f7b64a4051ecd1b6086444555fa278a2`, and
  materialization `92ec9b7f105d5e0fd1c5f9e9f2a4602ee3dd005365a570e7ba91a573bb8b31fb`.
- The actual join/root/owner/source/item checks, C4 immutable historical reuse,
  and exact durable-ledger-first paths remain the previously approved paths.
  No new authority source, DTO, endpoint, or version field was introduced.

The exact Agent source is commit `3730d0bd51686a1692450359482205df64dcc839`,
tree `3892a10bcffa9bf520b4c79591637cf3259d6724`, with schema SHA-256
`f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`.
The public floor fixture remains the unchanged
`tests/fixtures/published-command-schemas/agent-26ef2bbb.json`, SHA-256
`a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.

## Correctness checks

The four carrier-specific unapproved xfails from the predecessor are gone:
the two normal-generation cases, the legacy 0.2.2 floor case, and the public
typed-item control are ordinary assertions. The exact public-floor negative
and current typed-item reservation positive remain present and strict.

The current compatibility helper proves the historical floor through the
reviewed transitive widening proof; it does not rewrite the candidate or add
an allowlist. The current public artifact is still validated separately, so
private typed-item acceptance does not weaken the public negative control.

## Tests and commands

All commands used the read-only shared Runtime venv, `PYTHONPATH=$PWD`,
`PYTHONDONTWRITEBYTECODE=1`, `-B`, and private `/tmp` basetemps where
applicable.

```text
python -B generators/generate.py                         PASS
python -B generators/generate.py --check                 PASS
python -B scripts/artifact_manifest.py --check          PASS
git diff --check                                          PASS
```

Focused semantic probes:

```text
pytest -q -p no:cacheprovider \
  tests/test_timeline_materialization_join.py::test_complete_captured_join_previews_original_map_without_writes \
  tests/test_timeline_materialization_authority_review.py::test_public_inputs_cannot_delegate_private_capture_authority \
  tests/test_timeline_projection_ownership.py::test_current_typed_item_creation_claim_is_accepted_and_reserved \
  tests/test_timeline_projection_ownership.py::test_matching_creation_history_is_authenticated
  PASS: 5 passed
```

Compatibility and floor controls:

```text
pytest -q -p no:cacheprovider tests/test_command_schema_compatibility.py
  PASS: 164 passed
pytest -q -p no:cacheprovider tests/test_timeline_projection_ownership.py \
  -k 'frozen_artifact or current_typed_item_creation_claim_is_accepted_and_reserved'
  PASS: 2 passed, 52 deselected
```

One initial exploratory invocation used a guessed, nonexistent test node and
returned pytest exit 4 with no tests collected; it was corrected and is not
counted as evidence. No full suite, broad matrix, browser/live-socket suite,
hand render, or native Agent/Runtime pair was run. No frozen fixture was
changed and no test was skipped or weakened.

## Limits and required next steps

- This is an internal Runtime approval only. Agent peer review remains
  required, followed by one coordinated native `3730` lifecycle/ACK/own-slot/
  global-item pair. Existing focused/neighbor evidence is not relabeled as
  that exact native pair.
- `c45cbc6ba3772ac2cebb5a5c94f91be24231e2d5` contains an additional
  **125-line** `tests/test_render_native_historical_retry.py`. It is outside
  this corrected carrier tree, but must be carried and requalified at the
  future merge; do not overwrite or drop it while merging the carrier.
- The current catalog-promotion restoration `4c1a1a30…` adds a newer catalog
  head prewrite fence after this base. Any future carrier merge must retain
  and requalify that fence rather than overwrite it.
- No merge, publication, public pin, or activation was performed.
