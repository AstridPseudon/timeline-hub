# Gate 6 current-space execution handoff

Central preflight request
`vw-m3-gate6-current-space-cleared-same-packet-0750-e2e-viewing-gate6-clean-child-lock-marker-preflight-0748-1021075104-27901`
ran exactly:

```text
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-lifecycle-cause-repair-0739/run.sh --preflight
```

It failed exit 1 after the validator reported PASS. The validator produced
exactly five collected cases, source/graph/inode/77+75/tool/ancestry/dist/
GET200/clean-env guards passed, and issuance/browser/Runtime/physical cases
were all zero. The retained runner asserted `result.appSource.files`, but the
JSON stores that binding at `result.tuple.appSource`; this is the blocking
post-preflight shape mismatch. No physical request was registered.

Pre-request bytes under fd9: work free `11410075648`, threshold
`11320247244`, floor `10737418240`, threshold delta `582829004`, headroom
over threshold `89828404`. Central before-preflight free was `11409055744`;
preflight JSON recorded `11409043456`. Namespace, tuple, grant, marker, and
outputs remain absent. Final packet hashes and full details are in the worker
REPORT.
