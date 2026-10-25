# D127c attach recipe

The normal product launcher remains unchanged. A diagnostic-only harness starts
the Runtime worker with this checkout on `PYTHONPATH`, constructs
`P2CommitPhaseCapture(..., enabled=True)`, calls `start()` before the mounted
HTTP server begins serving, sends one genuine v2 element commit, then calls
`stop()` after the bounded request.

The supported activating source seam is the existing Python trace observation
of `RuntimeHandler._timeline_commit`. Eligibility additionally requires the
existing prefetched request bytes, the exact POST commit route template, a
`commands` list containing `clip.set-element`, and no `dry_run: true`.

No product/server/service/provider/store/auth/schema/generated/App-source
files are changed. No body, request identifier, key, URL, argument, local,
exception text, or raw stack is copied into the safe output. Direct calls that
lack the mounted prefetch are intentionally not profiled.

Raw pstats are optional private validation artifacts only: use a new path under
`TMPDIR`; the helper creates the parent as mode 0700 and the file as mode 0600.
