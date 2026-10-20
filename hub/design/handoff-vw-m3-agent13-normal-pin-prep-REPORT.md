# Agent normal public13 pin source — handoff

## Result

Prepared a source-only Agent public13 pin candidate from `tl/integration`.
This branch is **held**: Owner13:25 requires App FIRST, and the App
public13 pin/consumer source (`2b3c` / `35e3` with the corrective 143 cases)
is still under final review. No merge, adoption request, shared install, or
shared dependency mutation was performed.

## Exact identity

- Artifact: `remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz`
- SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- Size: 58,477 bytes
- Regular tar members: 77
- Lock integrity: `sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==`
- Release source remains the existing pure `encodedEnvelopeSource` /
  `EncodedEnvelopeSource` export; no package implementation was changed.

The normal manifest, lock root dependency, lock resolved path/version/integrity,
artifact, sidecar, and Agent package-admission version now agree on 0.0.13.
The old public12 artifact remains byte-identical (`0a7b6152…f0f1a3`) and was
not removed or rewritten. Explicit public12 scene/presenter fixtures remain
unchanged.

## Changed scope

- `remotion/package.json`
- `remotion/package-lock.json`
- `remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz`
- `remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz.sha256`
- Agent’s package admission constant in
  `astrid/core/rendering/remotion_runtime.py` (0.0.12 → 0.0.13), required so
  the exact readiness-positive test accepts the new normal pin
- direct current-pin/readiness tests, plus the current capture hash map

No Runtime client/schema pin, compiler, SDK/provider, renderer behavior,
default-theme behavior, source implementation, dependency, toolchain, or
semver range changed.

## Evidence

- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python3 -B -m pytest -q tests/packs/rendering/test_composition_package.py -m 'not integration'`
  — **6 passed, 1 deselected**. Covers lock/artifact identity, 77 regular
  members, readiness positive, missing/unsafe export negatives, and the new
  public13 valid plus four-forged admission smoke.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python3 -B -m pytest -q tests/core/timeline/test_clip_fields.py::test_render_status_defaults_to_pinned_union_composition tests/journeys/test_journey_plumbing.py::test_renderer_install_problem_names_the_missing_install_and_the_fix`
  — **2 passed**.
- `sha256sum` matched the approved public13 artifact and `cmp` matched the
  copied sidecar.
- `git diff --check` — **passed**.

The public API smoke ran in a pytest-owned temporary extraction using the
artifact bytes and system Node 22; this is overlay-only evidence, not an
installed graph or production qualification. No install, build, browser,
render, socket, network, full suite, or shared dependency/cache mutation was
run. The capture-scene host lane was not run because this sandbox has no
provisioned Node v20.19.4 renderer executable; its current hash map was
updated only for the exact artifact identity.

## Owner-gated next step

After App publishes its qualified13 source and checksum, the owner may
provision an isolated Agent13 renderer leaf, verify all 77 extracted bytes and
the lock integrity, then run the direct current-pin/readiness lane. Do not
install into shared linked peers or request adoption from this branch before
that App publication and owner decision.
