# Handoff — tab fingerprint framing fix

READY for manager pure preflight and one capability probe after final-SHA grant.

The App tab controller now uses the original canonical tree framing: it collects
the sorted `[path, kind, sha256(bytes)]` tuples and hashes one
`JSON.stringify(wholeTupleArray)` value. This corrects the real framing defect
without changing any environment, expected hash, version, six-peer-root, or
source guard. `hashTree` is exported only for the direct regression.

The direct regression uses a temporary two-file fixture with regular and
executable modes. It asserts the exact canonical fixture digest, rejects the
known pre-fix per-tuple concatenation digest, matches the read-only frozen
Chrome155 tree (`255` entries) and installed `playwright-core` tree (`106`
entries, frozen SHA
`6a78060c81886b7ba6f631d5b1193d50f0362c779f5b2dff2d784a31a6acc46d`), then
rejects changed bytes and a changed executable mode.

Passed with pinned Node `v20.19.4`:

```text
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --test tests/e2e/timeline/tab-audio-capture.controller.test.mjs
  1 top-level test passed; 0 failed, 0 skipped
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check tests/e2e/timeline/tab-audio-capture.controller.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check tests/e2e/timeline/tab-audio-capture.controller.test.mjs
bash -n tests/e2e/timeline/setup-tab-audio-capture.sh
npm exec -- eslint tests/e2e/timeline/tab-audio-capture.controller.mjs tests/e2e/timeline/tab-audio-capture.controller.test.mjs --max-warnings 0
git diff --check
```

No browser capability probe, socket/live service, network, install, full
suite, or central test-service request was run. Manager should rerun pure
preflight against the final committed SHA, then perform the single approved
real capability probe.
