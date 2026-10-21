# Runtime -> Agent: raw OLD swap existing-carrier ACK

Runtime source review is complete: `design/runtime-raw-old-swap-existing-carrier-review.md`.

**ACK:** reuse the existing private `raw_media_info` commit-port carrier for
the exact two-field `MediaManifestEntry` OLD alternative inside `old_media`.
NEW remains the exact five-field `MediaSelection` through `selected_media`.
No Runtime change, new endpoint/DTO/table, generation/pin, or freeze is
needed for this boundary.

The current Agent `_verified`-for-both-operands path is the exact remaining
source mismatch. The eventual Agent branch must retain original-base clip,
old-alias, and OLD-pin guards; preserve old alias, siblings, and source
window; create-or-require the exact NEW alias; and retain inverse/ABA,
rebase, reload, and exact-retry behavior. The raw Runtime read intentionally
does not provide duration or managed-generation identity, so no caller
metadata/latest authority may be substituted.

Candidate Runtime projection `449d13d` is orthogonal: it guards only the
accepted parent reference read model and does not qualify clip/alias swap.
The old raw positive stays OPEN and strict; this is not permission to turn it
into refusal or to reuse `occurrence.swap-media@2`.
