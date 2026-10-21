# Gate 6 host-startup diagnosis handoff

Central `...-28523` ran 129s and failed all five cases at App `bootstrap.ts:238`. The common message combines two events:

- Original: the b70 helper emitted a valid `status:"failed"` line before `status:"ready"`.
- Secondary: App cleanup rejected the failed protocol at `bootstrap.ts:222`, then `bootstrap.ts:238` appended `pack-host startup cleanup failed`.

The original `error_type`/`error_location`, generic-host log, ready/state files, and raw custody result are not retained. App explicitly discards helper stderr (`bootstrap.ts:145`) and collapses the helper failure payload (`bootstrap.ts:169`). Therefore the exact missing prerequisite is UNKNOWN; do not infer one from the wrapper summary or replay this run.

Frozen evidence: Agent d0a `d0a5072bbe7b7ce9489f43aa0a81027ec400343b` / tree `6adb4a1190dfb2874e101565f37eccd392b1ae2f`; helper b70 `b70b9d569b2c80885d72734c61cd57e64c3715a8` / tree `687f077c4771e3dbb66bfb7ff2b98f310ac054b6` / blob `bc75d73f21c6310efad7fc41e4a3d790bfe3a8975e0eb96c08c3dec63e62961b`; Runtime SERVER 8f `8f105c26e3b62f9c2683f717a9773a12bc775a8e` versus official PRODUCER 2c4 `2c4ac180c2220bdad966bc01e95ad230e99ce26a`; graph `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c`; Agent Python `/home/user/work/venv-agent/bin/python`; App `909d2bfa...` / tree `79728118...`.

Physical boundary is firm: Chrome 155 was not launched. Every trace begins with `browserName:""`, records only the `harness` and `fixture` fixtures, and fails at `bootstrap.ts:238` from `harness.ts:280`. Browser launch is `harness.ts:292`, downstream and unreachable. No case body/export/media/comparison ran. Whether the generic host child was spawned is UNKNOWN because its custody files/log were removed; no residual pack-host/browser/Runtime/Vite process remains.

Minimal next step: in a newly authorized diagnostic run, preserve the helper's secret-free failed stdout line plus `generic-host.log`, ready/state, PID birth identity, and custody result before cleanup. Then repair only the exact existing environment prerequisite named by that payload. Keep Release 14 held; no handoff or pin qualifies.
