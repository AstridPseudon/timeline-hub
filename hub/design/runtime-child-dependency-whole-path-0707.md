## Report

- Read PLAN and all named 0642/0649/0654/0701/0707 packets. No source changes.
- Exact regression: baseline `c74f6582e` forwarded original argv at `make-child-venv:76`. Current parser shifts/removes arguments at lines 45–64, then reuse forwards empty `"$@"` at line 92. Requester therefore receives no name/Agent SHA and refuses `invalid child name`.
- Normal route is otherwise wired: request validation/queue [`request-child-venv:10-60`](.../ops-handoff/child-dependency-reuse/candidate/request-child-venv:10), queue serialization [`:243-249`](.../ops-handoff/child-dependency-reuse/candidate/request-child-venv:243), Store context [`make-child-venv:186-190`](.../ops-handoff/child-dependency-reuse/candidate/make-child-venv:186), seeded verification/pip snapshot [`:301-315`](.../ops-handoff/child-dependency-reuse/candidate/make-child-venv:301), and Store build/reuse [`bench_store.py:579-644`](.../ops-handoff/child-dependency-reuse/candidate/bench_store.py:579).
- Store identity remains only `(agent_sha, backend_sha, client_tuple)` [`bench_store.py:39-52`](.../ops-handoff/child-dependency-reuse/candidate/bench_store.py:39). Legacy reuse verifies source distributions/RECORDs only; it does not prove third-party wheel hashes [`request-child-venv:135-225`](.../ops-handoff/child-dependency-reuse/candidate/request-child-venv:135).
- Genuine 0642 evidence contains no original wheelhouse, wheel files, wheel filenames, or per-wheel lock hashes. The failed candidate’s partial path and pip/provision logs are absent. It contains only `astrid` and `astrid-runtime` RECORDs plus a report with `pip_freeze` omitted.

Recommended correction for Sol:

1. Preserve original argv before parsing and forward that saved array on reuse.
2. When dependency-seed opt-in is set, fail closed on any legacy or Store-managed entry lacking explicit immutable dependency provenance; leave default legacy reuse unchanged.
3. The bounded provenance seam should retain the verifier’s exact lock bytes and selected wheel hashes/bytes, then verify every installed non-source dependency against that manifest on both fresh build and reuse. Source tuple or old RECORDs alone are insufficient.
4. Do not authorize oldchild cloning/overlay/relabeling or add a global same-UID trust backend. Same-UID parent concerns are not a newly reachable attack under the current private-owner model.

Tests/body rerun: none, per brief. No provisioning, installation, network, live Store/cache, or process probes performed. No AgentREADY or positive wheelhouse claim.

Completion markers written: commit message and empty `DONE`; worktree remains clean.