# Viewing recovery markers contradict live worker evidence

Problem: at22:34:43 lead-recover marked vw-m3-player-startup, vw-m3-cpu-profile-proof and vw-m3-app-route-contract EXIT137/INTERRUPTED and removed running markers. All THREE original logs continued with new commands after that timestamp. Player49units+77neighbors completed22:36:58, route boundary probes20PASS at22:36:36, CPU central1019223448-19007 preflight+5dependencyPASS stillrunning. Thus these jobs survived; do not kill/restart them on stale metadata.

I queued three new recovery workers based on the interruption markers, but all were REFUSED before worktree creation: fatal cannot create refs/heads/tl/vw-m3-*-recover.lock: Read-only file system (Agent/App .git). Dispatcher heartbeat is current but dispatcher.pid contains4, updated22:36:16. This suggests daemon recovery in a restricted process context; lead must verify outside the Codex sandbox. Manager did NOT run lead-recover or any daemon/git mutations.

Recommended: inspect actual host processes, restore one external dispatcher/hub-syncd/adopt-watch as needed, and correct stale worker metadata only after proving live processes. Keep original workers/source/test service intact. Refused recovery requests should stay abandoned (names not reused); do not retry while originals live. Ensure original harness final commit/exit isn't suppressed by stale137.

Meanwhile original workers are told to continue existing tasks and preserve evidence; no duplicate render/capture requested. CPU running result collected first; audio next quiet grant only after CPU completes. M3 integration/pins still held until recordedM1.
