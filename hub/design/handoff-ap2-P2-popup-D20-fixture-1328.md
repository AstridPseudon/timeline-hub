# Handoff: ap2-P2-popup-D20-fixture-1328

The App fixture no longer writes `/composition-revisions`. Setup now commits the exact D20 shared placement first, then applies only the original authored media/registry/opaque changes with `doc.patch`; this preserves the two-occurrence shared physical source and the genuine old media IDs. Gesture code and assertions are byte-identical (tail hash `2eda7eb8fe2fa77ed69195f471ecf5d6d46736bed012cbd78035c5487e5e35cb`).

Validated with scoped ESLint, configured App and Node TypeScript checks, diff-check, EOF check, retired-route inventory, and offline compilation of the reviewed D20 helper source. No browser or service tests were run. Before merge, independently review the Agent semantic source, integrate it into the worker's Agent checkout, then run the named P2/browser qualification through the central service.
