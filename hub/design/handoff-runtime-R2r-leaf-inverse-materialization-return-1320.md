# Runtime handoff: R2r leaf inverse materialization

The Runtime leaf inverse fix is ready for review on base `8592822fd11275540f596562f43c715676f2bc0f`.

Production ownership is limited to `runtime_protocol/timeline_commit_auth.py`. The fix consumes authenticated source-history materialization bindings in reverse, validates the paired internal/shot turnover, owner, pin, digest, native payload, unrelated closure images, and parent pin, then applies the existing complete stage-image guard. Tests are limited to `tests/test_timeline_inverse_stage_authentication.py`.

Proof: the retained first-stage actual capture now passes; 9 focused tests and the requested 170-test Runtime target lane pass; Ruff passes; production pyright passes. The complete retained two-stage replay remains blocked at the already-diagnosed aggregate/root sequential-input boundary and was not waived or rerun live.

See `scratchpad/orch/workerreport.md` and the worker evidence file for exact artifact/module/request/prepared/history/binding hashes.
