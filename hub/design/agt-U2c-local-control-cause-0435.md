## U2c Linux local-control cause report

Overall classification: **FAIL; freeze remains held.**

No product or test files were changed. The worktree remains clean.

### Remaining local-control test

`test_local_host_control_is_separate_and_survives_multiple_bounded_requests` fails for a production Linux authority gap, not merely an unfaithful test setup.

Source chain:

- `astrid/core/execution/generic_host.py:12717` calls `AuthenticatedCleanupActor.private_peer(control)`.
- `astrid/core/execution/custody_broker.py:886` calls `_peer_token`.
- `custody_broker.py:594-596` explicitly rejects all non-Darwin platforms with `Darwin audit-token custody is unavailable`.

The retained 0410 `BrokenPipeError` is therefore secondary: `serve_control()` exits during peer authentication before processing the first frame.

Existing Linux custody support is process identity/pidfd custody only, covered by:

- `tests/core/execution/test_custody_broker.py:1532`
- `tests/core/execution/test_custody_broker.py:4856-4886`

No implemented Linux socket peer-credential authority (`SO_PEERCRED`, equivalent, or approved caller binding) exists or is used by this path.

Requested files for any future correction:

- Agent: `astrid/core/execution/generic_host.py`
- Agent: `astrid/core/execution/custody_broker.py`
- Agent: `tests/integrations/test_generic_host_activation_acceptance.py`
- Existing Linux custody reference: `tests/core/execution/test_custody_broker.py`

This requires an explicit scope decision: authorize a new Linux kernel-backed peer-authentication mechanism for the retained Runtime relay channel, and assign ownership/approval between Agent custody code and Runtime authority. No permission-gate, UID-only fallback, forged identity, or Darwin bypass is acceptable.

### Identity refusal message

Separate diagnostic seam:

- `astrid/sdk/host_bootstrap.py:1151-1152` raises `parked host OS identity changed`.
- The unchanged test expects `executable, uid or birth`.

Recommended PR-sized correction: preserve the existing predicate, but distinguish invalid handles from a valid handle whose executable/UID/birth identity changed, using the existing detailed diagnostic. Keep all assertions and safety behavior unchanged.

### Separate RunPod failures

The eight child-proof failures are unrelated Runtime/provider dependency failures:

- Runtime validation: `/home/user/work/runtime/runtime_protocol/remote_worker_activation.py:140-170`
- Agent producer seam: `astrid/packs/runpod/worker_owner.py:1307-1400`

Runtime requires `child: {attached, lanes, birth_id}`; the existing Agent observation omits it. Owner: Runtime readiness authority plus the RunPod process/session owner. No fabricated proof is appropriate.

### Evidence

Retained 0410 results:

- Abort safety: **14 passed**
- Activation/source identity: **10 failed, 77 passed**
- No full activation green claim.

Read-only checks run:

- AST parsing of generic host, custody broker, host bootstrap, and target test: **passed**
- `git diff --check`: **passed**
- `git diff --exit-code --quiet`: **passed**
- No tests rerun, per the read-only/static-check brief.

The v2 contract was read from `/home/user/work/runtime/contract/commit-v2.md`; the requested `design/commit-v2.md` path was not present.