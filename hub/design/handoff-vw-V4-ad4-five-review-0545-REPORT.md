# V4 independent FAIL review: branch-five `ac9870277`

## Result

**FAIL.** The reviewed branch is not product-ready and must not merge. The
preserved branch-five run has the requested observed result: **2 PASS, 1 FAIL,
2 ERROR**. The two permitted passing controls independently pass, but that
does not qualify V4 or the 52/54/native/integrated suites.

No product, test, generated, pin, package, or recipe files were changed. No
source branch was merged. D14's two equal-text undo cases remain unchanged,
unskipped, and un-xfailed in the exact `5292b388…` test blob.

## Reviewed identities and custody

- Reviewed HEAD/base: `ac9870277873f445921424fa4edf65e04fe443b1`.
- Agent V2 source commits are present exactly: `e50beb3063df13b5faa86896eb5161ba1df8cb54` (FPS) and `ad4e459a32d9abbbe28794fb13ef45b1b9cd6893` (word-anchor D12).
- The normal Agent/client source is `f894c3c9dda25ab03527eeb7f52da5da31d627c1`; its Runtime client lock names official producer source `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Runtime checkout used by the permitted test is exactly `ad823e0a0f5be4a7acf1d3006df6f794709da63d`.
- `runtime.lock.json` has 15 entries. Consumer bytes and all 15 producer bytes at `34eac…` both match (PASS); `python scripts/vendor_lock.py check runtime.lock.json` also passes.
- `tests/editing_conformance/native_word_anchor_fixture.py` is blob `af7407a5…`, exactly the fixture blob in `5292b388…` and the created-claim output of `38e8063162a36a87369561c581bc18fe8fbef37c`.
- `tests/editing_conformance/test_native_word_anchor.py` is blob `5db819f4…`, exactly the `5292b388…` test blob.
- The earlier omitted-created problem from `old9cf…` is therefore fixed by the exact `created: ["parent/track:initial"]` claim at fixture lines 194–196. The new traces occur after that command identity succeeds; they are not attributed to the old problem.

## Evidence run

The existing first native-anchor log at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-V4-branch-five-0542/native-word-anchor-original5.log`
records the allowed five-case command once:

```text
2 passed, 2 errors, 1 failed, 49 deselected in 5.67s
```

Its exact outcomes are:

1. PASS: `native_move_refuses_anchor_basis_until_explicit_clear`.
2. PASS: `half_open_window_and_exact_rational_fps_are_validated_at_acceptance`.
3. ERROR at fixture setup: `short-occurrence`.
4. ERROR at fixture setup: `raw-source-window`.
5. FAIL at fixture setup: `stale_anchor_refuses_when_intervening_window_excludes_selected_word`.

Independent allowed controls, run once with the exact requested command:

```sh
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py -k 'native_move_refuses_anchor_basis_until_explicit_clear or half_open_window_and_exact_rational_fps_are_validated_at_acceptance'
```

Result: **2 passed, 52 deselected in 2.69s**.

Additional checks:

```sh
ruff check --no-cache tests/editing_conformance/native_word_anchor_fixture.py tests/editing_conformance/test_native_word_anchor.py
git diff --check ac9870277873f445921424fa4edf65e04fe443b1
git diff --check ac9870277873f445921424fa4edf65e04fe443b1^ ac9870277873f445921424fa4edf65e04fe443b1
python scripts/vendor_lock.py check runtime.lock.json
```

Results: Ruff PASS; both diff checks PASS; vendor lock PASS. A separate
read-only comparison of all 15 lock entries against producer source
`34eac…` also passed for consumer and producer bytes.

No 54-case rerun, native14, full, browser, localhost, or heavy suite was run.

## Exact causal findings

### ERROR 1: short occurrence is rejected before the anchor command

The fixture parameter is `duration_ms=100`
(`native_word_anchor_fixture.py:67–90`, `test_native_word_anchor.py:111–114`).
The retained child voice clip is authored with `at=1`, `from=2`, `to=6`,
and `speed=2`, so its timeline duration is `(6 - 2) / 2 = 2` seconds
while the occurrence bound is `0.1` seconds.

