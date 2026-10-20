Unrequested broad test STOP needed: agt-m3-public13-installed-host-gate-agent-remotion-0013-nodes-1020180723-30947.
Worker violated bounded package/SSR/admission task: requested named suite WITHOUT --files; now running whole default suite (~8%). It is not an authorized full or qualification result.
Please terminate ONLY this test process group outside sandbox and mark CANCELLED/notcached, preserving logs/source. Test running file PID3148, resultdir has request files=''.
This blocks two targeted slots; raw-compose17366 and actual D13 cleanup probe are waiting. No new full requested by manager.
Worker stop requested; replacement will specify exact files plus bounded suite defaults. Source89cdb currentpin is unchanged; installed13 profile remains valid.
Not covered because: no manager stop-test command exists; outside-sandbox test process is not addressable safely by namespaced manager PID.
Rule that would let me decide next time: bin/request-stop-test <exact id>, plus refuse no-files requests on *-nodes suites.
