# vw-m4 README cross-area consumer review

## Verdict

**REQUEST CHANGES — one inaccurate line.** The public-consumer boundary claims
otherwise match the current handoffs and source evidence.

### Inaccurate line

`README.md:391` says:

> `16/697 vs 16/799 threshold crossing`

That describes the wrong fact. Both `16/697` and `16/799` are above the strict
`>.02` threshold. The handoff records `16/697` versus `16/799` as the
compatibility-padding ratio control; the strict threshold crossings are **15
vs 16** (`15/799 <= .02 < 16/799`, while the 697-pixel denominator crosses at
15). Recommended wording:

> `697 vs 799 pixels; compatibility-padding ratios 16/697 vs 16/799, with strict threshold crossings at 15 vs 16`

The supporting evidence is `handoff-vw-m3-mouth-compat-agent-proposal-REPORT.md:24`
and the settled scope record `orchestrator-scope-triage-20261021T1147Z.md`/
`handoff-vw-m4-scope-triage-ledger-1209-REPORT.md:6`.

## Claims independently verified

- 0.0.14 source `df7b863...`, 80-member artifact, exact SHA, and package smoke
  identity agree with `release14-qualified-handoff.md`; the older 0.0.13/77-
  member artifact remains historical. Package qualification is explicitly
  distinct from coordinated Agent/App consumer pin and route adoption.
- The Main imported-theme route is accurately described as the admitted
  `media.import_file`/CAS descriptor passed as `inputs.theme`, materialized as
  managed `theme.json` by GenericHost, resolved by the existing renderer
  resolver, and forwarded as Root `props.theme`. A slug is not a Theme
  document. The normal proof is a pre-render props proof, not final-media or
  parity evidence.
- The evaluator/React/registry/theme seams and Agent/App host adapters are
  intentional adapters around the Composition evaluator; the handoffs and
  scope ruling do not authorize vendored Composition copies as adapters.
- `InspectionMouth`, public geometry/crop fields, fallback retirement, and
  statistic rewrites are not in 0.0.14. The private mouth-box fallback, legacy
  crop selection, statistics, thresholds, and separate 387-pixel erase control
  remain deferred/retained as documented.
- Gate 6 remains open. The latest canonical run passed preflight but failed in
  packet readiness before browser/Runtime launch, so physical execution was
  `0` bodies and all `5` cases not run; no media or parity claim follows.
- Scanner108 payload SHA prefix `204a` and instruction payload SHA prefix
  `969fe` remain immutable delivery inputs; no README change replaces them.

## Verification performed

Read-only commands; no tests, browser, socket, install, or full-suite replay:

```text
sed -n '1,240p' /tmp/.../scratchpad/orch/PLAN.md
git diff --unified=80 df7b86308902fae90eda1dc3080d17d8fc30ea78..40072bfef228ec382419f61e79d955b5f38b5ca9 -- README.md
sed -n '1,320p' <relevant handoff reports under /tmp/.../scratchpad/orch/design
rg -n <theme/evaluator/adapter symbols> /home/user/work/agent /home/user/work/app <this Composition worktree>
nl -ba README.md | sed -n '335,430p'
```

The target worktree remained clean. No product or README edit was made by this
review.
