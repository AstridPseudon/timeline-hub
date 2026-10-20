# Runtime ordinary014 raw-media compose

## Result

Composed the approved b731 optional `media_info` implementation onto the
ordinary014 current-server candidate `202074110717146fc7f08af2306a8dd7f695b0b1`.
The pre-harness candidate tree is:

- candidate commit base: `202074110717146fc7f08af2306a8dd7f695b0b1`
- candidate base tree: `ee39286bd0eb27d4075074cc4785d6d15e33f243`
- candidate successor tree: `dcece2a11c40dfd71cdebb764b449796f9c06504`
- harness-assigned successor commit: pending; do not cite the uncommitted tree
  as a commit SHA

The immutable official producer remains Runtime `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`. Artifact identity remains
`sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`,
with manifest SHA-256
`ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`, wire
digest `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`,
75 artifact paths, 55 definitions, and 29 operations.

## Source delta

Exactly three paths differ from the base:

- `runtime_protocol/timeline_commit.py`: private `MediaInfo` shape and
  `RuntimeCommitPort.media_info` declaration.
- `runtime_protocol/timeline_commit_port.py`: exact declared-pin memoized read,
  same-descriptor CAS verification/WAV parsing/recheck, and acceptance recheck.
- `tests/test_timeline_raw_audio_port.py`: seven raw-media regression cases.

The three file contents match the approved b731 implementation byte-for-byte.
No generated contract, schema, DTO, public route, package/version pin, table,
inline duration, private carrier, or artifact was changed. The carried parent
strict pending test marker in `tests/test_timeline_clip_replacement.py` remains
unchanged. Existing CAS/catalog/text/fence/clip/c45/audit/shell behavior is
preserved.

## Tests

Passed the requested focused lane:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_raw_audio_port.py tests/test_timeline_commit_port.py tests/test_timeline_commit_contract.py
```

Result: **71 passed in 32.12s**.

Passed normal reproducibility checks:

```text
/home/user/work/venv-runtime/bin/python generators/generate.py --check
/home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --check --source-root "$PWD" --fixture-root "$PWD/conformance/fixtures"
```

The generator and TypeScript checks exited successfully; the artifact check
reported `contract/artifacts.json is current`. Also passed Python compilation,
`git diff --check`, exact b731 selected-file comparisons, and candidate-tree
path/identity checks.

## Qualification boundary

The private seam is intended to be consumed through the real RuntimeService
commit provider and the normal authenticated, project-scoped `/v1` commit route
after the existing health/door handshake. It adds no raw-media HTTP endpoint
and does not bypass health, origin, credential, or project checks. HTTP scope is
therefore the existing commit route only; a real HTTP pair was not run here.

The Agent review of `9bf503f9` found a blocker: b731 accepts a same-project,
request-declared raw pin absent from the accepted base revision closure, while
the approved e220 behavior refuses that pin. This worker deliberately retained
the requested b731 implementation and did not make an unsanctioned authority
change. Native Agent/Runtime, HTTP, and CLI qualification remain **HOLD** until
the separate `rt-m2-raw-base-eligibility-fix` produces a reviewed successor and
the bounded pair is rerun. No native-pair duplicate or broad/full suite was run.

## Next step

Replace the pending successor commit placeholder with the harness-assigned SHA,
then rerun the one bounded Agent native pair against that exact commit/tree
after the base-closure fix is reviewed. Keep public 0.2.13 integration and
ordinary014 artifact adoption held until that qualification passes.
