# Validation

Final exact author/reviewer command, from the Composition worktree:

```bash
E=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-sol-next/evidence
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P "$E/check-source.py" check
```

Final result: exit0, control_status=PASS,
pair_status=BLOCKED_U2_003_NATIVE_CUSTODY, admission_cases=10,
lifecycle_cases=38. Final log:
`privatecontrol-logs/check-1793006061981700787.json`.

- All original 36 lifecycle cases remain, with their original expected exits;
  two measurement-fail cases add actual assertion failures, failing JUnit,
  body exit1 and valid file custody. The fixture pair records cut exit1,
  pristine exit0, final pair exit1 and native custody UNPROVEN. It does not
  turn test failure into PASS.
- Ten native association cases: positive observational readback admitted=false;
  missing summary, request target, suite and duplicate fields, snapshot tree
  and source, resolved row, terminal exit, and raw custody mutation refused.
  These replace self-authored JSON association as the checked surface; they
  are not claimed as ten genuine live admissions. Arbitrary receipt/binding
  admission and production dispatch both explicitly refuse U2-003, exit78.
- Ten operational admission controls execute the exact native classification
  and floor expressions: both same-suite heavy members at inclusive4700000000,
  below-core, one-heavy, global-stop, light below/equal5000000000,
  default-heavy equal/above5200000000, and unreadable disk. They do not run
  test-run, create snapshots, or admit real jobs.
- Actual unchanged D73 launcher: original stub hash38afc8a5..., positive exit17
  with one call, Agent-SHA-only poison exit1 with zero calls. The extra tiny
  assertion launch uses the queue-returned fixture ID and actual D73 output
  files to check launcher manifest/runmanifest/body terminal readback.
- Existing tools/install_p4_launcher.py executes only against an owned private
  fixture registry. Successful restoration and an intervening same-suite edit
  are checked; the latter is retained byte for byte and restore refuses78.
- Native request-test and wait-test source copies change only O to the private
  TMPDIR fixture. A bounded queue dependency actor uses exact native snap and
  terminal source excerpts; polling sleep alone is shortened via a fixture
  dependency. This is not the native daemon, native Git snapshot, trace or
  authenticated receipt. Their omission remains the live blocker.
- Source checks pass all45 retained historical hashes in place, original0735
  file hashes, actual integrated/pristine clean sources and 22/17 selectors,
  native operational-source hashes, distinct manifests, protected tests,
  environment/argv and original floor arithmetic. No host missingness is
  hidden. A host missing inputs must fail the same full checker.

Final syntax/read-only checks (all exit0):

```bash
E=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-sol-next/evidence
bash -n "$E/controller-continuation.sh" "$E/command-cut.sh" "$E/command-pristine.sh" "$E/tiny-controls.sh" "$E/positive-stub.sh"
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P - "$E" <<'PY'
import ast,json,sys
from pathlib import Path
root=Path(sys.argv[1])
for name in ('binding-source.py','check-source.py'):
 ast.parse((root/name).read_text());print('Python AST PASS',name)
for name in ('source-manifest.json','readiness.json','admission-derivation.json'):
 json.loads((root/name).read_text());print('JSON PASS',name)
PY
bash "$E/controller-continuation.sh" check
git diff --check
git status --short
git rev-parse HEAD HEAD^{tree}
```

Controller check reports BLOCKED_U2_003, not source-ready or admitted. Worktree
status remains clean. Base readback is6a2d1c22/tree57f68e1f. All outputs are
outside the Composition tree, so no inherited evidence is added to the repo.

Earlier checker attempts are not hidden: three exited78 during native fixture
construction (one actor timeout after controller refusal; fixed-custody
mismatch on attempted resealing; then an unwritable sealed fixture manifest).
The fixture construction now retains every original sealed identity/hash and
extends only its own generated launcher outputs; production checks were not
relaxed. A later run exited78 at cut/floor-above: monitor and after_wait samples
were appended with a -0.000475-second timestamp inversion. The existing
nondecreasing-time test correctly failed. Both owned recipes now serialize
measurement, timestamp and append using flock on their own trace file; the
unchanged cadence assertion and expected result pass in the final run. This
is a trace-local writer correction, not a lock claimed to govern the daemon.
The passing prior and final control logs remain preserved. Failed fixtures
remain in TMPDIR; nothing was deleted.

No real test-service request, row installation, admission, daemon/test-run,
wait-test, product test/collection/full suite, browser, socket, provider,
Store action or independent review occurred. Product lint/typecheck are N/A:
only external operational shell/Python evidence scripts changed. Shell syntax,
Python AST, and the owned executable source controls are the relevant checks.
C0 runtime behavior, REG0, gates, shipping, and a full suite remain unverified.

Disk samples are our own; no historical trace was copied. The first-tool
five-second observation is followed by a disclosed41.49056455498794-second
start gap before the persistent five-second sampler. This fails uninterrupted
worker-start trace acceptance; it is not backfilled. Actual sampled free space
never crossed the4000000000 stop. Terminal sample/reap facts are appended to
disk-trace.txt and readiness.json. This trace supplies no live admission.

Final own trace summary: {"all_sampled_above_stop": true, "first": "2026-10-26T08:54:19.125800+00:00", "largest_gap_seconds": 41.894135698035825, "minimum_bytes": 4527046656, "sampler_exit": 130, "sampler_reaped": true, "samples": 260, "terminal": "2026-10-26T09:16:47.634032+00:00", "worker_start_continuous": false}.
Sampler session24386 was explicitly interrupted and returned exit130; no live sampler was left running. Terminal sample is an actual post-reap measurement.

Trace limit clarification: besides the initial41.490565-second gap, the actual terminal post-reap sample follows the last sampler entry by41.894136seconds. Both gaps are retained verbatim in readiness.json. No uninterrupted worker trace or live-admission qualification is claimed.
