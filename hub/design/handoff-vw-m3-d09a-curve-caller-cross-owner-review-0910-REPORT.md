# VW-D09a independent cross-owner source review

## Verdict

**APPROVE.** The cumulative `0837+0846` packet satisfies the bounded D09a
curve-caller migration contract and is ready for the Agent HOME gate.

## Real Git source

- Base before the initial implementation:
  `a9f4cfdaee40f3382b51d6cdb291d7012be96b8c`.
- Initial implementation:
  `637dd07fd39272c67cc9f47784e4e8cf74357c50`.
- Dispatch correction / review HEAD:
  `3fed64383467c1051352a8426aebf8dd7542599d`.
- Review worktree was clean and product source was not edited by this review.

## Source verdict

`render_curves` calls the existing `_public_mouth_facts` admission path only
for `am-presenter` elements and passes a state only when that admitted state
exists for the same sampled frame. A missing or rejected public batch produces
an empty override map, so the original `props_at` call remains in force.

The admission/query/source/capture/cache guards are unchanged from the real
base: evidence mode, complete frame coverage, raw-mouth shape/range, basis and
fps, source-derived address, exact frame and dimensions, unique presenter
layer, state codebook, content-frame zero, and known finite positive ROI all
remain enforced. No timing or codebook copy, public API, DTO, provider,
authority, source factory, serialized field, or new query was introduced.

`props_at` keeps `own_motion` precedence and the original `PROPS.get` mapping
and call when no public override is present. An explicit admitted `"closed"`
state is not treated as falsey and produces mouth scalar `0.0`. The retained
direct-neighbor assertions and fallback controls remain unchanged.

## Evidence and limits

- Selected-cut aggregate: 25 passed in 5.14s (reused worker result).
- Motion neighbors: 33 passed in 10.27s (reused worker result).
- Ruff on all three files: passed (reused worker result).
- `git diff --check a9f4cfdae..3fed64383` on all three files: passed.
- Reviewer pure dispatch/closed-state check: PASS.

No Node host, browser, socket, central service, full suite, install,
source/cache custody suite, or physical proof was run, per brief. These
limitations remain unverified rather than being claimed green.

The exact cumulative patch and flat file/assertion summaries accompany this
report under the same `handoff-vw-m3-d09a-curve-caller-cross-owner-review-0910-`
prefix.
