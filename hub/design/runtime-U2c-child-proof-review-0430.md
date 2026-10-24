## U2c child-proof review

Result: the missing-producer claim is correct. No existing genuine RunPod producer emits the required child attachment/two-lane/birth identity proof.

- Runtime authority: `remote_worker_activation.py` at `2b49da8d6` / blob `2049b17e…`, lines 140–175. RunPod observations must contain `child.attached == true`, lanes exactly `["orchestration", "executor"]`, and a nonempty `birth_id`.
- Runtime deployment does not provide it: `remote_worker_deployment.py` blob `58c96b64…`, lines 552–560 and 818–890. `ProjectedLaunch` contains only argv, env, digest, and cwd.
- Local comparison is genuine: `verified_host_launch.py` blob `ea6d3c58…`, lines 390–423 binds the actual retained child and birth identity; `local_worker_composition.py` blob `5b259646…`, lines 384–406 and 1052–1054 binds and re-verifies that same child.
- Agent RunPod seam is incomplete at current integration `999e221f…`:
  - `worker_owner.py` blob `513d201d…`, lines 258–293 re-observes only account/pod identity.
  - `RunPodRemoteWorkerInspector.observe()` lines 1328–1391 emits provider identity, host process identity, Runtime/session/readiness data, but no `child`.
  - `worker_process.py` blob `5a2f5686…`, lines 382–410 provides host process birth identity, not provider child custody.
  - `host_bootstrap.py` blob `870dc7ff…`, lines 1106–1207 likewise emits host/provider data only.
- `attached_unverified` in `worker_preparation.py` is explicitly not proof. Runtime’s test fixture manually inserts the child object at `tests/test_remote_worker_activation.py:120–145`; it cannot qualify production RunPod behavior.

Authority/owner seam: Runtime owns the unchanged strict readiness validator; the missing producer is Agent-owned, in the RunPod provider/process/session owner path feeding `RunPodRemoteWorkerInspector.observe()`. It must capture genuine provider-owned two-lane child attachment and birth identity. No Runtime API, credential, guard, or contract change is indicated.

Checks:

- `git diff --check` — passed.
- Runtime activation/deployment source equality against refs `40427e8b5` and `8ea0766f5` — passed.
- Worktree — clean.
- Tests, sockets, daemons, credentials, lint, and types — not run per read-only/source-only brief.

U2c remains blocked until that Agent-owned producer exists. No implementation or new scope was added.