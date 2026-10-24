## Verdict: FAIL at the App emitter seam

Added [a4_image_claim_proof.py](/home/user/work/wt/agt-A4-image-claim-audit-0112/test-support/a4_image_claim_proof.py), an offline causal proof using the retained evidence only.

Evidence:

- Input SHA: `09f4af...a2f24c4`
- App output SHA: `b9f9b3...4368bc7a`
- Core command fields all match Agent recording: `schema_version`, `op`, `version`, `select`, `args`.
- App submitted `created: []` implicitly.
- Agent recorded:

  `parent/asset:<asset>` and `parent/clip:clip-0`

- Runtime `validate_claims` therefore reproduced:

  `validation_error / invalid_records / provider executed a different command`

- No accepted write, head change, or history entry occurred.
- Selection custody was genuine: exact five-field registered image selection, `image/png`, size `3`.
- Canonical raw track opaque data and all child revisions were preserved.

The precise production seam is App commit `22efcda3...`, `src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:333-334`, where `clip.add-media` is emitted without `created`. The smallest authentic correction is to emit the asset ref conditionally from the authored registry plus `parent/clip:${row.id}`. No product change was made here.

The submitted step also has `patch: []` and no reads; the provider derives two effects and 13 dependencies. This was not the first refusal because `validate_claims` rejects the missing `created` claim first.

Checks passed:

- `py_compile`
- Ruff
- `git diff --check`
- Bounded offline proof with Runtime pin `8ea0766f`

No full or live suite was run. Commit message and `DONE` marker were written.