# D141j mounted capture source findings

The private harness is complete and bounded to two new support files. It uses the existing App page fixture's single page/session, dynamically imports the existing collector module through `page.evaluate`, calls the existing installer and snapshot, writes the four-field artifact, attaches it through Playwright result retention, and uninstalls in `finally` on both success and failure.

The four top-level fields are `schema`, `expectedOccurrenceId`, `events`, and `retention`. Empty events remain empty; no mounted semantic presence is fabricated. The existing four-boundary positive/negative controls and checker remain unchanged and were exercised separately.

No product repair was made. `app.ts`, the popup proof, collector source, checker, pins, generated files, wire, and original assertions are unchanged. The Runtime phase helper remains a Runtime sink only.

No native diagnostic observation was run. Registration is false, no request/body/service/preflight/full/browser suite was started, and cause remains UNKNOWN. Future enable/extract/retention details are in `route.json`.
