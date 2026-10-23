# F-D22 audio final-1542

Verdict: **PASS**, bounded to Agent candidate `8d5a368f7` plus the final
documentation diff.

## Scope

The only repository changes are:

- `docs/design/audio-compile-contract.md`
- `docs/design/visual-compile-contract.md`

The reviewed test and JSON blobs remain byte-identical to `8d5a368f7`:

```text
tests/editing_conformance/test_compile_contracts.py  519a2aa5431aa8ad324f88cc649ff2bdc631f55d3e8b7b482a8e1200d3e37b4a
tests/editing_conformance/fixtures/audio_compile_contract.json  32f38f92df0af531823fed84895f65d4e1f30d2d5dea773818fefb5f714873a7
```

`git diff --quiet 8d5a368f7 --` over those two paths passed. `git diff
--check` passed.

## Exact profile and tests

The approved exact profile run used Runtime checkout
`/home/user/work/wt/rt-pin-9ce4242b` at
`9ce4242bc01f100bab9efc51032a73985cefb2b2`, Node `v20.19.4`, Agent Python
`3.13.16`, and profile
`/home/user/work/runtimes/agent-remotion-v3-819acf-1110`. The two original
audio fade nodes ran once and passed:

```text
tests/editing_conformance/test_compile_contracts.py::test_audio_vector[fade-in-needs-prepared-envelope-source]
tests/editing_conformance/test_compile_contracts.py::test_audio_vector[fade-out-needs-prepared-envelope-source]
2 passed in 2.29s
```

Profile verification:

- package-lock SHA-256:
  `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`;
- approved source archive SHA-256:
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`;
- actual JS module:
  `/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules/@banodoco/timeline-composition/dist/index.js`;
- actual JS module SHA-256:
  `cee41ba08f5cea25d8451fed086ad8fa4bff73e9f41b2a161f5d59cb125827e1`;
- installed Composition version: `0.0.14`.

The private typecheck command
`/home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline`
returned `Mypy findings: current=1912 baseline=1912` (**PASS**, zero added).
Review-1534 scoped Ruff `2149/2149` and trusted source/digest/attempt
negative-control evidence were reused. The prior generic 58-case run is
explicitly not represented as exact 819acf execution; it used Composition
`0.0.14`.

## Documentation acceptance

The audio contract now records that `root_preparation.py` calls
`prepare_normal_audio_sources` from `normal_audio.py`; that boundary verifies
managed source identity and creates attempt-owned prepared output using the
public Composition envelope policy. Pure logical projection remains unable to
invent `audio.render_source`, and absent/mismatched prepared sources still
refuse. Vectors 10–11 are no longer described as strict xfails: they pass
through the bounded trusted preparation fixture. The visual contract has only
a minimal cross-reference correction and makes no audio PCM/parity claim.

No product/test/schema/client/pin/archive/dependency change was made. No full
or browser/live suite was run. Separate sliced-source PCM acceptance and
renderer/App parity remain unverified. Next step is manager/queue integration;
no merge was performed.
