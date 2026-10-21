# Agent M2 free-multi forward/ rational repair

Repair exactly the two executable blockers in
`agent-free-multi-full-source-contract-review.md`, reviewed source-only at
`922317bd58aa4db8f7cced85b37dd96038ae17df`. This is a source-only contract
repair. The composed schema remains byte-identical to
`ba0/60defs34ops12v2`, and every 84fc floor remains byte-identical. No Runtime,
App, pin/freeze/generation, native, browser, render, full-suite, 462, or 173
work belongs here.

## 1. Forward equal-state ABA

The current `replay()` special case excludes `clip.move-set` from
`identities_only`, so any overlapping intervening publication is rejected
before the already-captured command claims are checked. That is the wrong
forward policy.

Change only the forward replay policy. A forward move-set replay may use the
existing identity-only intervening-history path for ordinary authored value
writes. The replay must then run the existing captured-command verification
against the final head. In particular:

- The original `reads`, `selections`, `bindings`, `created`, `expect`, and
  dependency/source pins remain the claims being checked. Do not re-capture,
  refresh, or rewrite them from the head.
- A value-only ABA whose final value and entity identity equal the original
  input is accepted. The two `hold` writes in the review probe must replay the
  move and produce records equivalent to the original plan.
- Membership/order claims, destination/lane structure, source/dependency pins,
  and entity identity/recreation claims remain protected. A genuinely changed
  final member set/order, source, or identity refuses atomically.
- Membership-affecting ABA records (including lane/root membership writes) and
  source/dependency history remain strict protections; relaxing a clip's
  ordinary value write must not turn those into a new acceptance path.
- `timeline.inverse` remains on the strict `check_intervening` path. A later
  same-value assignment or ABA still refuses undo with `intervening_write`.

The implementation must not globally weaken `check_intervening`, discard the
move-set selections/source reads, or make the command claims describe the
newer head. The minimal acceptable change is an explicit forward-only policy
at the replay boundary, with the existing final-state claim checks and strict
inverse path preserved.

### Forward replay acceptance matrix

| Case | Required result | Guard that proves it |
| --- | --- | --- |
| `hold: 2 -> 3 -> 2`, same clip identity | accept; original claims remain | final value/identity plus original command claims |
| final member set or authored order changed | refuse atomically | captured `selection.clips` / collection claims |
| final source/dependency value or source identity changed | refuse atomically | source read/dependency pin |
| row/track recreated under an occupied-looking ID | refuse atomically | bound entity identity / created-ID claim |
| inverse after a later same-value write or ABA | refuse | strict `intervening_write` check |

The old lane-entry/lane-root ABA assertions remain safety coverage. The new
positive case is only the ordinary equal-value forward case; it is not a
reason to remove or weaken membership, source, identity, order, or inverse
guards.

## 2. Main rational list spelling

`_move_set.py` must continue to obtain its FPS through the existing `rate()`
path and then use the existing `quantized_on()`/`Fraction` common-delta
calculation. Extend that existing parser/policy to accept Main's already
supported exact two-integer list spelling `[30000, 1001]`, with the same
positive-integer validation as Main's canonical FPS parser. Keep the existing
mapping spelling and scalar/default behavior unchanged.

Do not add a second quantizer, direct `30000 / 1001` placement, a new clamp,
or another `30` default. The move-set dependency must still record the
canonical numerator/denominator, and all destinations must be translated by
one shared quantized delta. The expected list-form result is byte/semantic
equivalent to the existing mapping-form result: starts at
`90 * 1001 / 30000` and a common two-second separation for the fixture. The
existing half-open blocker predicate remains unchanged:
`left < blocker_end and blocker_start < right`.

The parser probe must use only forms supported by the actual Main parser:
the nested `parent.config.theme_overrides.visual.canvas.fps` (and its supported
`base_parent_payload` counterpart) for Main timing coverage, plus the
move-set fixture's existing direct `parent.config.output.fps` field. Do not
invent a top-level or otherwise unsupported FPS location merely to make the
probe pass. The existing Main timing test remains the authority for nested
list/mapping acceptance; the move-set regression proves that its own direct
FPS input reaches the same canonical rate policy.

## Proposed test ledger

No old assertion is deleted. The one incorrect forward-ABA expectation is
converted one-to-one, and an equivalent real membership change is added as an
independent refusal:

| Ledger mapping | Required assertion |
| --- | --- |
| `tests/editing_conformance/test_recipe_free_move_set.py::test_membership_predicates_sources_and_aba_refuse_atomically[read-aba]` -> `tests/editing_conformance/test_recipe_free_move_set.py::test_forward_equal_value_aba_accepts_original_guards` | Same staged move and two intervening `hold` writes; replay succeeds, output/records remain equivalent to the original plan, and the original claims are not refreshed. Retain the paired inverse refusal assertion as a separate strict check. |
| `tests/editing_conformance/test_recipe_free_move_set.py::test_forward_changed_membership_refuses_atomically` (new) | Add a genuinely new member/blocker to the selected/destination collection, leave it changed at the final head, assert `selection_changed`, unchanged head, and no partial writes. |
| `tests/editing_conformance/test_recipe_free_move_set.py::test_membership_predicates_sources_and_aba_refuse_atomically[lane-entry-aba]` | Keep the lane membership ABA refusal. |
| `tests/editing_conformance/test_recipe_free_move_set.py::test_membership_predicates_sources_and_aba_refuse_atomically[lane-root-aba]` | Keep the lane-root/order ABA refusal. |
| `tests/editing_conformance/test_recipe_free_move_set.py::test_membership_predicates_sources_and_aba_refuse_atomically[source]`, `[member]`, `[order]` | Keep final source, member, and order refusal and atomicity. |
| `tests/editing_conformance/test_recipe_free_move_set.py::test_shared_rational_quantized_delta_accepts_main_list_rate_spelling` (new) | Run the existing common-delta fixture with `[30000, 1001]`; assert the exact mapping-equivalent starts/separation, preserved windows/holds/opaque data, canonical dependency pin, and exact inverse. |
| `tests/editing_conformance/test_recipe_free_move_set.py::test_half_open_destination_contacts_and_real_blockers` | Keep all four parameter IDs and half-open contact/blocker behavior. |
| `tests/editing_conformance/test_recipe_free_move_set.py::test_source_registry_reads_and_same_value_assignments_remain_guarded` | Keep source-pin refusal and inverse same-value guard. |
| `tests/editing_conformance/test_recipe_free_move_set.py::test_created_track_surviving_dependent_refuses_after_own_moves_are_reversed` | Keep surviving-dependent and intervening-write refusal. |
| `tests/editing_conformance/test_recipe_free_move_set.py::test_exact_app_drag_golden_selection_order_and_created_track_are_one_unit`, `test_create_and_two_own_move_stages_have_exact_inverse_and_redo` | Keep same-batch track creation, reserved IDs, authored order, opaque fields, clear behavior, inverse, redo, and reload. |
| `tests/sdk/test_timing_compiler.py::test_fixed_source_window_and_rational_half_frame_ties` | Keep both Main mapping/list parameter IDs; this remains nested Main parser evidence for exact rational half-frame ties. |

The focused qualification set is the two new regressions, the retained
move-set neighbors above, the 84fc/schema-floor subset, and the existing Main
rational timing test. Do not run or claim full/462/173, Runtime/App,
generation/pinning, native, browser, live-socket, render, or integration
qualification from this repair.

