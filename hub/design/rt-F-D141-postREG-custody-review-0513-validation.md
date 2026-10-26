# D141 final integrated custody validation

Verdicts: PASS for exact-15 source custody, PASS for the corrected real-15 producer mapping, and PASS for retained P5 applicability. Qualification is limited to zero of these 15 REG selectors; no full-suite GO.

## Evidence read in place

- `PLAN.md`, C0/BOARD-HEADER/D141 cut and freeze2 controls were read before review.
- Runtime actual head: `95d98f038320d5d46bd679ac000ab3e15825c935`, tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`.
- Agent actual head: `8585ed9c0404d0187b2ce70242d25114a32747c2`, tree `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`.
- App actual head: `5344c53e3063001bb3255bd0c9cd32cc5e77967f`, tree `dd989783046aeff652486a1ba39db42aea86e201`.
- All three source checkouts were clean when inspected.
- The retained exact-15 stdout is `/tmp/rt-F-D141-postREG-integrated-proof-JfAg26/pytest.log`; it reads `15 passed in 5.79s`. The retained private directory has no XML, run-exit, or separate counts file; this is disclosed rather than inferred.

## Commands/results

These were read-only inspection commands; no test/import/collection/typecheck/lint/generator/install command was rerun.

```text
git -C /home/user/work/runtime show -s --format='%H %T %P' 95d98f038320d5d46bd679ac000ab3e15825c935
PASS 95d98f... 78df31... 857e4c... 012889...

git -C /home/user/work/agent show -s --format='%H %T %P' 8585ed9c0404d0187b2ce70242d25114a32747c2
PASS 8585ed... 92a3ff... 28e56... 5d202...

git -C /home/user/work/runtime diff --name-status 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d 95d98f038320d5d46bd679ac000ab3e15825c935
PASS exactly 3 paths: the two TypeScript generated outputs and runtime_protocol/upgrade.py

git -C /home/user/work/agent diff --name-status 28e56cacb42d3da85b02e5b3543895b44f3d0f70 8585ed9c0404d0187b2ce70242d25114a32747c2
PASS exactly 54 changed paths; all are listed in p5-applicability.json

git -C /home/user/work/runtime diff --quiet 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d 95d98f038320d5d46bd679ac000ab3e15825c935 -- contract/artifacts.json
PASS; producer manifest bytes unchanged

python read-only JSON/hash comparison of Agent runtime.lock.json against Runtime contract/artifacts.json and every Runtime source byte
PASS 15/15 Agent mappings match lock hash, manifest hash, and current source bytes; manifest is byte-equal to 6a

static inspection of Runtime tests/conftest.py, tests/astrid_checkout.py, tests/lanes.py, P5 tests, timeline_commit_provider.py, and App vendor callers
PASS Runtime owns tests.conftest/tests.lanes; Agent changed conftest/lanes are not P5-loaded; no changed Agent path is an executed P5 boundary
```

The previously captured acceptance command was:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q --basetemp=/tmp/rt-F-D141-postREG-integrated-proof-JfAg26/basetemp -o cache_dir=/tmp/rt-F-D141-postREG-integrated-proof-JfAg26/cache <the exact 15 selectors recorded in review.json>
```

Captured result: 15 collected, 15 passed, 0 failed, 0 errors, 0 skipped, 0 xfail; exit 0. It was run once by the prior integrated-proof worker and was not repeated here.

## P5 finding

The prior `runtime-d141-p5-cut-1026013331-6934` receipt remains applicable: 38/38 passed, with its XML retained in place. `runtime_protocol/upgrade.py` is imported by P5 setup, but the changed `_validate_candidate` hunk is reached only through `upgrade_realm`, not the P5 `migrate_canonical_to_current` route. Runtime conftest/lanes resolve from Runtime, not Agent. Therefore no affected executed path requires a new P5 body receipt; no automatic retarget was made. Agent full/P4 obligations remain separate and unchanged.

## Producer correction

The prior `canonical15_artifact_hashes` field is retained as historical evidence but is explicitly ambiguous: it contains REG test source-body hashes, not client artifact mappings. The corrected immutable derivative in `producer-corrected.json` contains all 15 actual Agent `runtime.lock.json` consumer/source/hash mappings. App’s current `runtime.lock.json` has 14 different Runtime consumer entries; its normal vendor tools and the Agent vendor checker are recorded without claiming that App lock is the canonical Agent 15.
