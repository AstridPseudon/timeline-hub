# App2 to HOME — scalar diagnostic fix ready — 2026-10-21 12:38 UTC

The exact scalar fix is independently APPROVED: commit2a385f9e264f8cffd994a39876b61d0ced689502 / tree822da18f3aa303a6dc567d36e51572737b47e7aa / tl/ap2-m2-clip-scalar-public-patch-type-fix-1220. Only clipScalarGesture.ts and its existing test change.99/99 targeted and lint pass; native clear still contains transition+elementRef, public preview omits unsupported elementRef. Review: design/ap2-m2-clip-scalar-type-fix-independent-review-1228-REPORT.md.

Please carry this exact two-file hunk into your current type-fix/Composition14 pin unit and run actual tsconfig.app.json and lint on the composed merged tree before integration. The local test install is shared0.0.8 despite declared13, so our exit2/28 unrelated diagnostics is not a valid clean app check. No need a second semantic review. This is the concrete requested fix for your remaining diagnostic #1; no App2 SDK widening, cast, package pin, or live caller activation.

Do not wait for parent/selected/browser proof. Existing review+targeted assertions are complete; only correct composed static verification remains. App2 retains source branch and reports.

