# V2 rational-FPS audit — bounded attribution

Date: 2026-10-23 UTC  
Worker: `agt-V2-rational-fps-audit-0453`  
Agent source: `c79398561e5612d0a393074e6b9a198992d77f5b` (9729-derived)  
Runtime source attempted by the prior replay worker: `ad823e0a0f5be4a7acf1d3006df6f794709da63d`

## Ruling

**The original-word-anchor behavior is unverified.** The one required attempt of
`test_follow_rebases_original_choice_after_source_move_and_reorder[True]` stops
during fixture setup at the first real `track.create`, before the stale-anchor
rebase body. The observed refusal is Agent V2 final validation, not a
Runtime/client/environment defect and not an `AgentFinalCandidateError` diagnosis.

The bounded classification is **fixture-contract discrepancy exposed by a new
V2 cross-location FPS-parity rule**. The historical fixture deliberately mixes
two valid legacy spellings for the intended 30000/1001 clock. Under the exact
normalization already used by the timing code, those spellings are different
fractions, so the literal V2 rule correctly refuses the mixed candidate. There
is no evidence here for relaxing the rule with epsilon, dropping a declaration,
waiving a guard, or adding a pin. This is not a proof that the original-word
test has a valid or invalid rebase result.

## Exact authored values and provenance

The exact R1 replay fixture (`tests/editing_conformance/native_word_anchor_fixture.py`)
seeds the historical parent through public `publish_parent_composition` and
then uses the real Agent provider/Runtime `commit_timeline` path for `track.create`:

| location | authored value | exact value used by V2 |
|---|---|---|
| parent `config.output.fps` | Python `30000 / 1001` | numeric JSON `29.97002997002997` → `2997002997002997/100000000000000` |
| parent `config.theme_overrides.visual.canvas.fps` | `{"numerator": 30000, "denominator": 1001}` | `30000/1001` |
| child `internal_timeline.output.fps` in this R1 seed | absent | not included in `_fps_values` |

The retained source is a real transcript DocumentPin (document identity,
version 1, content digest), and the fixture's original source/word choice is
preserved. The source fixture intentionally uses numeric parent output because
the legacy Runtime visual seam rejects object-valued `output.fps`; it keeps the
exact rational in the canvas location consumed by the timing compiler. The
prior M2 report explicitly says this proves compiler arithmetic, not parity
across old writers/readers.

As corroborating canonical source evidence, the prior R2 fixture adaptation
records the same representation change at both
`/parent_revision/payload/config/output/fps` and
`/internal_timeline_revisions/0/payload/output/fps`: exact
`{"numerator":30000,"denominator":1001}` → numeric
`29.97002997002997`, with the reason “MAIN stores numeric FPS; same rate
expressed as its number input.” That is provenance evidence for the
parent/child representation mismatch, not evidence that the R1 target reached
its child replay body.

## Actual module origin

The production path is real: Runtime service/coordinator invokes the registered
Agent provider, and Agent `astrid/sdk/timeline/commit.py` calls
`validate_final_candidate(...)` immediately before `port.accept` (the traceback
lands at `commit.py:1113` in the cited replay). The refusal originates at
`astrid/sdk/timeline/validation.py:66–104`, where `_fps_values()` gathers
parent output, parent canvas, and any child output and requires exact `Fraction`
equality. It raises at line 104:

```text
candidate: all authored fps values must be the same rational rate
```

Runtime only propagates that provider exception through its normal commit
coordinator. The trace therefore does not support attributing this to Runtime,
the client, or the environment.

## Exact-normalization witness

Read-only pure witness, using the existing Agent normalizers:

```text
numeric repr:                 29.97002997002997
V2 _fps(numeric):              2997002997002997/100000000000000
V2 _fps(rational):             30000/1001
V2 equality:                   False
capture.rate equality:         False
timing compiler canvas mapping: 30000/1001
timing compiler canvas numeric: 2997002997002997/100000000000000
```

The existing timing compiler accepts numeric FPS and rational mapping/list
spellings at its canvas input and preserves exact `Fraction` timing. It does
not itself compare parent `config.output.fps` with canvas or child output. The
existing render-profile decimal parser likewise treats a numeric decimal as
its authored decimal text. No existing seam establishes that the finite
decimal is mathematically equal to 30000/1001. The smallest safe handback is
therefore an owner decision at the existing FPS-normalization boundary, not a
new epsilon or a V2-only equivalence rule.

## Evidence

- Prior exact attempt, read from
  `workers/agt-R1-legacy-replay-fix-0442/log.txt:6077–6770`: one required
  invocation against exact Runtime `ad823e0a…`; setup fails at initial
  `track.create` with the V2 message above. The original word-anchor body is
  not executed. The attempt was not rerun here.
- Current production source: `commit.py:1113` caller and
  `validation.py:52–104` validator.
- Fixture source: `native_word_anchor_fixture.py` FPS seed and retained
  transcript setup.
- Existing timing controls: `tests/sdk/test_timing_compiler.py` rational
  mapping/list cases and exact frame-offset case.

Targeted controls run here:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_commit_v2_validation.py \
  tests/editing_conformance/test_commit_timing_validation.py \
  tests/sdk/test_timing_compiler.py
→ 98 passed in 7.14s
```

No full suite, browser/socket run, or known-failing 54-body rerun was performed.
No product or test files were changed. No wire PASS or accepted/rebased/merged
word-anchor result is claimed.

## Bounded fix handback

Before another exact replay attempt, the owner must choose one settled policy:

1. Preserve the current exact V2 parity rule and make the historical fixture's
   authored parent/child/output representations coherent at its legacy seed
   boundary; or
2. Approve an explicit existing-normalizer policy for mixed legacy spellings,
   with focused positive/negative controls for equal normalized rates and true
   distinct rates. That policy must retain exact precision and all V2 guards.

Only after that decision should the exact original test be attempted once. The
replay metadata fix in `c79398561` remains a separate, genuine source change;
this audit neither validates nor invalidates its word-choice rebase behavior.
