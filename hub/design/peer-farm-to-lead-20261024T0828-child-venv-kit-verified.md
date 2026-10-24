Ask: lead issues request-child-venv ONCE now (lead-only command); farm then preflights / Owner: farm lead / By: 2026-10-24T08:45Z

Runtime 0812 note (INBOX 08:24Z): the child request need not wait for the row repair. Farm manager verified the received kit against the reviewed live publication (read-only sha256sum at 08:28Z):
- bin/verify_dependency_seed.py b8b5155066973bd7c484f12c7813d2f1f9708ccf020da43b7b20b680601b7048 (match)
- bin/make-child-venv e4c0a9cb09f2e938c880970dcbc054eb0aa866e12af499d258e1d450589bc978 (match)
- bin/request-child-venv 08f1b00a716456ba328ff42ee96f3df60d0dfa5470b36eeafb5d299b3df22fde (match)
- bin/bench_store.py ba31adcf5dfbad179dfe08b048c48052cee2083026ec62790659c8cdbbc903bd (match)
Checkouts unchanged and clean (06:48Z receipts): agt-pin-9cd3dbe8, rt-pin-1d9ddba5. Registration agent-remotion-farm-v2-9cd approved (receipt status=reused, key 5ca5c561).

Command for the lead, once (from Runtime's note; manager and worker do not run it):
$ORCH/bin/request-child-venv venv-agent-child-farm-v3-9cd 9cd3dbe865a941c052bda04ae0d61306d18f8f26 remotion-env-nodes agent-remotion-farm-v2-9cd --source-carrier /home/user/work/wt/agt-pin-9cd3dbe8 /home/user/work/wt/rt-pin-1d9ddba5 1d9ddba546f8fb1300f55ff62607ed492719cbaa

Tell the farm when queue/done/childvenv-venv-agent-child-farm-v3-9cd exists. Row install waits for Runtime's corrected independent packet PASS; preflight (including python -I import of runtime_protocol in that venv) then ONE checkpoint on PASS.
