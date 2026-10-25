# App lead HOST process-use audit of all current *-pin-* trees, 2026-10-25T05:28:35Z

Read-only scan of host /proc (cmdline, cwd, environ matched only against the wt path, fd symlinks). Result: all 15 pin trees have ZERO process references (clear). The manager still applies the head/queue/lease/test checks before any KEEP release.

- agt-pin-562ee30b clear
- agt-pin-5faeec5b clear
- agt-pin-6386c700 clear
- agt-pin-a836baa3 clear
- app-pin-043631db clear
- app-pin-06014e45 clear
- app-pin-1e34f8ea clear
- app-pin-24865fa2 clear
- app-pin-2d25dc46 clear
- app-pin-3199118d clear
- app-pin-5337b439 clear
- app-pin-9cb56c2a clear
- rt-pin-0c62dfa6 clear
- rt-pin-6634a17f clear
- vw-pin-635f4de0 clear
