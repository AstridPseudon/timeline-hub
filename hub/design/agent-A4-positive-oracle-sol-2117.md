Completed the oracle repair in the single allowed test file.

Expected fields now use captured patch values matched by ID/path. The subminimum case explicitly requires anchor hold `0`, inserted hold `0.0667`, and later position `5.0667`. Other anchors remain exact. Added whole-payload comparison, including the config mirror. No timing executor or fabricated authority was added.

Verification commands and results:

```bash
F=tests/editing_conformance/test_a4_after_positive_doc_patch_witness.py
P=/home/user/work/venv-agent/bin/python
export PYTHONDONTWRITEBYTECODE=1
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f
export PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f

$P "$TMPDIR/a4-offline-audit.py"
$P -m pytest --collect-only -q -o addopts= -p no:cacheprovider "$F"
$P -m ruff check --no-cache "$F"
/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --no-incremental --cache-dir "$TMPDIR/a4-fidelity-mypy" "$F"
$P scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
$P scripts/artifact_manifest.py --check
git diff --check
```

All passed: offline identity/expected-field assertions **4/4**, collection **4 tests**, lint/typecheck clean, lock and artifacts current. The audit confirmed unchanged packet `33934817…fff8b4`, fixture constructors, omitted-read checks, v2 assertions, and **3,431 outside-file identities**. Runtime `8ea0766f` retains tree `6047ac30`, matching `abd47e68`; frozen producer `34eac004` is clean.

**Static oracle PASS; provider positives remain unqualified.** All four remain unmerged/unaccepted. Prior **4 FAIL / 16 PASS** evidence was retained without rerunning provider bodies. Missing authentic prepared-media authority remains the separate App/Runtime dependency; no acceptance or P1 qualification is claimed.

Next: independent review of this repair, then App/Runtime authority completion. Commit message and empty `DONE` marker written; no Git mutations performed.