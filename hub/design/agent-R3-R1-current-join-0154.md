# Agent R3 current R1-native join

- Exact R3 source: `2cc23d0aab76e1ef55b1128e14889ce96b33a01b`.
- Exact merge parent: current `tl/integration` `1951ee928a377c61d13642677269c4f91f70f0f0`; manager marker says the clean merge completed at 01:55Z.
- Current preservation: inherited-read capture remains in `astrid/sdk/timeline/commands.py`; V1 meta/schema and R3 conformance/preview/error files remain in the staged merge tree. No extra product edits were made.
- Source test evidence: the real-document conformance/provider/preview-error lane passed 126 tests; meta/round-trip/client neighbors passed 19 tests plus 2 subtests. Scoped product Ruff passed. Mypy baseline remained exactly 1915 findings.
- Runtime owner source observed: `/home/user/work/runtime` current integration `44d6be180e65174a8c25047a599342752e7afeff`; used only as the offline `runtime_protocol` import for Agent tests. No actual wire or HTTP claim is made.
- Later independent review remains a manager follow-up against the exact merged tree. Full/browser/live suites were not run.
