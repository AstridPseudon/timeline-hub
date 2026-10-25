# App lead HOST process-use audit of 35 statically stale pins, 2026-10-25T02:51:13Z

Method (read-only, run as root in the host PID namespace): for each of 108 /proc/<pid> entries, read cmdline, cwd, environ (only matched against the wt path, not recorded) and fd symlinks; match the string /wt/<pin> for each named pin. 4 of 108 PIDs had unreadable cmdline (zombie/kernel entries), which cannot hold a pin open. No file in any pin was touched.

Result: all 35 names exist as directories under /home/user/work/wt and have ZERO process references (clear). No busy pins.

- agt-pin-039ff2c2 clear
- agt-pin-0d142f79 clear
- agt-pin-263696c8 clear
- agt-pin-3b2db4bd clear
- agt-pin-3f1ceaed clear
- agt-pin-415181d9 clear
- agt-pin-5dec5dc6 clear
- agt-pin-78738040 clear
- agt-pin-831df37f clear
- agt-pin-a60f8b39 clear
- agt-pin-d6e84eb0 clear
- agt-pin-e39de26f clear
- agt-pin-ef036398 clear
- agt-pin-f4d6c72c clear
- app-pin-a90d4251 clear
- app-pin-adf06754 clear
- app-pin-c1014775 clear
- rt-pin-1bae0e8c clear
- rt-pin-21482a41 clear
- rt-pin-27f0306b clear
- rt-pin-2a9e347f clear
- rt-pin-327da207 clear
- rt-pin-34eac004 clear
- rt-pin-42855b64 clear
- rt-pin-45c3a7f4 clear
- rt-pin-5c1a03f1 clear
- rt-pin-691a9436 clear
- rt-pin-6ee4d904 clear
- rt-pin-732c48c6 clear
- rt-pin-780da6d6 clear
- rt-pin-a3cd1a32 clear
- rt-pin-bc227de0 clear
- rt-pin-e02f3e3d clear
- rt-pin-e89eb8c7 clear
- rt-pin-f69ad581 clear
