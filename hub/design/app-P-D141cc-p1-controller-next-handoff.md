# P1 handoff

Verdict: PASS for the admitted original P1 selector only.

Native submit created and waited through the unchanged D66 service path. Preflight ID: `app-pin-82e9e13d-full-d141-p1-82e9e13d-submit-preflight-1026121110-31121` (`pass`, exit 0). Normal ID: `app-pin-82e9e13d-full-d141-p1-82e9e13d-submit-1026121140-32161` (`pass`, exit 0, same-ID wait reported 200s). Raw `KEEP` was present for both IDs; the normal marker was created with `TEST_KEEP=D141hh p1` before queueing. The normal service reported readiness and two P1 cases: accepted split → merged trim after an intervening Agent edit → lost acknowledgement/restart/retry, and stale trim refusal with App rollback/message.

The source recipe, exact four pins, builder, and native output/artifact/stdout/stderr paths were loaded from the original JSON. There was one `--submit` invocation and one same-ID wait; no alternate request route or rerun. The persistent first-tool sampler was stopped and reaped after terminal; its trace is retained with the measured minimum and gaps.

This is not a platform GO, REG0, final-build, or ZIP claim. No product files were changed.
