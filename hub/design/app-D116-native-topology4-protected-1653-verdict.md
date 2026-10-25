# D116 independent protected review

Verdict: **SOURCE FAIL; NEW4 NOTRUN**.

The actual base is the published normal successor `9350a674a85b9328e7ac1e8192e66dcc65cfbf77`, descended directly from `20177e66564f9f91735ed1a11bac821682d60edf`. The immutable Runtime pin is clean at `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` (parent `de2954a0`). The worktree contains only the two authorized new files relative to that base; all checked original hashes match and no product, Runtime, generated, pin, shared-fixture, archive, or CLI source changed.

The four new nodes collect, and Python 3.11 compile, Ruff, mypy, and diff checks pass. Functional execution is not authorized because the protected source review found:

1. `tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_move_trim_lost_ack_restart_and_guarded_undo` omits the original 1143/1147 assertion that the accepted suffix uses a distinct idempotency key: `observed[-1]["key"] != flight["key"]`.
2. `tests/editing_conformance/native_checkout_current_fixture.py::prepare` constructs both `music-bed` and `music-other` on `music-other` and does not construct the original parent `music` track. The genuine historical topology has `music-bed` on `music` and `music-other` on its distinct `music-other` track.

No source fix, functional bypass, central test request, or NEW4 run was made. Return these exact findings to the source owner for correction and re-review.
