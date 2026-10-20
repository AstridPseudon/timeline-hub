# M2 public-10 adoption: Bundle 1 + Composition 0.0.10

Status: **verified.** The exact-pair Runtime suite and the pin and conformance
suites pass. The Node-env node suite now passes 12 of 12 nodes after the shared
runtime lock was reinstalled from the committed lock (section 9). The earlier
TextCard SSR failure was environment drift, not code (section 4).

## 1. Commits and trees

| Item | Value |
|---|---|
| Adoption base (`tl/agt-public10-adoption`) | `fc6c1f26` (`feat(rendering): adopt Composition 0.0.10 with bundle 1 parent track labels`) |
| Finish branch (`tl/agt-public10-finish`) | `fc6c1f26` plus the uncommitted `git rm` of the 0.0.8 tarball |
| Test-service snapshot tree (Agent, includes the `git rm`) | `a158800a3d4878687912d0b0bc17698d6ede0d88` |
| Bundle 1 applied from | `tl/agt-m2-bundle1-pin` `3bf9e536` (based on `fc324e83`) |

Change in this step: `remotion/artifacts/banodoco-timeline-composition-0.0.8.tgz`
removed (`git rm`). Nothing in the tree references the 0.0.8 tarball any more
(`grep 0\.0\.8` finds nothing outside the old tarball itself).

## 2. Pins

**Runtime (exact pair).** Producer checkout `/home/user/work/wt/rt-m2-track-public-export`
at `6be970633cc82ab412428151e6bf42f3e7fc3081`, clean working tree.

- `runtime.lock.json` `source_commit`: `6be970633cc82ab412428151e6bf42f3e7fc3081` (matches producer HEAD).
- `runtime.lock.json` `producer_version`: `sha256:3b805d6946fd73c44144009021f44153b78ceeb5e5b1298cd2397a1f2dc19730`.
- Client `SCHEMA_DIGEST` (`astrid_runtime_client/contract_metadata.py`): `sha256:89a396aaa10a5ab6c29fb5f053bf12dd031be4a259c33ebc6a53489fcd5878d3`.
  This equals the same constant at Runtime `6be97063`.

**Composition 0.0.10.**

- Tarball `remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz`, sha256
  `cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7`.
  The copy in `/home/user/work/runtimes/agent-remotion-0010/artifacts/` has the same digest.
- `remotion/package.json`: `"@banodoco/timeline-composition": "file:artifacts/banodoco-timeline-composition-0.0.10.tgz"`.
- `remotion/package-lock.json` integrity: `sha512-SmJAoem9f+86D+eO+PvBAz3JydlefpUUwcOOkG7SU9k2ZPKpjXLWKHm/N4424TO5HNQtCHMt5T6Jy2Y5zA6Ycg==`.
- `astrid/core/rendering/remotion_runtime.py`: `_COMPOSITION_PACKAGE_VERSION = "0.0.10"`.

## 3. Test results

Test commands were run through the central test service (`request-test` / `wait-test`).
No full suite was requested.

| Suite | Command (abridged) | Result |
|---|---|---|
| `bundle1-runtime6be9706-integration` | exact-pair guard `git -C rt-m2-track-public-export rev-parse HEAD` = `6be97063`, then `pytest -m integration` over `test_commit_runtime_parent_track_label.py`, `test_commit_runtime_m1.py`, `test_commit_runtime_identity.py`, `tests/sdk/test_timeline_commit_provider_runtime.py`, `tests/stage1/test_runtime_client_cutover.py` | **pass**, 48 passed in 70.40s, exit 0. Service ID `agt-public10-finish-bundle1-runtime6be9706-integration-1020044639-19000`. |
| `remotion-0010-nodes` (`--files`: `tests/reshape/test_remotion_gate.py`, `tests/core/test_editor_element_catalog.py`, `tests/core/timeline/test_clip_fields.py::test_render_status_defaults_to_pinned_union_composition`, `tests/journeys/test_journey_plumbing.py::test_renderer_install_problem_names_the_missing_install_and_the_fix`, `tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup`) | env `ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0010`, Node `v20.19.4` | **fail**, 1 failed, 11 passed in 10.52s, exit 1. Service ID `agt-public10-finish-remotion-0010-nodes-1020044639-20937`. The failure is the TextCard SSR node (section 4). |
| Vendor lock | `scripts/vendor_lock.py check runtime.lock.json --producer rt-m2-track-public-export` | **Not run as a script.** The sandbox blocked Python execution. The check was reproduced by hand (section 5), with the same results. |

Targeted runs from the adoption worker (not repeated here, since this step only
removes one unreferenced tarball): `580 passed, 4 skipped, 33 deselected` for
pin, `editing_conformance` and neighbours; `1061 passed, 10 skipped, 33 deselected, 1 failed`
for rendering pack plus native and label tests. The one failure there was the
same TextCard SSR node (Node not on PATH in that sandbox).

## 4. The blocked node: runtime lockfile drift (environment, not code)

`TextCardVisibleMarkupTest` first checks that the selected Remotion runtime's
`package.json` and `package-lock.json` equal the snapshot's. The `package.json`
check passes. The `package-lock.json` check fails.

