# VW-D09a — existing public-row curve caller result

Implemented the bounded caller migration from the source proposal.

- render_curves validates an admitted presenter row set through the existing
  _public_mouth_facts path and passes only present same-frame states onward.
- props_at and _presenter_props have one private optional keyword seam.
  None retains mouth_state; "closed" is selected explicitly, so scalar 0.0
  remains valid.
- The selected-cut regression proves admitted rows drive curve mouth values,
  private mouth_state is not consulted for those rows, and an absent sampled
  frame retains the private result.
- No crop, statistics, strict-threshold, provider, source, DTO, authority,
  serialized-field, or fallback behavior changed.

Evidence is recorded in the worker REPORT.md. The separate source/cache
custody suites were not run because this task forbids helper/Runtime/socket/
source-capture work during the active Gate 6 source/custody lane.
