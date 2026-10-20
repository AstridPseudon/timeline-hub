# D09a/b/c default/partial physical-equivalence prep

## Result

Offline prep is complete. No Composition source files were changed. The
registered-source qualification extension is intentionally red on the current
source, so retirement of the private crop/statistics path is not qualified:

- `default`: legacy crop is `None`; approved public crop is `(298, 202, 345, 219)` (799 px).
- `partial` (`x=151, y=104`): legacy crop is `(298, 202, 339, 219)`; approved public crop is `(298, 202, 345, 219)` (799 px).

This is a concrete failure of the existing legacy consumer reaching the
component-owned frame-zero compatibility region. The existing
`mouthInspectionRect`/`mouthEraseRect` geometry remains the sole proposal; no
second geometry, guessed default region, blanket refusal, threshold change, or
SDK/private-function deletion was introduced. The existing explicit four-still
qualification remains untouched. Private crop/statistics must remain until a
source change makes both supported legacy inputs reach the same normalized
public region.

## Handoff artifacts

- [source fingerprint](handoff-vw-m3-mouth-default-partial-physical-prep-source-fingerprint.json)
- [test patch](handoff-vw-m3-mouth-default-partial-physical-prep-test.patch)
- [central READY command](handoff-vw-m3-mouth-default-partial-physical-prep-COMMAND)
- [guarded controller](handoff-vw-m3-mouth-default-partial-physical-prep-run-central.py)
- [guarded READY wrapper](handoff-vw-m3-mouth-default-partial-physical-prep-READY.sh)

The patch adds only the default and one partial case, two frames (`0`, `3`)
per case, and a planted 20-pixel mismatch. It asserts the unchanged 799 px
compatibility denominator and 387 px erase region, verifies the planted
mismatch exceeds 2%, and verifies captured PNGs are unchanged. It is central-
only and does not run from this worker.

## Validation

- `git -C /home/user/work/agent apply --check --whitespace=error-all ...test.patch` — PASS.
- `git -C /home/user/work/agent apply --stat ...test.patch` — PASS; 2 files, 122 insertions.
- `bash -n ...READY.sh` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 -c 'ast.parse(...)'` on the controller — PASS.
- Composition `npm test -- --test-name-pattern='scene|diagnostic'` — BLOCKED during `npm run build:test` because this worker lacks the repository dependencies (`react`, `remotion`, `@remotion/media`, `@types/node`, and related modules). No install was attempted, per task rules.

No browser, render, localhost, full suite, network, central capture, or shared
dependency mutation was performed. The worktree is clean. Central execution
requires manager review/grant, an exact reviewed Agent source SHA in
`READY_GRANTED`, the immutable public12 artifact, and the literal command in
the COMMAND artifact.
