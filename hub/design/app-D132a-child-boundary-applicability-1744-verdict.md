# D132a/G3/R2 verdict

## Result

`NOT_APPLICABLE`

The already-qualified Runtime source `ab1e4f6141987706132916e2da16477f5a019464` does not qualify the remaining initial child-stage seam.

## Boundary

The first failure is at initial child birth during Runtime authenticated validation of the prepared record, before materialization, inverse, reload, or redo. The Agent operation stages `shot:new-shot` and `occurrence:new-occ`, then selects and reads `occurrence:new-occ/collection:clip` and `occurrence:new-occ/clip:title`. `Recording.read` deliberately captures the pre-command input state while returning the staged value. Frozen Runtime validation resolves those aliases against the pre-command closure; `timeline_commit_auth.py:150-156` finds no occurrence row and refuses `provider occurrence alias is outside its boundary`.

## Applicability comparison

The qualified pin changes only inverse-stage handling, including inverse-only restored-owner absence, complete-step materialization binding, inherited inverse shot-root retirement, authenticated physical turnover replay, and validation ordering after inverse effect boundaries. It leaves `native_site` and the ordinary initial create-command child alias path unchanged. Therefore it cannot qualify this exact first failure.

## Owner and scope

The existing owner is Runtime authenticated closure validation (`timeline_commit_auth.py` `native_site`/`validate_step`). If the same-command child behavior remains required by the contract, the minimal unapplied scope is a narrow Runtime rule authenticating aliases/collection captures for roots created earlier in that command’s staged execution while retaining the absent pre-command guard and exact boundary provenance. No Agent producer correction, test rewrite, normalizer, private authority injection, or product-guard-fault claim is supported.

No implementation was made.
