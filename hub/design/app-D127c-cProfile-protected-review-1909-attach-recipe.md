# D127c attach review

The candidate documents an opt-in harness start before the mounted HTTP server,
then `P2CommitPhaseCapture(..., enabled=True).start()`, one mounted request,
and `stop()`. The source seam is the existing trace observation of
`RuntimeHandler._timeline_commit`; eligibility reads the existing prefetched
body and the exact POST timeline commit route.

The candidate's attach recipe does not record or enforce the reviewed D66
external helper's canonical basename and source hash. It instead describes
starting Runtime with the review checkout on `PYTHONPATH`. No product caller or
server source was changed, so this review grants no production-caller or D66
path/hash credit.

The source guard also needs to be narrowed to one element-only first POST and
must reject unsafe raw-pstats parent paths before any normal body is admitted.
