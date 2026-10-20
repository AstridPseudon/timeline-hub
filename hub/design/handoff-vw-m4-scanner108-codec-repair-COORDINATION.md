# Scanner 1.0.8 repair coordination

Repair is underway from exact 1.0.7 (archive baf2fd28f96670b02e4dc63e21bc680e2ab0339a97671515d79ab91f9cbd3e27). No product edits or 1.0.7 overwrites.

Proposed reuse: enumerate Agent FieldSpec stored_at plus stored_at_audio; validate each present stored field with its Agent-declared schema plus FieldSpec.to_stored (describe is formatting only), using the animation spec for shared entrance/exit storage, not rejecting non-fade animations as fade aliases. Preserve None clears. Audio curve non-string containers fail closed; unknown string curve IDs retain existing unknown policy (all 40 original tests are preserved, including their complete synthetic fixture with not-a-registered-curve). Transition mappings keep existing free-form string ID/type policy. No whole-document schema validator or copied bounds/animation names.

Codec-matrix worker: please publish findings in your flat handoff; repair will inspect them before final packaging. This note is a proposal for the repair, not an Agent-policy approval.
