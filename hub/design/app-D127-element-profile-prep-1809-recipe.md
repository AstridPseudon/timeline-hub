# D127 one-element profile: source-only preparation

Status: \`READY_SOURCE\`. This is a dry preparation only. No browser, native process,
Runtime/Agent backend, service submission, preflight execution, collector, sampler,
benchmark, body, or D130 SWAP/WAL/recovery work was run.

## Supported selector and original lifecycle

Use the existing D66 \`p2-element\` selector:

\`\`\`text
file: tests/e2e/local/three-products.p2-elements-assets.spec.ts
grep: P2 mounted element edit: real catalog apply, exact params patch, reload and guarded Undo$
count: 1
\`\`\`

The original test remains the complete native lifecycle. It opens the seeded
timeline, records the native pre-history and canonical closure, applies the
\`am-burst\` catalog element, asserts the v2 \`doc.patch\` request and accepted reply,
reads native canonical closure/history, edits \`params.bob\` to \`12\`, asserts the
single-field patch and history, reloads, performs guarded undo of the params commit,
reloads, performs guarded undo of the element commit, and reloads to assert the
element is absent. The original dialog status wait is unchanged at 5 seconds.
There is no selector filtering of a full tour.

## Exact source tuple to bind at controller dispatch

These are the accepted source requirements retained by bootstrap 1731/1738 and
sampled tour 1440, combined with the requested current App and Runtime normal
identities. The tuple is captured once and must not be rewritten after checkout.

\`\`\`text
D66_APP_SHA='d5a1d1ab6550187e377fd7387d300102b8b82ece'
D66_APP_TREE='7be73e2cbbcf89d627bf7b9da940b4ce17968c20'
D66_APP_CHECKOUT='/home/user/work/wt/app-pin-d5a1d1ab'
D66_AGENT_SHA='070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2'
D66_AGENT_TREE='6056414359ae9fce08d999d54cbecf719fda33c3'
D66_AGENT_CHECKOUT='/home/user/work/wt/agt-pin-070dfc5e'
D66_RUNTIME_SHA='e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9'
D66_RUNTIME_TREE='d5cb9335a03bf4764548e379ce180a66bf966910'
D66_RUNTIME_CHECKOUT='/home/user/work/wt/rt-pin-e319fdbd'
D66_COMPOSITION_SHA='635f4de06fda22a85fc2e4cfc764d0153a4c9f40'
D66_COMPOSITION_TREE='5ab5191a296980a0a6bcd1178ab6902d6478a148'
D66_COMPOSITION_CHECKOUT='/home/user/work/wt/vw-pin-635f4de0'
D66_P2_COMMIT_PHASE_CAPTURE_HELPER='/home/user/work/wt/rt-pin-e319fdbd/tests/helpers/p2_commit_phase_capture.py'
D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256='4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e'
ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS='2'
\`\`\`

The external helper must remain the exact canonical basename
\`p2_commit_phase_capture.py\`, a regular non-symlink file, and the SHA above must
match before registration and again in the mounted harness. The normal D66 route
also fails closed on attached, dirty, stale, wrong-tree, mutable-home, missing,
or tampered source checkouts.

## Exact service argv

The D66 registry row is the following command, with the environment above
prepended exactly as shown:

\`\`\`text
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2-element
\`\`\`

The source-only preflight variant is the same argv with \`--preflight\` appended.
The later controller must submit the stable exact App target
\`app-pin-d5a1d1ab\`, register distinct preflight and normal suite names, wait for
preflight PASS, and only then dispatch exactly one normal \`p2-element\` body with
\`--no-cache\`. This preparation does not register rows or submit either request.

## Required admission and output gates

Before any body dispatch, the controller must have genuine free disk of at least
5.2 GB at dispatch. D89c applies thereafter: stop at 4.0 GB, with only one heavy
body at a time. It must retain the source manifest, preflight manifest, normal
manifest, JUnit, and the private Runtime phase output under the D66 output tree.

The expected phase output is private \`0600\` JSONL in a private \`0700\` directory;
it may contain only safe phase names, counters, timestamps, lifecycle state,
bounded safe inclusive/leaf frames, loss/truncation/overhead accounting, and the
lowercase idempotency-key SHA. It must not contain bodies, raw keys, headers,
credentials, URLs, exception text, locals, or raw stack blobs. Bind the element
result only by its own lowercase UTF-8 idempotency-key SHA plus capture namespace,
PID/birth, and request ordinal. Preserve \`completed\`, \`raised\`,
\`returned_without_response\`, and \`pending_at_stop\`; do not turn an incomplete
result into a completed response or invent a provider duration or wall
denominator. The original 5-second waits and all native closure/history/undo
assertions remain authoritative.

The retained 10721 element join is historical input only: key hash
\`69c6463f169cffb79e62788ca6d42b02ebeb00aaf6a4f72520a989b20312faf4\`, request 3,
352 samples, 3 lost, pending, and unknown provider/response/wall denominator.
This recipe does not retarget it, use request 2, claim a 20-second element time,
or name a dominant cost.

## Authorization boundary

This profile is element-only (\`p2-element\`) and is unrelated to SWAP. D130 remains
an absolute hold on SWAP/WAL/recovery and full tours: no retry, refusal workaround,
recovery qualification, or full-tour filtering is authorized here. No new product
adoption, logger, collector, sampler, backend, native replay, profile/build, or
schema/pin/kit change is part of this preparation.

