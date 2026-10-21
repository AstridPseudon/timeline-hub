# App M2 producer central-prefix first-cause — 0617

## Result

Diagnosed and corrected the exact central-only empty-log failure from result
23173. The failure was not a source, probe, TSX, wrapper, package, Agent, or
Runtime mismatch. The central test service snapshots the target worktree by
creating a synthetic commit with `git commit-tree`, then runs the registered
command from that snapshot. The custody gate compared the snapshot's commit
hash
(`git -C "$PWD" show -s --format=%H HEAD`) to `FINAL_HEAD`. The snapshot
tree was exact, but its commit identity was necessarily different, so line 66
returned 1 before the source gate was entered. With `set -eu`, this produced
the empty log.

The independent central diagnostic observed:

- service source tree: `fd16d32fd3487e56c9fe1ff16582dba240f63b77` — expected and PASS;
- service synthetic commit: `732c811ca9e4ce0e576ad0c0339d9ac52623a948`;
- expected source commit: `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7`;
- all other custody predicates passed: keeper HEAD/tree/clean state, KEEP
  marker, node_modules symlink, wrapper/source/startup/probe/TSX/loader/package
  hashes, Agent and Runtime refs/clean states, and spec/helper/config hashes;
- TSX canonical realpath passed:
  `/home/user/work/app/node_modules/tsx/dist/cli.mjs` on both sides;
- gate path length was 179 bytes and gate file length was 4469 bytes.

The one-line corrected copy changes only the central snapshot identity check:

```diff
-test "$(git -C "$PWD" show -s --format=%H HEAD)" = "$FINAL_HEAD"
+test "$(git -C "$PWD" show -s --format=%T HEAD)" = "$FINAL_TREE"
```

The existing immutable gate remains unchanged at
`0ffea3e0ed4f78c5ebdd73d090ed9fd919a9430e3cfe7696ae9cd4847e638287`.
The corrected generated gate is
`66a0410164b53fef514ad661a04e5b8322355636a3840ea6519ea0dd981710c9`
and remains 4469 bytes.

## Exact service commands and results

The failed prior command was:

```sh
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-tsx-canonical-guard-one-line-0609/producer-startup-final-custody-gate.sh | cut -d' ' -f1)" = 0ffea3e0ed4f78c5ebdd73d090ed9fd919a9430e3cfe7696ae9cd4847e638287 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-tsx-canonical-guard-one-line-0609/producer-startup-final-custody-gate.sh preflight
```

Result: `…-23173`, FAIL exit 1, empty log.

The one source-only central diagnostic ran once, in the service snapshot cwd:

```sh
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-central-prefix-first-cause-0617/producer-startup-central-tree-gate.sh | cut -d' ' -f1)" = 66a0410164b53fef514ad661a04e5b8322355636a3840ea6519ea0dd981710c9 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-central-prefix-first-cause-0617/central-predicate-diagnostic.sh "$PWD"
```

Result: `…-1021062015-28023`, PASS. The diagnostic's predicate results
identified only the synthetic commit mismatch above.

Offline literal proof:

- correct generated gate path/hash/quote: PASS;
- wrong path: REFUSED;
- wrong hash: REFUSED;
- wrong POSIX quoting: REFUSED;
- immutable gate hash: INTACT.

The one permitted corrected source preflight used the exact target
`ap2-m2-producer-realm-physical-path-diagnosis-0538`:

```sh
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-central-prefix-first-cause-0617/producer-startup-central-tree-gate.sh | cut -d' ' -f1)" = 66a0410164b53fef514ad661a04e5b8322355636a3840ea6519ea0dd981710c9 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-central-prefix-first-cause-0617/producer-startup-central-tree-gate.sh preflight
```

Result: `…-1021062113-2043`, PASS; public13 preflight PASS, checks=10.

The one existing startup smoke was then run once via the same target using the
corrected registration
`ap2-m2-producer-central-prefix-first-cause-0617-startup`, which invokes the
existing `producer-startup-only-gate.sh` smoke:

```sh
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-central-prefix-first-cause-0617/producer-startup-central-tree-gate.sh | cut -d' ' -f1)" = 66a0410164b53fef514ad661a04e5b8322355636a3840ea6519ea0dd981710c9 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-central-prefix-first-cause-0617/producer-startup-central-tree-gate.sh startup
```

Result: `…-1021062152-17029`, FAIL exit 1. Preflight still passed, then
the existing probe failed with:

```
Error: Transform failed with 3 errors:
producer-startup-only-probe.ts:10:22: ERROR: Top-level await is currently not supported with the "cjs" output format
producer-startup-only-probe.ts:75:0: ERROR: Top-level await is currently not supported with the "cjs" output format
producer-startup-only-probe.ts:76:0: ERROR: Top-level await is currently not supported with the "cjs" output format
```

Per instruction, stopped on this first new startup failure; no retry and no
producer case/body, Vite, build, browser, full suite, or install was run.

## Protected hashes

- source HEAD/tree: `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` /
  `fd16d32fd3487e56c9fe1ff16582dba240f63b77`;
- wrapper: `329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352`;
- source gate: `c365641bdeca10b9d740d5968c9a1161db7b18f8bf49e9d8bd46f14aae60cfab`;
- startup gate: `8f3be0c8fcb18ab474b8d5b31c8b6a17b1cdc3d02324b4159d184c266357013c`;
- probe: `4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6`;
- TSX executable/CLI: `8729ecfb90d9d568939e4190e6f1d3317c946583b7d37a776e0c23a21c021cf8`;
- TSX loader: `0b1c5b86192772fe9257710e739959cee5947c11ae1f93b61abfaa9b80c6def1`;
- TSX package: `6e764b21991c21595441f82387c1451ccd10a3e7a3f0973cc5e3649a12dea7d2`;
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55` /
  `236c3e57e0265c52b81ba8085de3193026176bff`;
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` /
  `7ab412cc4bcbe517efcfa806e092336390312e18`;
- spec/helper/config:
  `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`,
  `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`,
  `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`.

## App changes

No App source, probe, test body, wrapper, dependency, or graph file changed.
The worktree remains at source HEAD/tree above and clean. The corrected gate and
diagnostic are worker-owned orchestration artifacts under the requested
scratchpad worker directory; no Git refs or commits were created.

