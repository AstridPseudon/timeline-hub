# Parent-media genuine-drop evidence gate

## Result

The single authorized central gate was attempted against the coherent committed
donor `tl/ap2-m2-parent-snapshot-tree-guard-source`:

- original App commit: `74643bed98fc9bf3102f544bc189e6464510f58b2`
- original App tree: `a75e27930df49a0c4ee9005806d59b14f16d2361`
- donor parent/source-only commit: `d4c60b271d43df1512477cdbe2cf78dddf3a72e6`
- donor parent tree: `dea180c32cb49873215bd15b638d9fc8016ec008`

The private retained-evidence driver was updated to the donor's exact original
commit/tree. Its absolute runner/helper paths, locked cache prerequisite,
pre-build collection check, and bounded evidence copy-before-cleanup remained
unchanged.

## Guard review

The donor's App guard accepts a synthetic App `HEAD` only when the expected full
source tree matches and source is clean; the observed synthetic `HEAD` remains
reported. Agent, Runtime, and Runtime-producer identity checks remain strict.
The donor report records 16 pure guard tests passed; I did not rerun those tests
on a different tree.

## Central evidence

Command:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-snapshot-tree-guard-source ap2-m2-parent-retained-evidence-real-gate) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: **failed, exit 1 in 1s**, result
`ap2-m2-parent-snapshot-tree-guard-source-ap2-m2-parent-retained-evidence-real-gate-1020224252-16049`.
The service snapshot had the donor tree, but the private wrapper still required
`HEAD == expected_app_head`; the service's synthetic commit therefore stopped
the run before build, browser, socket, or evidence capture. `log.txt` and
`runner.log` were empty; no trace, request/response, console, refusal, wire,
or browser assertions were produced.

Consequently the intended exact external tuple (`3c4f6de4` Agent,
`20207411` Runtime, `a0dca169` producer, artifact `f021e771`, schema
`6ba7b51e`, Composition 0.0.13) and the requested negative/draft/add/retry/
reload/undo/opaque/no-double/zeroLegacy assertions remain unverified by this
run.

After this sole run, the driver was corrected locally to accept only the exact
expected full tree and clean source, while retaining the original expected HEAD
in `source-tree.txt`. No second gate was submitted.

## Tests and next step

- `sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-retained-evidence-real-gate/run-parent-manual-drop-evidence.sh` — passed.
- No product source, local driver, browser, socket, full suite, dependency, pin, or adoption test was run.

Exact postcommit command for the orchestrator, after reviewing the bounded
driver correction, is the same single named gate command above, targeting
`ap2-m2-parent-snapshot-tree-guard-source`; do not treat this worker's failed
attempt as genuine-drop evidence.
