# App Gate 5 after-lost-ACK readiness

This source-only change adds the missing ordering case to
`tests/e2e/local/three-products.spec.ts`. The existing M1 journey remains
unchanged. The new case is titled `M2 real gate 5` and includes `M1 real` in
its title so the existing named browser lane selects it without relabelling
the historical M1 case.

## Required current source tuple

The test now requires both current source pins before the cohort starts. The
runner must provide nonempty full 40-character values for:

```text
TIMELINE_BUNDLE_AGENT_HEAD=<final Agent SHA matching public12>
TIMELINE_BUNDLE_RUNTIME_HEAD=<final Runtime SHA>
```

The values are intentionally not filled in here: the final Runtime tuple and
matching Agent public12 source are still pending. The test compares each value
to the actual clean checkout selected by `ASTRID_CHECKOUT` and
`ASTRID_RUNTIME_CHECKOUT`; missing, abbreviated, or moved pins fail the run.

## Central browser command

After the final tuple is published, the central test service must register the
two `TIMELINE_BUNDLE_*_HEAD` variables on the `e2e-m1-gesture` command (the
existing `M1 real` grep selects both the preserved M1 case and this new case):

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env \
  PLAYWRIGHT_OUTPUT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/browser-artifacts/${PWD##*/} \
  TIMELINE_BUNDLE_AGENT_HEAD=<final Agent SHA matching public12> \
  TIMELINE_BUNDLE_RUNTIME_HEAD=<final Runtime SHA> \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  ASTRID_CHECKOUT=/home/user/work/agent \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  npm run test:e2e:three-products -- --grep 'M1 real'
```

Equivalent queue request, once the suite definition carries those exact two
pin variables:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m2-gate5-after-ackloss-source e2e-m1-gesture) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

No browser, full suite, build, TypeScript check, install, server, or socket
run was performed by this worker while the active full run was protected.

## Evidence required from the browser run

The new mounted journey must show: A accepted; independent Agent C; the
durable A response aborted and the actual App outbox in `retry`; a fresh B
pointer gesture authored after that state and still unsent; reload and Runtime
restart; exact A request bytes/key/receipt replay; B submitted with fresh key,
base HA, and unchanged original guards; B rebased to 7 while C remains; raw
immutable closure, transition and opaque preservation, history/undo, Agent
`show` plus native-input inspection, and zero legacy snapshot POSTs.
