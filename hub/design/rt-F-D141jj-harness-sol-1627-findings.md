# Qualification: FAIL

## F1: blocking (observed)

Isolation removes the reused fixed trace collision, but complete checker still exits 1 at preserved stale-nonapp-upstream assertion.


## F2: blocking (observed and source inspection)

Stale fixture commits current.txt on HEAD but leaves origin/main and tl/integration at stale_base. Thus recorded upstream_base equals current origin/main; D68 exact stale-upstream guard does not fire. The mislabeled negative is accepted and creates a PASS receipt.

Source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-base-fix-next/evidence/check_jj.py:438-448; /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-base-fix-next/evidence/candidate/delivery_gate_build.py:240-241`.


## F3: blocking (static, genuine stale case not executed)

invoke only converts OSError/ValueError into failure. D68 subprocess refusal instead returns nonzero through run_wrapper; caller.main writes a FAIL receipt and returns code. Existing negative asserts exception and no target receipt. Merely making origin/main stale will still not satisfy these preserved assertions. No production contract or assertion changed.

Source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-base-fix-next/evidence/check_jj.py:116-122,431-432; /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-base-fix-next/evidence/candidate/run-final-delivery.py:295-324`.


## F4: coverage (static, later case unexecuted)

wrong-stage-owner patches caller.os.geteuid to 65534 before main. Shared os.geteuid is consulted in source_identity first, so real source root ownership fails before stage ownership is checked. Existing helper can report this case for an earlier refusal, failing to establish its stated stage-owner purpose.

Source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-base-fix-next/evidence/check_jj.py:477-484; /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141jj-base-fix-next/evidence/candidate/run-final-delivery.py:106,270-274`.


## F5: monitoring limitation (observed)

Detached first sampler and first replacement launch failed before persistent supervised monitor. Coverage gap disclosed in sampler-lifecycle.json and timestamps; no heavy execution during gap. Persistent 5s sampler covers the sole checker run and validations; do not call whole-worker coverage complete.


## F6: scope (observed)

One complete checker command was launched once. Its preserved failure stops remaining negatives, so seven refusal purposes are preserved in code but not all verified in this run. Negative fixture unexpectedly caused a second sequential bounded D68 staging operation within that single heavy checker invocation. No concurrent heavy, full source copy, retry or deletion.
