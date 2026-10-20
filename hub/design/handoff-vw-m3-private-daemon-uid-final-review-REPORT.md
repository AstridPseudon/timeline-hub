## APPROVE

Reviewed `cd966437a` against `tl/vw-m3-pulse-daemon-only-uid-fix`. No product edits made.

- Only Pulse daemon uses `runuser` as existing `nobody:65534`; controller, Node, Chrome, and ffmpeg remain root.
- Private runtime/home/cookie paths are fresh, mode `0700`, cookie-authenticated, and cleaned via process-group termination/reaping.
- Existing source, grant, graph, discovery, stereo, warm-monitor, and forbidden-operation guards remain intact.
- Node SHA verified: `43d6cf...bb99490`; Chrome SHA verified: `cb19b5...e2c76`.

Tests passed:

```text
bash -n setup-private-pulse-stereo.sh
tsc --noEmit ... private-pulse-stereo.probe.ts private-pulse-stereo.config.ts
eslint --no-cache ... probe.ts config.ts
node --test tab-audio-capture.controller.test.mjs tab-audio-capture.analysis.test.mjs
offline launcher smoke: passed, no daemon/browser/socket/capture
environment tests against frozen clean graph overlay: 1 passed
git diff --check
```

`--discover` was not completed: the required 10 GiB disk floor is unavailable (9.7 GiB free). Live daemon/browser/socket/grant execution was not run. `getent` confirms `nobody:65534`; sandbox `runuser` cannot set groups, so central preflight remains required.

DONE marker and commit message written.