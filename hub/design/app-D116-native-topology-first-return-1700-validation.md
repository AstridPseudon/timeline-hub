# D116 validation

The two protected SOURCEFAIL findings are corrected:

1. The accepted post-restart suffix now asserts `observed[-1]["key"] != flight["key"]`, matching original selectors 1143 and 1147.
2. The current emitter-authored topology now creates parent tracks `music` and `music-other`, places `music-bed` on `music`, and places `music-other` on the distinct `music-other` track.

The current route remains the registered provider with the authenticated transcript
pin and picker/anchor seam, followed by `emit_document_commands` and a real commit.
Original selectors, shared fixtures, product/runtime files, generated files, pins,
CLI paths, and archive inputs remain unchanged.

No functional test, central request, full suite, family suite, browser, native,
collector, or original replay was run. Independent protected review is still the
required next gate before the four collected cases may execute.
