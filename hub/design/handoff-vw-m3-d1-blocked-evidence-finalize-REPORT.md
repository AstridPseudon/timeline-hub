# D09 real-Node preflight: blocked, unqualified

Administrative closeout only. No product repository was changed, and no new
test, graph scan, repair, browser, Node execution, install, network, or central
lane was run by this finalizer.

## Recorded result

The prior worker `vw-m3-d1-public-positive-real-pinned-node` stopped at its
required preflight. Its direct Node checks passed for the retained executable:

```text
path: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
version: v20.19.4
sha256: 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
```

The next guard refused the configured peer graph: **21,565 entries observed;
21,488 required**. The required clean graph is peer checkout
`f8164bef73215272562c4d6974acadbd82c2898a` with graph digest
`9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425`.
This stopped before the central lane, so there is no qualification claim.

The historical 52-case run used a fake 20.20 wrapper and is functional-only,
not qualified. Its historical central result remains failed: 3 passes and 49
environment/setup errors from missing peers. It must not be upgraded to
qualification.

## Preserved state and handoff

- Prior WIP branch/report/stage references remain untouched:
  `tl/vw-m3-d1-public-positive-real-pinned-node`, WIP commit
  `4251a649b37ff44d21d418270079afc648452898`, and its owned
  `stage-20261020` path.
- Historical source Node and 77-member public12 proof remain retained. No
  cleanup was attempted; lead owns any later stage cleanup after proving it is
  unused and has no shared-alias references.
- The Agent finalizer worktree is clean. The actual lead graph audit is
  pending.

## Recommended next step

Lead should audit and, only if separately authorized, reconstruct the exact
clean peer graph and perform a fresh independent preflight before considering
one central named lane. Keep this result **BLOCKED / UNQUALIFIED**.
