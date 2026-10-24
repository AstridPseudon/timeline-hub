Ask: Agent accounts the 468 failed/errored nodes (D43); Runtime reviews the runtime_protocol import errors against Runtime pin 45c3a7f4 / Owner: Agent and Runtime / By: 2026-10-24T06:30Z

TERMINAL (05:51Z, worker tf-agent-full-farm-0503 DONE): test id agent-full-farm-1024050351-26511 FAIL, 288 failed, 17335 passed, 4 skipped, 187 setup errors, 2836 s. Tested Agent HEAD 9cd3dbe865a941c052bda04ae0d61306d18f8f26, tree 57f0231da0d7904ecd8778169973d6384e0ae141 (not the selected 8657e836 / b5cbc402). Non-gate checkpoint. No resubmit.

Full report, causes and the node lists: design/farm-agent-full-checkpoint-20261024T0555Z.md, -nodes-failed.txt (281 ids), -nodes-errored.txt (187 ids). No junit; passed ids cannot be listed; 7 of the 288 failures have no FAILED line in the log.

Causes (rough): 187 setup errors are environment (the full-farm row has no ASTRID_REMOTION_PROJECT_DIR / Node 20.19.4 / provisioned Remotion peers, only Python path env). About 61 `No module named runtime_protocol` plus 48 `cannot import name external_pack_sources from runtime_protocol` point at the Runtime pin 45c3a7f4 versus this Agent tree (pin mismatch, product or harness undetermined). About 100 timeline/SDK state failures (editing_conformance, sdk/test_timeline_*) are likely product, possibly downstream of the pin mismatch.

Consequence: the row lacks the Remotion/Node env used by the `full-remotion-*` rows, so a clean full needs a corrected row first. The farm will not re-run without an owner decision.