The real production path is Runtime `commit_timeline` →
`agent.create_runtime_commit_service()` → `commit.py:1119` →
`validate_final_candidate`. The existing Agent V2 validator computes the
bound at `validation.py:446–461`; `_validate_clip_list` rejects at
`validation.py:229–231` with:

```text
candidate.shots['shot'].internal_timeline.clips['voice']: timeline interval must fit the occurrence's half-open bounds
```

The error occurs during the fixture's initial `track.create` at
`native_word_anchor_fixture.py:194–196`, before `clip.anchor` is attempted.
This is owned by the existing Agent V2 final-candidate validation path (the
G234/R3/V2 owner handback), not Runtime/client identity. Any correction must
scope D12a only as settled, retaining the interval guard for an actually
involved write; this review makes no waiver.

### ERROR 2: raw source map is rejected before the anchor command

The fixture parameter adds `source_window={"from":20,"to":30}` at
`native_word_anchor_fixture.py:91–92`. The initial unrelated `track.create`
again reaches `commit.py:1119` and final timing validation. The existing
timing kernel rejects every explicit `source_window`/`time_map`/related map
in `astrid/sdk/timeline/_timing_evaluators.py:48–51`:

```text
('occ', 'shot', 'voice'): unsupported explicit map source_window
```

`validate_candidate_timing` propagates this through
`_commit_timing_validation.py:379`, `validation.py:480–482`, and
`commit.py:1158–1160` classifies the base-invalid candidate. The intended
`clip.anchor` source-map guard is not reached. This is the same existing
Agent V2/G234 final-candidate ownership boundary; preserve the unsupported
source-map guard and do not blame the fixed `created` claim.

### FAIL: ad4 D12 sees the stale source change as a real legacy-word invalidation

The test asks the fixture to land `fixture.window` with `from=4,to=6` at
`test_native_word_anchor.py:521–531`. The retained legacy parent declaration
is still the word expression containing `"again"`; the selected transcript
word is at source time 3–3.5. With `from=4`, the word is outside the source
clip's half-open search interval.

The new `ad4e459a…` D12 source makes this causal rather than a generic byte
comparison. `_reference_basis` now includes the complete word-search context
at `_commit_timing_validation.py:83–100`, including physical source clips and
timing inputs; `_legacy_exemptions` requires exact basis equality at lines
258–261. The `from` geometry change is consequently not exempted. Final
validation then enters `validate_candidate_timing` and calls
`legacy_binding` at line 351; `native_word_anchor.py:144–169` filters words
by the half-open `from`/`to` bounds and raises:

```text
candidate.timing: legacy word anchor is missing
```

The preserved log shows this exact chain and the `legacy_binding` frame. The
source facts support a genuinely modified/invalidated declaration basis: the
changed source geometry is part of the legacy word lookup, not unrelated
layout. This is not evidence that ad4 overcounts arbitrary geometry. It also
means the test cannot reach its later stale-replay conflict assertion on this
tree. The existing Agent V2/G234 owner must decide the narrow D12a handling of
this involved source-window write while preserving authored source/word data,
physical-owner checks, and semantic guards; no policy waiver or source edit is
made here.

## Production caller and readiness boundary

This is not a detached unit-only path. The fixture registers
`agent.create_runtime_commit_service()` at `native_word_anchor_fixture.py:185`
and calls the real Runtime `commit_timeline`. The production chain is:

```text
RuntimeService.commit_timeline
  -> Runtime coordinator / RequestCommitPort
  -> Agent RuntimeCommitService.commit
  -> validate_final_candidate
  -> port.accept(prepared) or port.preview(prepared)
```

The failing traces reach Agent final validation before acceptance, so they are
real provider behavior. The two passing controls are valid evidence only for
those controls. Overall product readiness is **FAIL**; no 52/54 or integrated
PASS is claimed.

## Handback

Agent existing V2/G234/R3 owner: consume the three exact traces above. Keep
the fixed creation claim, exact test blobs, normal client `34eac…`, Runtime
`ad823…`, current normalizers, authored source/word/physical ownership, and
all semantic guards. Resolve only the scoped validation/ownership behavior
required by the settled D12a/C0 decisions, then qualify a meaningful successor
before any later 54/integrated run. No code was changed by this review.
