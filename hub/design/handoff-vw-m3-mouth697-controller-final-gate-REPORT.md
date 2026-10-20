# Mouth697 controller final gate

## Verdict

**APPROVE — narrow future central execution only.** This is approval of the
prepared controller/manifest/patch contract, not a physical pixel result and
not an admitted-host, Runtime, or Gate 7 claim. No grant was created and no
browser/render/socket execution was performed.

## Reviewed handoff

- Patch: `handoff-vw-m3-mouth697-physical-controller-prep.patch`
  (`sha256 9624922e36ff9668d2458704368a16ea87d4e82551959e46d9e0b197ca122d5c`)
- Manifest: `handoff-vw-m3-mouth697-physical-controller-prep-manifest.json`
  (`sha256 c70af694aba13fbe4cd174a47d3d536a49a93dce5bf172a833fe350d74daa1bf`)
- READY script: `sha256 04603d3b75a201119336bcea2f458890cdb33070ca9c22073992d6482836cbf6`
- Central runner: `sha256 cc576c4cea3c647ebb4f298decfdda6c323d4398f37f0f7687ed27c738250ae6`

The frozen `ee71010a0947edcbbacbf8178e5fee11ab6bab3d` Agent source was read
without checkout. All eight manifest/controller source hashes match that
revision. The Composition reference is `5a4e9b72f`; the current Composition
worktree remained clean.

## Contract review

- The new case is only raw `mouth: {x: 151, y: 104}` with omitted width and
  frames `[0, 3]`.
- It requires private/public crops `(298, 202, 339, 219)`, area `697`, and
  erase area `387`; it compares the actual crop pixels and statistics.
- The planted negative changes exactly 20 pixels, uses the 697 denominator,
  and asserts `20 / 697 > 0.02` without editing captured PNGs.
- Default/malformed inputs remain source-only unknown/no-inspection cases.
  No fabricated positive or default capture was added.
- The explicit-width four-still 799/387 helper is unchanged and is not the
  selected central test. No component, source geometry, padding, threshold,
  private crop, or statistics implementation was changed.
- The runner binds a clean full-commit checkout, requires the reviewed source
  as an ancestor, checks all tracked source bytes before and after, and uses
  the immutable public12 artifact (`77` files,
  `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`).
- It guards the full f816 dependency graph (`21,488` entries and tree
  `9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425`), all
  six peer hashes, Node20.19.4 by full SHA, Chrome155 by full tree SHA, the
  0700 private temp directory, browser flock, 10 GiB floor plus temp budget,
  quiet mode, exact fresh grant, one-shot `RUN_STARTED`, and scratch cleanup.

The stale source-root artifact manifest is not silently promoted. This handoff
is component-level compatibility preparation only; it supplies no normal
admission, Runtime, or Gate 7 evidence. If normal renderer admission for the
selected owner descendant requires artifact regeneration, the controller must
refuse/wait for that owner descendant rather than bypassing the requirement.

## Offline evidence

- Manifest/controller binding assertions: PASS.
- JSON parse, Python AST/compile, and READY shell syntax: PASS.
- Frozen `ee71010a0` source hash comparison: PASS.
- `git -C /home/user/work/agent apply --check --whitespace=error-all <...patch>`: PASS.
- Private extraction of Agent HEAD, patch apply, three Node `--check` runs,
  two Python compile checks: PASS.
- Composition `git diff --check` and status: clean.

No central test, browser, render, grant, network, install, live socket, full
suite, or git mutation was run. Therefore the actual 697px pixel/statistic
qualification and all external admission gates remain unverified.

## Required next step

The manager may perform exactly one fresh grant using the command in the
companion `-COMMAND` file, substituting a clean owner checkout and its exact
40-character HEAD. `READY_GRANTED` must equal that HEAD and it must be a
descendant of `ee71010a0`; do not reuse a rejected grant/controller. Preserve
the immutable artifact, dependency graph, browser lock, and resource guards.
