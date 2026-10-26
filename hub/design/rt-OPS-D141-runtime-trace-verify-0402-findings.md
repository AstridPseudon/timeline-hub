# D141h independent closure findings

Verdict: **FAIL**. This is one bounded verification pass of the actual 0349 return source. No source edits were made.

## D141H-VERIFY-001 — OPEN

The required cancellation/reaping preservation check failed in the exact author control script. The run stopped at `real-controls.py:478` with:

```text
AssertionError: cancelled installed runner did not finalize its own trace
```

The private fixture's `body-cancel` remained `running`; its `disk-trace.tsv` had only the header and one `first` row; no `trace-validation` was produced within the script's 30-second wait. This leaves terminal/cancel/reap/KEEP trace and exit semantics unqualified.

This is the second D141h failure after 0340's D141H-SEC-001 review failure. Per the task brief, escalation is Main/Sol. I did not infer a root cause or edit the source.

## D141H-SEC-001 — UNVERIFIED, not claimed closed

The inspected implementation contains the intended no-follow descriptor custody, regular single-link owner/mode checks, device/inode binding, physical-parent binding, nonblocking opens, and same-descriptor validator path. However, the required same-control attack cases were after the cancellation assertion and did not run. Therefore this worker does not claim an independent PASS for symlink, FIFO, regular-inode replacement, parent substitution, bounded refusal, or zero redirected writes.

No other product or scope finding was opened. The source-only status, exact five-file publication manifest, App paired-kit refusal, C0 v2 API semantics, and lack of live P5/target15 qualification remain bounded preconditions/limits rather than release claims.
