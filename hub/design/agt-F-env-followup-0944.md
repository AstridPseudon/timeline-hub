# F environment follow-up handoff — agt-F-env-followup-0944

The authentic `agent-remotion-0013` runtime is available and identity-checked:

| Item | Evidence |
|---|---|
| Agent source | `30da0a5e05d4529a2b97b3c1818cf9e15842d628` |
| Agent tree | `0dacaabb6cbb42bebc09b6677983814ad2f4d237` |
| Remotion tree | `08236aaf8c63e43dafba6baa4fe412343edd6a99` |
| lock SHA-256 | `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24` |
| Composition | `0.0.13`, artifact SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` |
| Remotion | `4.0.509` |
| path | `/home/user/work/runtimes/agent-remotion-0013` |

One original D09 node was sent through the central test service:

```text
tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result
request: agt-F-env-followup-0944-targeted-1023094616-20851
result: FAIL exit=1, 26s
```

The runtime fixture was found and copied. The test failed in the isolated registry probe because `runtime_protocol` was not installed: `ModuleNotFoundError: No module named 'runtime_protocol'`. The existing child environment’s real `python -I` origins are:

```text
astrid              /home/user/work/venv-agent-child-s2/lib/python3.13/site-packages/astrid/__init__.py
astrid_runtime_client /home/user/work/venv-agent-child-s2/lib/python3.13/site-packages/astrid_runtime_client/__init__.py
astrid_runtime      None
runtime_protocol    None
```

This confirms the remaining issue is an ordinary missing installed Runtime prerequisite, not a safety denial. The installer invokes `python -I -m astrid_runtime`; `PYTHONPATH` cannot be used as a qualification bypass.

The approved `make-child-venv` operation has no package/network timeout. It installs 160 requirements with `--no-cache-dir`, including two VCS requirements, and its previous run made no progress for about 34 minutes before termination and wedged the dispatcher. Current disk evidence was 16,400,961,536 bytes free against a 15 GB floor; the existing child comparator is 693,246,231 bytes and the 0013 runtime is 329,859,697 bytes. No retry was submitted.

Next owner: farm/ops should add an operations-side bounded timeout/progress guard to the existing provisioning execution and arrange a real installed Agent + Runtime tree (or approved packaged Runtime executable), then rerun only the installer representative and this D09 node. Preserve the 0013 source/lock/artifact identity and all original guards. No product or test changes were made here.

