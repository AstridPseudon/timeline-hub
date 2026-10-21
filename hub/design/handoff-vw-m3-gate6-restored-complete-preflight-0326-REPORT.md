# Gate6 preflight handoff

The restored complete preflight is **READY** for the manager-authorized sole
actual attempt. The unchanged reusable 0311 aggregator passed **21/21 checks,
0 failures** under `/tmp/timeline-viewing-browser.lock`.

- App909: `909d2bfa186985db9791be0ab090b9f4e7824f9b`, tree `79728118…`.
- Runtime graph: `4913a37e…`, 21,455 entries; physical isolation and external
  link census pass; `.package-lock.json` is `nlink=1`.
- No live `/proc` owner remains under the old pytest-115 fixture; its target
  has zero regular files.
- Disk: observed `11,109,838,848`; exact required pre-stage minimum
  `11,052,089,344`; exact predicted post-stage
  `10,795,167,744` after `314,671,104` staging.
- Side effects: no token, grant, marker, Runtime, browser, export, or service
  request.
- Immutable aggregator hash:
  `00486e4cc426ebeed71895f03fcc59149b281373a3b877920139ed8efa9b026a`.

Complete report and 44-record statfs trace:
[worker REPORT](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-restored-complete-preflight-0326/REPORT.md>).
