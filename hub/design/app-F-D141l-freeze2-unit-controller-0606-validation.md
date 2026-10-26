# D141l current-unit validation

The normal service request `app-full-1026060654-8638` was admitted and ran against App `4de54db14bdc9ddc2ce2e5887258b03acbffd30d`, tree `84c3fb7f73f08c22220f8e808962fe3f24aaa0aa`. The registered command was unchanged: `npm test -- --maxWorkers=3`; request used `--no-cache`.

The dispatcher performed the binding validator check before body admission using the attached `timeline.d89d.measured-floor.v1` receipt. The receipt is data-only and is attached only at `tests/app-full-1026060654-8638/recorded-measured-floor.json`; its two witness paths reference the reviewed normalized DATA projections. The original normalization provenance remains in the witness-return evidence and is not presented as original stdout or a new observation.

Terminal result: exit 1 after 1270 seconds. Vitest: 4 failed / 1358 passed files out of 1362; 32 failed / 19745 passed tests out of 19777. The Node phase is `NOTRUN`, because `npm run test:app` failed before the registered `&&`-chained `npm run test:node` phase. No PASS or REG verdict is claimed.

Raw retained outputs: `tests/app-full-1026060654-8638/{request,snap,status,exit,summary,log.txt,disk-trace.tsv,KEEP}`. The service emitted no XML for this registered npm full route. Trace validation reported `trace PASS: 256 actual samples`; minimum available bytes were `4494544896`, final `4624244736`, and the 4,000,000,000-byte stop was not reached.

Pristine exact d822 checkout is not available to this worker. It must be obtained by the manager through the normal request-checkout path before any pristine full request; no synthetic checkout, source copy, fixture injection, or old receiver tuple is used.
