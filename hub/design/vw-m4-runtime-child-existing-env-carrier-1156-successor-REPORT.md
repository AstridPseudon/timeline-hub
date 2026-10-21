# 1156 exact-carrier successor

## Result

Prepared one unapplied successor patch for proposal 1156. The Composition
worktree stayed clean at df7b86308902fae90eda1dc3080d17d8fc30ea78, equal to
tl/integration.

The handoff is:

- vw-m4-runtime-child-existing-env-carrier-1156-successor.patch
- vw-m4-runtime-child-existing-env-carrier-1156-successor-fixture.sh
- vw-m4-runtime-child-existing-env-carrier-1156-successor-COMMANDS.txt
- vw-m4-runtime-child-existing-env-carrier-1156-successor-TEST.log

All are under
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/.

## Successor changes

bin/make-runtime now selects exactly one agent remotion-0012-nodes row before
$D.partial is created. It requires that row to contain exactly one
ASTRID_REMOTION_PROJECT_DIR token and requires its value to be exactly one of
the accepted legacy paths:

- /home/user/work/runtimes/agent-remotion-0012
- /home/user/work/runtimes/agent-remotion-0012/remotion

Missing, foreign, broken, duplicate, or duplicate-row inputs refuse before
archive/allocation. The existing env-template validation remains in place.

bin/make-child-venv now requires exactly one carrier token and exactly one
venv-agent-child-s2 selector in the selected base row before constructing
CHILD_LINE. The suite carrier is also checked against the selected runtime's
accepted flat/nested path before replacement.

The existing 1144 nested $D/remotion source layout, env carrier, lock digest
guard, immutable destinations, and no-guessed-baseline behavior are unchanged.
No ORCH bin/ file was installed or modified.

## Tests

Exact command record:

vw-m4-runtime-child-existing-env-carrier-1156-successor-COMMANDS.txt

Actual log:

vw-m4-runtime-child-existing-env-carrier-1156-successor-TEST.log

Passed:

- bash -n on the successor fixture.
- Successor patch dry-run and bash -n for both patched scripts in a private
  exact temporary root.
- The actual-hunk fixture, which applies both original 1156 and successor
  patches to private copies of only the kit scripts and uses synthetic
  Git/archive/Python boundaries.
- Runtime: missing, foreign, broken, and duplicate suite carriers were
  accepted far enough to reach archive on original 1156 (red), and refused
  with status 2 before archive or $D.partial on the successor (green).
- Runtime positive flat and nested carriers reached the successor validation
  and archive boundary, with both exact values shown by bash -x.
- Child: duplicate carrier and duplicate selector were accepted far enough to
  reach Python venv allocation on original 1156 (red), and refused with
  status 2 before Python allocation on the successor (green).
- Child positive flat and nested carriers reached CHILD_LINE construction,
  retaining the exact carrier and one selector before the synthetic allocation
  boundary.
- git diff --check; the Composition worktree status was clean.

Every fixture run records one exact mktemp root and removes that root in its
EXIT trap. The last recorded root was
/tmp/vw-m4-runtime1156-exact-carrier-fix-1210.e62Uuf; it was removed.

Not run by instruction: runtime/child creation, npm/PyPI installation, venv or
package installation, network, source/graph copy, build, browser, server,
socket, render, central test service, or full suite.

## Identity and hashes

Original proposal 1156:

cd5ae1b3444686789465fee7d07a0275647188d4d12893a991485a3bb1fb42ad

Successor patch:

12937a65da6a96eb5934ef83fddbfa3e6d7309a39eb18a28ffa19f445b3442ca

Successor fixture:

2c034ec72189b63ba87dee8c5dd9cd81c60e43f6ebbfd8247e0c20d181e8ba7d

Successor test log:

1f428099f1406e5b3c7bf9cc172bd3b68ccf56696fa9c4e257ab412737abe3ba

Successor command record:

e069cd6f668d2e5d11a1b55e56a3f0c00de6ad34c1a0c53338d3fe2f3f10eb03

Read-only kit source identities:

- make-runtime: 0bba1f5e69319dad8b68295eac1fddf7ba35ea21cc32d784407852700e7df202
- make-child-venv: b136f3c3fb24aa252dd4bb4ec875bc87c0b1565edf1f8392c1b08e514b0d89c4

## Decisions and next step

The selected legacy suite row is additionally required to be unique so the
validated row is the same row later cloned; this prevents a duplicate row from
making selection ambiguous. No missing legacy env or suite baseline was
invented or restored. The successor remains unapplied pending the lead's
independent review of this new diff and deliberate restoration/confirmation of
the authoritative legacy inputs.
