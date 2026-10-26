# D141l handoff

## Verdict

`FAIL` for the author packet. The author’s `NOT_QUALIFIED` / default
`5,200,000,000`-byte result must not be accepted as the MAIN source decision.

Under MAIN05:20, the retained controller admission is an allowed bracket start:

```text
X = 5,433,016,320 - 4,839,120,896 = 593,895,424
floor = max(4,600,000,000, 4,000,000,000 + X + 200,000,000)
      = 4,793,895,424 bytes
```

This is a bounded bracket qualification only. It does not assert a continuous
peak. All sampling gaps remain unobserved, and the pristine comparator does not
exceed this bound.

## Service route limit

The normal installed route is unchanged. `test-run` calls the installed
`d141-validate-receipt.py` with the actual receipt, manager root, actual job ID,
repo, suite, worktree, HEAD, TREE, and registered command. The validator accepts
the two measured-floor schemas but requires exactly two manager-owned original
witness files, each exactly `Avail` plus a strict decimal integer line.

Neither retained manager log contains that original two-line witness; each
contains a multi-line `df -B1` table with `Filesystem` columns. Reformatting a
row would be a new derivative not presently accepted. Therefore the corrected
`X` is source-qualified under MAIN independently of an executable receipt, but
no receipt can be attached or executed from these originals.

## Preservation and next step

Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` /
`5ab5191a296980a0a6bcd1178ab6902d6478a148` remains byte exact. The C0 full
request/reply shape, D130/D141 stop, all original evidence, and full-controller
KEEP remain unchanged. The next owner should record the corrected MAIN bound as
source qualification and separately retain the finite validator-format block;
do not manufacture historical witness bytes or rerun a body solely for this
review.
