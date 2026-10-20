# Runtime delivery base-ref fix

## Decision

`delivery-build` resolves each worktree's explicit `origin/main` to one
immutable commit ID at the start of `build_repo`. That ID is reused for the
diff/statistics, ancestry classification, squash parent, ranged-bundle
exclusion, and verification prerequisite. The integration tip is likewise
resolved once.

Private verification repositories receive those immutable objects under real
local refs (`refs/heads/main` and `refs/delivery/tip`). Verification checks out
the local `main`, so bundle prerequisites are tested against an actual local
base rather than an absent remote-tracking ref.

Ranged delivery sources may themselves be shallow. The private squash fetch
uses exactly `ahead + 1` depth: enough to retain the pinned base and every
intervening integration commit, without rebuilding unrelated source history.
Full/unrelated histories retain the existing unbounded path. The bundle is
still created from the integration ref with the pinned base excluded, and
bundle verification/fetch plus `git am` and tree equality remain mandatory.

## Evidence

- App source refs were inspected read-only: `origin/main` =
  `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa`, `tl/integration` =
  `7bb885b638838588a0dff81b64b7c34960ac07f3`, and the base is an ancestor.
- The App source is shallow. A depth-bounded private fetch materialized both
  local refs and exposed all 105 commits in `main..tip`.
- Ranged and unrelated-history delivery fixtures both produced PASS, with
  applied-patch tree = fetched-bundle tree = integration tree.

