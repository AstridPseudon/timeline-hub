# Runtime ordinary014 base-fix compose

## Result

Applied the exact `dcac221296ef2c73e02d30534effb2a09d9a91bd` base-eligibility
guard onto Runtime candidate `6798c6986d85601450a3d8dc25d10befeb1e92c7`.
The working tree delta is exactly two paths and exactly the dcac patch:

- `runtime_protocol/timeline_commit_port.py`: validate an exact raw media pin,
  require it in the authenticated request's original base closure, then retain
  the existing declared-pin memo and acceptance recheck.
- `tests/test_timeline_raw_audio_port.py`: add the same-project out-of-base
  refusal with a base-pin control.

The 6798 base remains the true merge candidate with parents
`202074110717146fc7f08af2306a8dd7f695b0b1` and
`b73139121169b72a2af9371f7808999ee91a1471`; its pre-edit tree is
`dcece2a11c40dfd71cdebb764b449796f9c06504`. The harness-assigned successor
commit and post-edit tree are pending and must replace this placeholder after
the harness commits the worktree.

## Preserved identity and scope

- Official immutable producer: Runtime `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`.
- Runtime wire digest: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Artifact version: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`.
- Artifact manifest: 75 paths, 55 definitions, 29 operations; generated and
  public contract bytes were not changed.
- No private carrier, schema, DTO, endpoint, release/version, catalog/CAS,
  fence, clip, c45, audit, or provider/health/auth bypass was added.
- The existing strict pending retired-route marker and positive assertions
  remain unchanged.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_raw_audio_port.py tests/test_timeline_commit_port.py tests/test_timeline_commit_contract.py tests/test_timeline_commit_acceptance.py
131 passed, 1 deselected in 37.74s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_raw_audio_port.py
8 passed in 5.67s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python generators/generate.py --check
passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
contract/artifacts.json is current

git diff --check
passed
```

No full suite, live HTTP/socket lane, Agent consumer pair, native legacy-trim
qualification, or post-harness artifact handoff was run. The new committed
SHA/tree and immutable a0/ce378 identity must be sent to the Agent INBOX only
after the harness assigns the commit.
