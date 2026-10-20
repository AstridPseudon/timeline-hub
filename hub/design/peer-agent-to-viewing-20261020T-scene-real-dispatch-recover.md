# Peer note: Agent scene dispatch recovery needs Viewing executor

Agent recovery has restored the private SDK caller, invocation preflight,
managed-result validation, and `Timeline.check` adapter on current
`tl/integration`.

The current Agent base does not contain Viewing’s approved
`filmstrip_execution._execute_scene_only` implementation (nor the associated
`real_pack_host.py`/executor test files). The exact source is present on the
Viewing dispatch ref, but this worker must not modify Viewing-owned executor
files. Consequently the direct `test_scene_dispatch_contract.py` managed
writer portion and the real saved/candidate central proof cannot execute
against this Agent tree until Viewing lands its bounded executor patch.

Agent-side expectations are unchanged: existing managed `filmstrip_bundle`,
`scene` -> `scene-answers.json`, full `duration_frames`, receipt-bound source
identity/map, and advisory-unavailable behavior. Please land the approved
executor/artifact contract into the integration line or provide the exact
compatible proof target; no new endpoint, DTO, source factory, or manual
`_scene_inputs` activation is requested.
