# Runtime post-014 merged server follow-up

**Status: COMPLETE — 2026-10-21**

This is a docs/handoff record for the compatible current server source. It
does not republish or repin the immutable ordinary Main014 producer.

## Exact source facts

- Published producer remains Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`,
  tree `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Current compatible server is Runtime integration
  `be8d254aef249cd421946cbf06ed86d58bc4b307`, tree
  `6d74348b66ee4a3602cfa4fd56b9b7c0ed7508e0`. It is not `95bd…` and is not
  the frozen physical `8f…` source.
- Transcript source `e2912b3afb6a6d019154185ac8214724da058d58` was merged as
  `2a9bd811ba1d1e65c0fb2c829eefd12939eed83`, tree
  `4fa58b2551f716c35cab6005cc8add84e59da8a9`.
- Rational source `60a919a22f42f0b5b0a246ce84cb43e9f46c2106` was merged as
  `be8d254…`, tree `6d74348b…`.
- The current server is an ancestor-preserving descendant of the published
  source: `95bd…` is an ancestor of `be8d…`, and `2a9bd811…` is an ancestor
  of `be8d…`.

## Deltas and preservation

The transcript patch allows retained transcript source reads and adds the
source-boundary test coverage. The rational patch accepts authored rational
FPS object mappings at inspection and converts them locally at the visual
seam without changing authored bytes. The combined published-to-current diff
is five files, 112 insertions and four deletions: three Runtime modules and
two tests.

The 76 paths in the published `contract/artifacts.json` were compared
byte-for-byte between `95bd…` and `be8d…`; zero paths differ. The published
schema/client/artifact identities remain: Runtime schema `7d4afa…`, raw
Agent schema `6ba7b5…` (55 definitions, 29 operations), raw bundle `6d707c…`,
and artifact version `54205b…` with manifest `a90238…`.

Transcript evidence is the exact public native `786` node pass plus 29
neighbors. Rational evidence is 14 controls plus actual admission and a
malformed-mapping negative. Neither patch activates broader association or
free-multi behavior.

## Full-run evidence

The manager-requested single central run completed:

`runtime-full-retained-owned-temp-integration-1021025626-25226`

It ran the retained-owned temporary integration suite on Runtime integration
tree `6d74348b…`, with the external snapshot Agent `04fdd64205b4a2365e50455bd3ac81b027c617f3`,
App `1be92c689c77efc3fe1d82eced116e86459139cf`, and Composition
`7bb54bbd64107e5090643ecca1e4d33164173e85c`. Final status is `pass`, exit
0: `5997 passed, 26 skipped, 15 xfailed, 12 warnings` in 311 seconds.

No product edit, regeneration, pin change, release-version claim, gate
closure, ZIP claim, browser run, renderer run, or duplicate full run was made.
