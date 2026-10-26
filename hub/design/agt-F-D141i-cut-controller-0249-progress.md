# D141i cut measurement progress

{
  "schema": "timeline.agent.d141i.cut-controller.service.v1",
  "controller": "agt-F-D141i-cut-controller-0249",
  "submitted_utc": "2026-10-26T02:51:56.752503+00:00",
  "request_command": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:agent agent-core-full --no-cache",
  "request_exit": 0,
  "returned_stdout": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-agent-core-full-1026025151-24049\n",
  "result_dir": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-agent-core-full-1026025151-24049",
  "service_id": "agent-agent-core-full-1026025151-24049",
  "request_file": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-agent-core-full-1026025151-24049/request",
  "wait_command": "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agent-agent-core-full-1026025151-24049",
  "status": "SUBMITTED_RECORDED_BEFORE_POLL"
}

## Terminal service result

- Service ID: `agent-agent-core-full-1026025151-24049`; request returned and was recorded before polling.
- `wait-test agent-agent-core-full-1026025151-24049`: terminal exit `78`; status `fail`.
- Controller refusal: `REFUSED: controller admission disk floor not met: 4687142912 < 4700000000`
- No retry, cancellation, release, retarget, local body, collection, or alternative environment.
- Body/JUnit/runner/monitor/disk-trace artifacts were not produced because admission refused before body start; this is separate from genuine outcome counts.
