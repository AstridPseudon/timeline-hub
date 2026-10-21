# D09 normal `prepare_pair` caller label proof — handoff

Branch: `tl/vw-m3-d09-normal-prepare-label-proof-1256`.

Added a test-only regression in `tests/sdk/test_timeline_checkout.py`.
`fast_lane.verify(labels=True)` invokes the real `prepare_pair` caller once;
that caller makes two normal `scene_only` requests (published managed run and
working candidate), parses two source-bound managed `filmstrip_bundle` ZIPs,
and returns two actual `frame_providers` with two retained frames each. The
public label path consumes those providers.

The test deliberately uses a non-local clip type and blank decoded PNGs, and
tripwires both `astrid.core.timeline.onscreen.visible_at` and the overlay's
authored-config `labels_for` inference. It does not manually inject providers
into the pair, add a carrier/authority/source factory, or change product code.

Evidence: the focused caller test passed; `test_timeline_checkout.py` plus
`test_fast_lane_words.py` passed **115 tests** with 4 existing Pillow
deprecation warnings. `git diff --check` passed. Full/browser/native/live
socket/install suites were not run.

The existing advisory no-carrier/live-legacy branch remains: scene request or
bundle failure leaves that side without a provider and the existing label
fallback remains available to callers with no managed Scene carrier. This
handoff qualifies the normal successful caller only.
