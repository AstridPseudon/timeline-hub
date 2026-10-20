```sh
/home/user/work/venv-agent/bin/python -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-explicit-root-scene-central-clean-env/run-integration-clean.py --preflight
# PASS; origins and exact source tuple recorded in preflight.json

R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-explicit-root-scene-central-clean-env integration-viewing-explicit-root-scene-clean)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
# central pytest: 6 passed in 18.32s
# central wrapper exit: 1 (initial cleanup omitted the empty stage root; fixed locally)
```

Selected tests are the six existing `test_scene_answers.py` cases: lock/root
lifetime, unavailable refusal, registered public Node query, missing source,
stale source, and real-query exception cleanup.
