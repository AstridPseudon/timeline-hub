BLOCKED — no READY graph and no capability command is authorized from this source.

The current safe diagnostic is:

```sh
cd /home/user/work/wt/vw-m3-tab-private12-capability-port
/tmp/vw-m3-agent-gate-node20.19.4/bin/node tests/e2e/timeline/tab-audio-capture.controller.mjs --discover
```

Expected NOW: exit 1, `BLOCKED: app-private-clean12-graph has no approved full physical READY graph`; no Playwright invocation or socket/browser. Do not interpret this as an actual --list pass.

There is deliberately no READY.json, grant, capability marker, or central request here. The exact graph fingerprint and final committed SHA cannot be supplied until the dependency blocker is resolved. `FROZEN_PRIVATE_GRAPH` must remain null until then.

Resume sequence for the manager: approved physical READY graph -> freeze graph/root/tree in controller -> point this worktree's own node_modules link at that graph (never change shared paths) -> finish private-only validation and actual --list -> harness commit -> independent exact source/graph review -> register a fresh central pure-preflight namespace using `bash /home/user/work/wt/vw-m3-tab-private12-capability-port/tests/e2e/timeline/setup-tab-audio-capture.sh` with TAB_AUDIO_RUN unset, under the normal browser flock/QUIET/floor checks -> review its exact fingerprint -> issue ONE new capability grant and distinct absolute output/preflight/marker paths -> ONE central capture invocation with TAB_AUDIO_RUN=1. No request is made by this worker. All pending fields remain explicitly unknown rather than borrowed from an old grant.
