# Gate6 existing authorization and launch inputs

Status: **manager procedure prepared; not authorized or launched**.

The current Gate6 path has no grant or marker creation command. The controller
only reads `TAB_AUDIO_GRANT_PATH` and `TAB_AUDIO_RUN_MARKER` during `--ready`,
and the central request is the registered `request-test integration:app
e2e-viewing-gate6-current-fivecase` command. Historical `--prepare`/`--preflight`/
`--claim` belongs to a different standalone public12/stereo controller and is
not a valid current Gate6 producer.

The manager procedure, exact current grant fields, source-freeze derivation,
owner/manager authority boundary, fresh exclusive marker rule, and one-shot
central command are in:

- worker command: `/home/user/work/wt/vw-m3-gate6-existing-grant-launch-inputs/COMMAND`
- worker report: `/home/user/work/wt/vw-m3-gate6-existing-grant-launch-inputs/report.md`

No grant, marker, credentials, source tuple, browser, render, capture, live
admission, or product/source/dependency change was made. Current App checkout
evidence is dirty and its controller constants do not match the frozen d0a5072b
Agent input, so it must not be used as the final source freeze.
