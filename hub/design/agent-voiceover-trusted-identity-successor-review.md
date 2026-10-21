# Agent voiceover trusted-identity successor review

Date: 2026-10-21 (UTC)

## Verdict

**APPROVE** for the exact committed successor:

- commit: `4c823a4c9fa2ccdc29e7a2d6bb6ff3ac1d003d13`
- tree: `382e23f702e6833ab0434cba36ba9657ac833906`
- parent: `6e9843662618b7bd3bde336094d7b8de7ce4063b`

The successor addresses both blocking findings in the prior `6e9843662`
review. `_consume_settled_voiceover_input` now requires trusted `target`,
`script_pin`, and `requester_key` arguments. `_request_identity` rejects a
claimant target from another project, validates the complete four-field target,
compares the complete target/script pin/requester key to trusted values, and
does so before claimant identity is used to recompute a root idempotency key.
Request settings are compared with every ordered plan job, not only the first;
per-entry text/settings and ordered occurrence checks remain in place.

The normal custody path is preserved: Runtime task/spec/result and managed
output identity remain authoritative, as do the exact media selection,
verified WAV bytes/hash/size, and intrinsic positive duration reads. The
requester still sends the normal duration-free speech inputs and the consumer
does not publish, commit, delegate, launch work, or copy trusted outer identity
into consumed rows.

This remains source-only and dormant. The committed tree has no production
caller for the consumer beyond its focused test import; no public, outer,
native, install, worker-root, or scope/delegation execution was attempted or
introduced. Private015 is therefore not claimed as qualified or activated.

## Concrete counterexample

None found in the committed successor. A carrier changing any target field,
script-pin value, or requester key is refused before Runtime custody reads can
make the claimant identity authoritative. A plan with different settings in a
later ordered job is likewise refused before consumption.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/agt-review-voiceover-trusted-identity-successor \
  tests/packs/video_editing/test_voiceover_requester.py
14 passed in 0.62s
```

Also passed: `git diff --check HEAD^ HEAD`. The worktree is clean. No full,
old broad, native, renderer, live-socket, or external-model suite was run.
