# App2 current95 normal014 runner-profile custody review

## Disposition

**HOLD.** The runner repair is not custody-approvable for the required
final95 cohort because it does not bind the required App source commit/tree
`10fa2ff9a8216604aa39e3584f89dc9e7a09080a` /
`01fd2a04ff0c383ec5281043c7e5a4c843d1d835`.

The final95 Agent/Runtime/artifact/schema profile is correctly closed and the
historical old202 default remains valid. The missing App identity is a precise
source-custody defect; no real gate is approved or requested by this review.

## Author completion and changed artifacts

The author worker `ap2-m2-main95-existing-runner-profile-repair-0108` completed
with exit 0 and `DONE` before this review. Its frozen report is:
`design/ap2-m2-main95-existing-runner-profile-repair-0108-REPORT.md`.

The report's before/after hashes were checked against the author log and the
after hashes were recomputed directly:

| Path | Before SHA-256 | After SHA-256 | Review |
| --- | --- | --- | --- |
| `design/normal014-source-common.sh` | `c48d03d9c07e10216f5da2474ba10b608430975039bb6eec84ac3f2d0d6e7d5a` | `1e3708e5dff0b0acc251e9c97d802aa39383fe52435d229448e3517ebbe9a101` | matched |
| `design/normal014-app-central.sh` | `1c784bec132f50ccfb29ea825bd32de28448eafaede1dbeb7f937cb3df252c08` | `766e0b6a38a5d450a92aee8424d181041c54d523a8ea1427316cf02f3809d68c` | matched |
| `design/normal014-parent-media-central.sh` | `383ace5a4ff5d197f24b2e92f31f829f78b9263513df70b5e457843b66229461` | `69507020c13b7351fd8350e39e481a186f21d4d4c4a98300102a4625f1142ffb` | matched |
| `tests/suites.conf` | `f14ad04c2529ae0fb9e4b6c8989afac5b540c3edec83041351acc50df2d9748d` | `f4f2dbffaee51a9213b87ff449fd432cff4dfbab5bc7adb3a35849ae79da14e4` | matched |

Only these four authorized orchestration artifacts changed. The assigned App
worktree remains clean; no product source, lock, generated file, shared
dependency, Runtime, Agent, or venv file was changed by this review.

## Exact identity checks

The final95 constants in `normal014-source-common.sh` bind:

- Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`;
- Runtime and producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`;
- 76 artifacts, package bytes
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`;
- Runtime wire schema
  `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`;
- raw Agent schema
  `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
- unchanged public13 graph/archive and Composition bytes, including archive
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30` and
  Composition `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

The helper also validates checked-out Agent/Runtime commit and tree, clean
source checkouts, producer ancestry, every manifest artifact byte, schema
equality, private node graph separation, cleanup traps, and the existing
browser lock. `AGENT_REPO` and `RUNTIME_REPO` are location overrides, but the
requested commit/tree and byte checks prevent them from supplying unchecked
source authority.

The historical `old202` profile is still the default and resolves to the
original Agent `3c4f6de4fa777323b3386c01c7266b619b86af6d`, Runtime
`202074110717146fc7f08af2306a8dd7f695b0b1`, producer `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
75-artifact profile. Unknown profile names fail closed.

## Precise custody defect

`normal014-app-central.sh` currently:

1. accepts caller-supplied `app_root` and checks only `package.json`;
2. copies that tree into a disposable overlay;
3. checks only that its lock starts at the public base Runtime commit
   `2c4ac180c2220bdad966bc01e95ad230e99ce26a`;
4. rewrites the overlay lock to the selected Runtime SHA and runs the normal
   vendor updater/checker; and
5. checks generated-byte and schema hashes.

It has no App SHA/tree constants and no `git rev-parse`/tree guard for App
`10fa2ff9` / `01fd2a04`. Generated-byte equality does not bind the remaining
App source, tests, or callers to that exact cohort. The registered suites are:

```text
app normal014-integration-parent-media-accepted env NORMAL014_PROFILE=final95 bash .../normal014-parent-media-central.sh run
app normal014-integration-e2e-gate5 env NORMAL014_PROFILE=final95 bash .../normal014-app-central.sh run "$PWD"
```

They therefore receive the current App integration snapshot. At review time
that snapshot was App commit `813a85106ecb4abbaf224081abe6c33b8dab0df7`,
tree `2a19a78bb1bdfb3fd779f568a1b513b094318982`, not the required `10fa` /
`01fd` pair. The exact required App objects are present in the App repository.

This also explains why the author's central run reaching final95 source
preflight does not establish same-cohort custody. The run later had one
browser failure at the existing 90-second `waitForCreatedProjectResponse`
wait; it is not a profile approval or a real-gate result.

## Checks run

Passed locally, offline and without browser/socket/full execution:

```text
sh -n design/normal014-source-common.sh design/normal014-app-central.sh design/normal014-parent-media-central.sh
  PASS

old202 identity smoke against the common helper
  PASS

final95 tuple smoke: Agent/tree, Runtime/tree, 76, 54205, schema7d4, raw6ba
  PASS

invalid NORMAL014_PROFILE refusal
  PASS

App identity-guard search for APP_SHA/APP_TREE/10fa/tree01fd or an App git tree check
  FAIL as expected: guard missing (this is the review defect)

git show identity checks:
  Agent 6efc815... -> tree 2ed2b8...
  Runtime 95bd3c... -> tree d3a290...
  App HEAD 813a851... -> tree 2a19a78...
  App required 10fa2ff... -> tree 01fd2a...
```

The author reported its final95 source/artifact preflight stopped at private
Python dependency installation because the sandbox has no network. The
central run's final95 pre-browser preflight/build/collection passed, but its
browser portion failed as described above. No local real gate, full suite,
browser, localhost, or socket run was performed by this reviewer.

## Required next step

Repair the existing final95 opt-in path so it asserts and uses App commit
`10fa2ff9a8216604aa39e3584f89dc9e7a09080a` and tree
`01fd2a04ff0c383ec5281043c7e5a4c843d1d835`, while preserving old202 default
behavior and the existing normal updater/checker, artifact, schema, public13,
cleanup, lock, and failure guards. Then repeat this independent custody
review before any real parent or Gate 5 request. Do not relabel the central
browser failure as a profile or gate pass.
