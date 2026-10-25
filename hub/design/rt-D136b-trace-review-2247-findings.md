# D136b independent trace review

## Verdict: PASS_SOURCE

The producer trace is source-valid as a conditional finding, but it does not identify the actual cause of original2136. The controlling result remains **UNKNOWN actual B022 cause / NO_GO**: nine setup errors, zero test-body outcomes, exit 1, and the same fail-closed Runtime message at `runtime_protocol/timeline_commit_auth.py:2209`. No product gap, producer author, setup migration, D104 permission, or Runtime guard change is authorized.

## 1. Current-source correction (all stale claims listed)

The trace’s `agent_home` is exact for the sampled checkout at `547e10456250c1b5bcf63b44a50c90ff0563ce1e`, but that checkout is the stale 07:16 `tl/integration` working HEAD. The authoritative D139-integrated Agent integration ref is `cd63be424d62226e3ee5c26fc5ce03227f5394a5`, parent `4c4ee35d5687c4cd40a0e5395efda53aa56f939d`. Runtime `tl/integration` is `f103bb46866999c961a8865636f2e66d544e0c9b`.

Incorrect or unqualified trace claims:

- Trace.md line 9 and the source-manifest `agent_home` entries present `547e…` as the current Agent home. This is a stale sampled home, not the authoritative current integration source.
- Trace.md line 11’s claim that current `CommitPatch.before`, recorder compiler-mirror, and document-manifest handling differ from original is true only for stale `547e…`. At authoritative `cd63…`, `_commit_patch.py`, `_recording.py`, and `commit.py` are the original `90b59…` blobs.
- Trace.md line 79’s “Original/current before differ” is false for authoritative `cd63…`: `_commit_patch.py` is `ac72a2cb8c549393869a96d753a04fc2d88b91ec` at both `90b59…` and `cd63…`.
- The `patch_before_home` citation is exact Git evidence for stale `547e…`, but is not a current-integration citation.
- The original `90b59…` `test_timeline_capture_projection.py` citation truthfully describes the actual2136 source. The authoritative `cd63…` test fixture is different, so that fixture-path claim must not be transferred to current integration.

The correction does not invalidate D136B-PRODUCER-01. Authoring request construction, duplicate operation, command execution, recording, commit patch, preview, document patch, commit service, initializer, and native occurrence source blobs used by the conditional argument are byte-identical from actual2136 `90b59…` to authoritative `cd63…`; the authoritative changes are `_command_state.py` (the reviewed20db blob) and the projection test fixture. Runtime auth/port/store/coordinator/provider and the selected controls remain byte-identical from `ab1e…` to `f103…`; Runtime service differs only in the unrelated output filename storage line.

## 2. Conditional producer/consumer finding

The source path can **possibly** produce the missing observation under this exact shape:

| Boundary | Source correspondence |
| --- | --- |
| Producer | `authoring_commit_request` runs `_materialize_duplicates` on the preceding bundle, puts every semantic command in one `structure` step with `command_ordinals = range(semantic_count)`. |
| Native birth | `occurrence_duplicate` / `copy_child` writes `shot:<destination>` (owner `None`) and then `occurrence:<destination>` (owner `parent`); `Recording.create_entity` records absent-to-present writes and created roots. |
| Following command | The next independent duplicate reads/binds/writes its own destination and does not name the prior destination occurrence. A physical `commit.input` pin is not a native occurrence reference. |
| Projection | `_project_created_child` only projects a birth when immediately following refs name that same occurrence or a descendant. The prior independent birth is therefore not projected; its paired shot root also lacks the authenticated fork-owner path. |
| Output | `command_output` processes the real native shot-root write. `native_site` normalizes a native `shot:<id>` root to `timeline`, `[]`; `images()` contains parent, `shot-revision:*`, and `internal-revision:*`, not `timeline`. B022 therefore refuses before private captured-output comparison or persistence. |

This is a valid conditional source contradiction, not proof that the nine observed failures took this branch. The private input/output capture, effects, materializations, and binding payloads cannot repair a missing native projection because reconstruction precedes private-output equality. Exact invocation, step, ordinal, record, ref, owner, before/after, and resolved physical coordinates remain unavailable and are **UNKNOWN**.

## 3. Controls and limits

- D100 candidate27 is a single guarded item birth inside an existing physical shot; accepted readback and wrong-previous no-write are valid controls but do not cover grouped independent root births.
- Strict sequential controls create an occurrence and immediately consume that same native owner. Their accepted fields/atomic and separate-step cases, plus foreign/future/ambiguous/owner/input/scope refusals, do not cover two independent duplicates.
- App2211/final2220’s controlling inventory passes its finite identity review: 16 source files, 6 groups, 45 rows, 30 condition maps, 31 AST blocks, 75 definitions, 307 helper calls, 9 final predicates, and 6 parameter values. It grants no dynamic qualification; B022 remains the only observed refusal and all downstream rows remain UNKNOWN/unreached.
- Original2136 and independent2144 remain exact: original9 is FAIL/HELD and overall NO_GO. No private raw capture was read, copied, or requested.

## 4. Disposition

PASS_SOURCE applies only to source consistency, exact Git objects, citations, and finite inventory. The finding is unapplied and must go to the Runtime manager/orchestrator before any Agent R1/G3 authoring decision. No step split, capture invention, future/current physical-ID guess, payload substitution, setup publication bypass, consumer exception, or guard relaxation is proposed.
