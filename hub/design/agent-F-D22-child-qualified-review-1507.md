# F-D22 child-qualified review

Diagnosis: **PASS**. Exact Agent `8c355...` source inspection and a bounded dependency projection check reproduce the mechanism: `dependency_pythonpath()` drops `/home/user/work/wt/rt-pin-3b926efa` because its basename is not `site-packages`/`dist-packages`; `generic_host.py` then reconstructs the source child `PYTHONPATH` without Runtime3b. The retained full trace shows the representative child `ModuleNotFoundError: runtime_protocol`.

Qualification: **FAIL / not qualified**. The sole sanctioned venv completed with Agent `8c355...` but Runtime `9ce424...`, while the required Runtime is `3b926...`. PEP 610 direct URLs, `-I` origins, Python `3.13.16`, and absent `PYTHONNOUSERSITE` were verified for the installed child. The named suite row also invokes `/home/user/work/venv-agent/bin/python`, not the child venv. No original node was run on a non-exact pair.

No product/test/harness-body/dependency/pin/environment changes were made. Free space was `15,145,512,960` bytes, above the 15 GB floor.

Retained full-service profile: `/home/user/work/runtimes/agent-remotion-v3-819acf-1110`, lock `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`, archive `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, Composition `0.0.14`, Node `v20.19.4`; `PYTHONNOUSERSITE` was absent. The prior full-service child stderr and argv/env remain retained; no new exact-pair argv/env/stderr exists because the mismatch stopped qualification.

Next owner is child-venv provisioning plus harness row repair. Once exact, run at most these four original nodes: `test_two_public_command_workers_settle_task_leases_then_host_drains_original`, `test_private_child_command_preserves_entrypoint_and_original_bridge[-c]`, `test_sanitized_child_import_proves_current_host_sdk_version_and_vendored_client`, and `test_public_checkout_check_uses_retained_managed_scene_result`; preserve argv/env/stderr/import origins/body/profile hashes and do not claim the full 114 environment failures cleared from one representative.

Evidence: worker report `report.md`; source hashes and exact commands are recorded there. Existing full service remains terminal FAIL (`185 failed, 16,733 passed, 4 skipped, 19 errors`, exit 1, raw SHA-256 `e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`).
