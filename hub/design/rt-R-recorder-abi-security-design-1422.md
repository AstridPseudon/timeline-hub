# Security design report

Verdict: **blocked; no sound existing ABI authority source**. No Runtime, schema, client, Agent, or test changes made. `DONE` created.

Reviewed:

- Plan and D61/R2r materials.
- Sol1410 source/attack packet, XML, test, and source facts.
- Agent whole-path 1354 design/escalation and current consumer paths.
- Runtime at `4386016c01474fc09b037c80edc1a36b51c1262e`, parent `e68cf231…`.

Findings:

- `_is_v2_request()` can select the validation regime from the authenticated request: v2 iff `label`, `steps`, `merge`, `reads`, or `doc.patch` is present; otherwise legacy ABI1. Effective merge mode must still apply the conservative omitted-`reads`/`doc.patch` rule.
- This is validated request-mode selection, not recorder authority. `recorder_abi` must never be accepted from the caller or provider record.
- Current `validate_bindings()` skips bindings without `physical_ref`; one Recorder schema accepts both modes. Therefore annotation presence, physical-field absence, or a copied provider flag cannot establish ABI2.
- Existing acceptance accepts both stripped-v2 and FULL-REWRITE captures. FULL-REWRITE can become exactly the genuine four-binding ABI1 shape while retaining v2 request annotations.

Smallest sound Runtime proposal:

1. Derive ABI mode from the sealed, validated request and effective merge mode.
2. For ABI2, require exact authenticated coverage—not subset coverage—over:
   - all command reads, including timeline expansion to every closure image;
   - collection membership and order;
   - native selections and their owner/order observations;
   - authored and derived physical writes;
   - every generated `commit.effect` for each step-patch effect, with exact ordinal/path/side and authenticated before/after image;
   - complete `commit.materialization` source/successor pairs, owner lists, and edge-before/edge-after links;
   - complete `commit.atomic` touched-scope coverage where applicable;
   - all other v2-enriched native bindings, with only explicitly authenticated stage-marker exceptions such as `inverse.stage`.
3. Reject duplicate, missing, extra, or partially physical binding sets before persistence.
4. Return a private validated result such as `(recorder_abi, coverage_digest)` from Runtime validation into `_publish`; do not recompute it from mutable metadata.
5. Commit the mode into the accepted event payload and history metadata, cross-checking both during replay/history verification. New authority pairs must be all-present or rejected.
6. Only pre-change history lacking the fact may default to ABI1. Genuine legacy records remain accepted under legacy rules; do not weaken the existing Agent guard.

Attack cases that must refuse without writes:

- Strip physical fields from v2 bindings.
- Rewrite all bindings to the four legacy keys and remove `commit.effect`.
- Retain only some physical bindings while omitting reads, effects, materialization, atomic scopes, or derived-write coverage.
- Supply `recorder_abi` as `1`, `2`, malformed, boolean, numeric, or object caller data.
- Tamper with history metadata, accepted-event mode, records digest, or mode/metadata disagreement.
- Downgrade authenticated ABI2 history to absent/ABI1; Agent must refuse.
- Preserve genuine ABI1 acceptance and exact retry behavior.

The genuine ABI1 fork currently reaches an existing Agent `fork source binding changed` guard before Runtime; this is a separate compatibility issue and must not be bypassed.

Evidence commands/results from Sol1410 (not rerun per brief):

```text
... pytest tests/test_timeline_recorder_abi_authority.py \
tests/test_timeline_commit_authentication.py \
tests/test_timeline_commit_sequential_verifier.py
192 passed, 14 failed
```

All 14 failures were the intended new authority controls. Existing authentication/sequential tests passed.

```text
... pytest tests/test_timeline_commit_port.py
94 passed
```

Local final checks: clean status, `git diff --check` passed, source identity/hash checks completed. No full suite, browser, HTTP, or product qualification run.