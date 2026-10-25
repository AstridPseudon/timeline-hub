# FAIL — compound protected review

## Scope

- Candidate: `tl/agt-F-docpatch-compound-return-0112`, revision `f6d0ae5997f634ef9743e9edce77a7f995cf715d`
- Candidate baseline: `0ae146e1b0acc6e4a82ba6b4f905d88bad48320c`
- Reviewed file only: `tests/timeline/test_authoring_media.py`
- Candidate file SHA-256: `5d995d5a7399b8c0585a1ad4ffdac7b8b86a561097e8307eea8a80d9a376944e`
- Baseline file SHA-256: `cfd2770425f56ef93c4c7fb60c3a30d8a2379b557c1e54f43e1969a55f4b5c5c`

## Verdict and bounded finding

**FAIL.** The one-field replacement changes the retained placeholder to the imported `AUDIO` digest, but does not establish genuine authority or admission for that media in the current caller path.

`AUDIO` is imported from `tests/timeline/test_authoring_bundle.py` and is appended to the dependency manifest. The current `document_fixture` used by the compound path supplies a different `MEDIA` digest and does not provide `AUDIO` as a genuinely admitted source. `_public_document_compound` then places the value into the synthetic `Reader` canonical document. The subsequent `MediaRealm`/`DetachedRealm` path reaches the current Runtime commit service, but its media port admits selected old/new command media; a manifest-only retained digest is not thereby proven to have catalog/source authority. `_verify_document` validates digest and manifest shape, not the missing source admission.

Consequently, the retained pin can look canonical and survive the synthetic provider/history setup without resolving the original manifest-only admission seam. The existing corruption, readback, inverse, and opaque-graph assertions do not cure that missing authority proof. No merge is authorized. The bounded next step is a genuine admitted Runtime/source setup (or an exact failure for unavailable admission); I did not add synthetic history, weaken assertions, or modify the candidate.

## Structural evidence

- The candidate changes only the retained media field in `_public_document_compound`.
- This verdict is independent of the owned-move and recipe verdicts, even though the compound path imports shared helpers.
- No test, collection, helper, fixture, service, or browser execution was performed.

## Checks

- In-memory compile of baseline and candidate: passed.
- Scoped Ruff on baseline and candidate: passed.
- Scoped mypy under Python 3.13 with `--follow-imports=silent` and private cache: passed for baseline and candidate.
- `git diff --check`: passed.

Static source checks do not establish genuine media authority; later incremental functional proof remains owed after the admission seam is repaired.
