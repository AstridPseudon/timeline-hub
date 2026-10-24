Ask: none, informational (actual checkpoint test ID and progress) / Owner: Farm worker tf-agent-full-farm-0503 / By: 2026-10-24T05:35Z

ONE run, submitted once, not resubmitted: `request-test integration:agent full-farm`, test id agent-full-farm-1024050351-26511, submitted 05:03:51Z. Worker tf-agent-full-farm-0503 is waiting on that same id (two 600 s waits returned 124; no resubmit). At 05:29Z the log was about 70% through with many F marks; no counts yet.

Preflight green: row `agent full-farm` present once in suites.conf; rt-pin-45c3a7f4 clean at 45c3a7f4; agt-pin-8657e836 clean at 8657e836; 18 GB disk free.

TESTED SUBJECT differs from the selected one: integration:agent tested HEAD 9cd3dbe865a941c052bda04ae0d61306d18f8f26, tree 57f0231da0d7904ecd8778169973d6384e0ae141 (the head Agent named at 05:07Z). The selected tree b5cbc402 (head 8657e836) is NOT what ran; the report will state 9cd3dbe8 / 57f0231d and never relabel it.

Counts, junit path and hash, node lists and failure classification follow in design/farm-agent-full-checkpoint-<UTC>.md when the run ends.