Normalised comparison (`jq -S .` of both files, then `diff`): the runtime lock is
missing 8 `libc` arrays (`"libc": ["glibc"]` / `["musl"]`, one per optional native package).
Versions, `resolved` and `integrity` fields are identical. This is an
npm-version artifact from the shared runtime install at
`/home/user/work/runtimes/agent-remotion-0010`, not a dependency change.

Not fixed here. The runtime directory is a shared environment path, and the
test is correct to refuse a drifted lock. Options, for the orchestrator:

1. Reinstall `/home/user/work/runtimes/agent-remotion-0010` from its committed lock
   with the pinned npm (`10.8.2`, Node `20.19.4`), then rerun the suite.
2. Or accept the drift only with an explicit decision. Do not weaken the test.

## 5. Vendor lock (manual reproduction)

`scripts/vendor_lock.py check` could not run here. The sandbox blocks Python
execution. The same checks were made with `jq`, `sha256sum` and `git`:

- Producer HEAD equals `source_commit`, and the producer working tree is clean.
- Manifest `producer` and `version` equal the lock's `producer` and `producer_version`.
- All 17 `files` entries: consumer bytes in this worktree, producer source bytes
  at `6be97063`, and the producer manifest `artifacts` value all have the lock's
  digest. No mismatch was found.

The script itself was not run, so this is a reproduction, not a pass of the
script. Re-run `python scripts/vendor_lock.py check runtime.lock.json --producer <6be97063 checkout>`
in an unrestricted shell to confirm.

## 6. Agent vendor lock behind Runtime `tl/integration`

Not moved in this step, per the brief.

- Agent client `SCHEMA_DIGEST`: `89a396aa…` (pinned to `6be97063`).
- Runtime `tl/integration` (`b2a1d9fd`) `SCHEMA_DIGEST`: `sha256:7486348fccf16b9104aa47d2076b68d1163931f765d8a4e7ec29415b5083bf22`
  (in `packages/python/astrid_runtime_client/contract_metadata.py`, `generated.py`, `runtime_protocol/contract_metadata.py`).
- The brief's `4e52f7df` was not found in the Agent tree or in `b2a1d9fd`. Its source is unknown and needs confirming.

## 7. Remotion gate

`scripts/reshape/remotion_gate.py` (`install` / `typecheck` / `parity`) was not
run in this worktree. `install` runs `npm ci` into `remotion/`, which would leave
build output in the worktree. The gate's unit tests (`tests/reshape/test_remotion_gate.py`)
did run and pass, as part of the 11 passed nodes above.

## 8. Open items

- Done: runtime lockfile drift fixed and `remotion-0010-nodes` rerun, 12 passed (section 9).
- Confirm the vendor-lock script result in an unrestricted shell (section 5).
- Confirm the `4e52f7df` source for the Agent-vs-Runtime schema digest comparison (section 6).
- Decide when Agent's vendor lock moves to Runtime `tl/integration` `b2a1d9fd`.

## 9. Rerun after the runtime lock fix

Precondition: `/home/user/work/runtimes/agent-remotion-0010/package-lock.json` is
byte-equal to the committed `remotion/package-lock.json` at `HEAD`
(`cmp` of `git show HEAD:remotion/package-lock.json` against the runtime lock: equal).
The worktree is clean at `ba633b20`, so the Runtime exact-pair suite was not rerun,
since the tree did not change.

Agent tree tested: `16d6528cb10310ac441bbf139c7aeb7f7ec51acf` (tree of committed `ba633b20`).
Section 1's `a158800a` was the snapshot tree before the `git rm` was committed.

Command (`request-test` / `wait-test`, `--no-cache`, no full suite):

```
request-test agt-public10-rerun remotion-0010-nodes --no-cache --files "tests/reshape/test_remotion_gate.py tests/core/test_editor_element_catalog.py tests/core/timeline/test_clip_fields.py::test_render_status_defaults_to_pinned_union_composition tests/journeys/test_journey_plumbing.py::test_renderer_install_problem_names_the_missing_install_and_the_fix tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup"
```

Service ID `agt-public10-rerun-remotion-0010-nodes-1020050742-21158`. Result: **pass**, exit 0,
`12 passed in 6.77s`. No failures, no skips.

| Node | Result |
|---|---|
| `tests/reshape/test_remotion_gate.py` (all nodes) | pass |
| `tests/core/test_editor_element_catalog.py` (all nodes) | pass |
| `tests/core/timeline/test_clip_fields.py::test_render_status_defaults_to_pinned_union_composition` | pass |
| `tests/journeys/test_journey_plumbing.py::test_renderer_install_problem_names_the_missing_install_and_the_fix` | pass |
| `tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup` (TextCard SSR) | pass |

The per-node breakdown above is by target; the pytest `-q` output gives the total
(12 passed) rather than a line per node. Section 4's blocker is resolved. No test
was changed, skipped or xfailed.

Remaining open items: section 5 (vendor lock script not run in an unrestricted shell),
section 6 (`4e52f7df` source), section 7 (Remotion gate `install` not run).
