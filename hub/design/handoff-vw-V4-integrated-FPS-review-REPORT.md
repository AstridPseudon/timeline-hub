# V4 integrated V2 FPS regression/source classification

## Verdict

**FAIL at fixture setup; classification: new Agent V2 invalidity-scope
regression caused by rational-normalization/source contamination.** This is
not a Runtime/client hold and is not evidence that the fixture's intended FPS
claim is malformed. The five selected cases never reached their assertions.
There is no V4, 52, or 54 completion claim here.

The fixture intentionally carries the same 30000/1001 rate in two existing
representations required by the current seam:

| authored location | source | value | Agent V2 interpretation |
| --- | --- | --- | --- |
| `candidate.parent.config.output.fps` | `tests/editing_conformance/native_word_anchor_fixture.py:109` | Python/JSON number `30000 / 1001` (`29.97002997002997`) | `_time_fraction`/`Fraction(str(value))` -> `2997002997002997/100000000000000` |
| `candidate.parent.config.theme_overrides.visual.canvas.fps` | `native_word_anchor_fixture.py:110`, `FPS` at line 26 | `{"numerator": 30000, "denominator": 1001}` | `Fraction(30000, 1001)` -> `30000/1001` |

Those fractions are unequal. The fixture comment at lines 107–108 records why
the numeric output spelling is retained: the legacy publication seam accepts
numeric `output.fps`, while the canvas carries the exact rational consumed by
the timing compiler. The numeric and rational values therefore express the
same intended rate even though the current check treats them as different
exact rates.

## Exact identities and retained dependencies

- Actual integrated Agent: `f95f1e1691b82dce74a49eb7ca444f97eb364037`;
  tree `a356b2d27e4228db745bfd61e27dd088b0dec1d7`.
- Fresh proof-only branch: `55a9af39b6dea29d87251ccf4ad5b8addaa3833b`;
  tree `a356b2d27e4228db745bfd61e27dd088b0dec1d7`. Full tree equality passed.
- Approved donor `5292b388a`: the two current blobs are exact:
  - `native_word_anchor_fixture.py`:
    `af7407a5a2d42bb63b5cc11ba4a4924d3186c607`
  - `test_native_word_anchor.py`:
    `5db819f485da679f613ef04455ec19708d316d6a`
- Current post-import diff from `9729c07b7` contains only those two test paths;
  no recipe or unrelated assertion path changed. The approved status hunks
  are exactly `refused -> invalid` (two acceptance cases) and
  `refused -> conflict` (one stale-head case).
- Runtime checkout is the required frozen
  `ad823e0a0f5be4a7acf1d3006df6f794709da63d`, tree
  `33904550800ee3e2fa34fe0b13c26754b46c7fdc`. The official artifact manifest
  `7c541b70` and all 15 retained map hashes are carried forward from the
  independent normal34 evidence; they are unrelated to this setup failure.

## Causal source trace

The current V2 owner introduced `astrid/sdk/timeline/validation.py` in
`6f4baa07603776840f0a78cc0cf459831bc026af`. Its `_fps`/`_fps_values` logic is
at lines 52–105; line 63 routes numeric values through `_number`, and lines
103–104 reject unequal normalized values with the observed message. The
integrated tree also contains D12 commit
`89c700aded947a4c498043e0f1a46b4ab3e0a873` via merge `9729c07b7`, but D12's
shared-physical-beat fallback is in
`_commit_timing_validation.py`; it does not author or mutate FPS.

The failure is scope-widened because `commit.py:1114–1119` calls
`validate_final_candidate` for the candidate of every commit, including this
fixture's unrelated initial `track.create`. The operation itself is
`capture.py:235–237`: it only calls `ctx.create(owner, 'track', row)` and does
not alter any FPS field. The fixture's created reference at
`native_word_anchor_fixture.py:194–196` is valid and was added solely for the
provider's created-identity claim.

The real production path is preserved and traced: Runtime
`service.py:2434–2478` validates the scoped route/body, authorization,
idempotency context and invokes the registered provider through the
coordinator; Agent `commit.py:1114` performs the failing provider-side final
validation before `commit.py:1143–1144` calls Runtime `port.preview`/`port.accept`.
Runtime `ad823e0a` is the host of the rejection, not its source.

## D12/C0 expectations and protected behavior

D12 must retain exact rational timing, half-open interval behavior, anchor
resolution, native-created identity claims, and Runtime authority checks. The
valid same-rate claim in this fixture should remain valid without rewriting
authored FPS data. C0's approved status adaptation remains the expected
classification for the eventual cases (`invalid`, `invalid`, `conflict`), but
this run proves none of those assertions because setup fails first.

The two D14 undo positives remain unchanged, unskipped, and visibly failing
known V2 regressions. They were not part of this probe and are not reclassified
here.

## Minimal existing-owner action

The existing Agent V2 owner should repair the current `_fps_values` path in
place: compare equivalent legacy numeric output and exact rational canvas
spellings using the existing canonical rate authority, while continuing to
reject genuinely different, invalid, or non-finite authored rates. The repair
must not rewrite the document, weaken rational/half-open/anchor/created or
authority guards, alter the fixture, or add a competing Runtime/client path.
Then rerun the five scoped cases on the corrected integrated home before any
original-54 proof. This report does not implement or pre-approve that repair.

## Evidence

The one permitted neighbor command was run once, with its complete first
output retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-V4-integrated-FPS-review/neighbor-test-first.log`

```sh
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py::test_native_move_refuses_anchor_basis_until_explicit_clear
```

Result: **exit 1; 1 error in 1.54s**, during `retained` fixture setup at the
initial `track.create`; the final exception is
`candidate: all authored fps values must be the same rational rate`. No
selected assertion ran.

Prior handoff evidence, read but not repeated, reports the five-case selection
as **5 errors, 49 deselected in 5.26s**, with the same setup error. The prior
Ruff and `git diff --check` checks passed. This task made no source, test,
fixture, generated, pin, manifest, package, or repository changes;
`git diff --check` is clean and the worktree is clean. Typecheck/lint are N/A
for this source-unchanged diagnostic; the existing handoff pass is reused.

Blocked next proof: the existing Agent V2 owner must publish the reviewed
normalization/scope correction and home SHA. Only then should the five cases
and later V4 gates be rerun.
