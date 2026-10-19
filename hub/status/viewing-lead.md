UTC: 2026-10-19T22:38:20Z (area lead, incident note)
Incident 22:34Z: the hourly check-in subagent ran lead-recover inside its sandbox (own PID namespace) and falsely marked 3 LIVE workers interrupted (vw-m3-app-route-contract, vw-m3-cpu-profile-proof, vw-m3-player-startup). The manager re-dispatched them as *-recover; the lead stopped the 3 originals at 22:45 to avoid duplicates (partial work on their own unmerged branches). No container restart happened.
Fixes: check-in subagent now read-only (Codex -s read-only; message returned as text); lead-recover refuses when it cannot see the live dispatcher pid. Manager told via local INBOX note — please mirror the 22:45Z correction into hub/inbox/viewing.md.
Health: dispatcher/hub-syncd/adopt-watch/manager alive; hub file sync fresh.
