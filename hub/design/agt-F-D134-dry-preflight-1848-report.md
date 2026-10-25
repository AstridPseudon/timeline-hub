## F/D134 report

Completed the authorized DRY preflight only.

- Generated fresh frozen-tuple manifests using the documented normal D73 maker recipe:
  - Positive SHA-256: `b539c6bda83f...`
  - Poison SHA-256: `f41fef0062e6...`
  - Poison differs only in `agent_sha=000...000`.
- Independently verified the existing 2234 positive stub hash:
  `38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0`.

Results:

- Positive DRY: launcher preflight `0`, stub exit `17`, exactly `1` call.
- Poison DRY: exit `1`, deliberate `D73 launcher: agent SHA mismatch`, `0` calls.

Validation passed:

```text
bash -n evidence/measurement-command.sh evidence/preflight-command.sh
python3.11 -m json.tool [all evidence JSON files]
git diff --check
```

No full suite, collection, request-test, package/profile/child build, production code, suite mutation, or behavior test was run.

Evidence is in [evidence/](</home/user/work/wt/agt-F-D134-dry-preflight-1848/evidence>). Commit message and `DONE` marker were created. D128 fixture custody remains the blocker for any future full body; this work provides no ship-grade or behavior credit.