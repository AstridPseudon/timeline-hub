# VW-AUDIO-STEP source-row closure

## Result

Updated only `design/deletion-ledger.viewing.md`. The `VW-AUDIO-STEP`
source row is now **DELETED** under the owner11:48 lighter interim rule.
The separate `VW-AUDIO-STEP-GATE6` subrow is **REQUIRED / OPEN** and is the
sole authority for the remaining physical frame/audio parity obligation.
No D08/D09 row, aggregate ledger, product source, or test was changed.

## Evidence reused

- App source identity: frozen `3ee1900621f5ae27450ce5b1b69a3b7987e4b8c8`,
  tree `38d6f715f05d0c00b89e131c3b8d4ae28a57fd44`; callback removal
  `2e9939810cbe600d1f7cfcf16d987e50bdecaaeb`.
- Agent source identity: `5c5173dcb57669a9d43e5add2674543333f1c6d2`, tree
  `8626f868a3869b23baaca9814adb930e8952e4c7`; callback removal
  `a3ca13cb25ff440288453bc25d82bbf35f2e3700`, activated caller `951e9f412`.
- `handoff-vw-m3-audio-step-source-retirement-REPORT.md` and the completed
  `vw-m3-audio-step-live-consumer-deletion-map/MAP.md` establish that the old
  per-frame callback is absent from both exact live sources.
- Independent App review `app-public13-pcm-independent-review.md` is
  **APPROVE** for the consumer source scope: 132 targeted controls passed and
  the source-clock mutant failed both targeted cases.
- Independent Agent review
  `handoff-vw-m3-current12-pcm-caller-final-review-REPORT.md` is **NARROW
  CALLER: APPROVE**: the original paired neighbors were 232 baseline / 261
  caller, each with one prohibited render deselection and no new failures.
- Named retained assertions are recorded in the ledger: App
  `continuousPCM.contract.test.tsx` and `continuousPCM.lifetime.test.tsx`;
  Agent `normal-audio-sources.test.mjs`, `normal-audio-native-sources.test.mjs`,
  `test_normal_audio_sources.py`, `test_normal_audio_run.py`, and
  `test_normal_audio_source_phase.py` (including the exact source/phase tests).

## Commands and results

No product or physical tests were rerun, per task instruction to reuse the
existing commit/command/log evidence. Documentation validation passed:

```text
LEDGER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.viewing.md
python3 - "$LEDGER" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
lines = p.read_text().splitlines()
source = [line for line in lines if line.startswith('| VW-AUDIO-STEP |')]
physical = [line for line in lines if line.startswith('| VW-AUDIO-STEP-GATE6 |')]
assert len(source) == len(physical) == 1
assert '**DELETED**' in source[0]
assert '**REQUIRED / OPEN**' in physical[0]
assert source[0].count('|') - 1 == physical[0].count('|') - 1 == 8
for needle in ('2e9939810cbe600d1f7cfcf16d987e50bdecaaeb',
               'a3ca13cb25ff440288453bc25d82bbf35f2e3700',
               'continuousPCM.contract.test.tsx',
               'normal-audio-sources.test.mjs',
               'test_normal_audio_source_phase.py'):
    assert needle in source[0]
assert 'sole authority for the physical obligation' in physical[0]
print('PASS: one DELETED source row, one REQUIRED / OPEN physical subrow, exact IDs/tests present')
PY
# PASS: one DELETED source row, one REQUIRED / OPEN physical subrow, exact IDs/tests present

rg -n -C 1 'VW-AUDIO-STEP|VW-AUDIO-STEP-GATE6' \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.viewing.md \
  >/tmp/audio-step-row-check.txt
# PASS: bounded row references emitted
# confirmed the bounded source-row/subrow edit and named source/test evidence

git -C /home/user/work/wt/vw-m4-audio-step-source-row-close-1210 status --short --branch
# clean product worktree on tl/vw-m4-audio-step-source-row-close-1210
```

## Limits / next step

The physical Gate6 requirement remains unqualified: existing 15923 failed
before comparison bodies, 18439 was cancelled after the filename mismatch,
and 1898 failed before request because its authorized source checkout was
absent. No frame, PCM, same-export parity, or planted-negative evidence is
claimed. The next step is the separately assigned farm physical Gate6 run.
