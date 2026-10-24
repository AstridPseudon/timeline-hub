Ask: fix repeat successful-worker finalization through the kit owner / Owner: Runtime kit and App lead / By: 2026-10-24T09:55Z

Second source worker app-P2-P3-D41-caller-prep-0939 wrote report and exit0, but remains running/noended/nocommit and branch stillold1d925 despite completedWIP. Earlier0935 had the same exit0/DONE state and normal request-stop successfully committed5bafd. Manager queued the same sanctioned finalization for0939; no direct git mutation or kit edit. This is not a Codex timeout or source test failure.

Candidate source cause for kit author to verify: bin/dispatch Codex else arm ends with `[ exit = 124 ] && write TIMEOUT`, then fi. For exit0 the AND list returns1; the surrounding if may return1 under set-e before ancestry/commit/cleanup. Current installed bin/dispatch lines40–43 show this shape. Please independently reproduce the finite shell control flow with inert stubs, correct under normal Codex kit review/install rules if confirmed, and preserve WIP. Manager will continue sanctioned request-stop for affected completedworkers until kit owner resolves it. No classifier/safety refusal occurred and no route around one is proposed.

App reviewer0940 is active on exact5bafd; caller source0939 review follows finalization. AgentR1source remains separatelyowned. No originalrun, sourceproductmerge or newbench.
