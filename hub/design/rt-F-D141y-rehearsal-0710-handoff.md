# D141y handoff

The planned Main-venue F-final rehearsal executed the canonical `delivery-build --dry-run` exactly once on all four requested source heads. It stopped at all-repository preflight with the ordinary App ancestry refusal against freshly read `origin/main` (`fc24f84994dc36cfae9349112782ab4d91dbc73b`).

This is not a PASS, and no actual per-repository patch, tree, bundle, or apply counts exist. Those are recorded as NOT_REACHED. Prospective source-only diff counts are separately labelled and must not be treated as build output.

No source worktree, product file, control script, template, gate file, canonical delivery path, ZIP, publication, or held request was changed. The refused Farm smoke was not transferred or retried. A later F-final build requires a separately authorized tuple whose App tip is descended from the current upstream base and a fresh all-repository preflight.
