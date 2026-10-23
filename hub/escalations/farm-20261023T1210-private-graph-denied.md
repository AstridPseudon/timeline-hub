# farm escalation: private dependency graph for the App full rerun was denied (permission)
Worker tf-app-full-ad96 (Luna high, --net --heavy, base ad96a4cac / tree f7ae7964edfb, both verified) could not build the private @banodoco/timeline-composition 0.0.14 graph. `ln -s`, `tar -xzf`, `cp -r` and a builder script each returned "requires approval" and the worker could not get it. Only mkdir and read-only commands ran. No test was run, there is no verdict, and the worktree and shared node_modules are untouched.

The shared graph holds a stale composition (0.0.13), so a plain `request-test integration:app full` would not be qualification evidence. The central test service uses the worktree's own graph, and no suite in tests/suites.conf builds a private one.

Decision owed: the orchestrator either (a) approves ln/tar/cp inside a private directory under the worker (workers/tf-app-full-ad96/nm) for this one run, (b) builds the private graph and points the farm run at it, or (c) tells App (whose worker ran this recipe successfully) to run the one full suite and the farm just records it. I did not route around the denial.
Leftover: $ORCH/workers/tf-app-full-ad96/build-nm.sh (draft builder script) needs removing with apply_patch Delete File.
