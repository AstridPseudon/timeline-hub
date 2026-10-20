# Final frozen-source gate: mouth697 partial presenter

## Verdict

**APPROVE the corrected component-level source/controller handoff for a future
central run, conditional on rehydrating the named clean Agent worktree.** Do
not grant or run it yet. The source and controller are verified below; the
dedicated checkout `/home/user/work/wt/vw-m3-mouth697-clean-source-descendant`
is currently absent.

**REHYDRATE request:** the Agent manager must materialize that path from
`tl/vw-m3-mouth697-clean-source-descendant` at
`ef4ebb23ded522c41569eb2355ee7f4a465aa4cd`, verify it is clean, then provide a
fresh independent `REVIEW.md` and `READY_GRANTED` for that exact SHA. The
existing worker has no grant artifacts (`REVIEW.md`, `READY_GRANTED`,
`RUN_STARTED`, and `POSTFLIGHT_OK` are all absent).

## Frozen source

- Base/product source: Agent `ee71010a0947edcbbacbf8178e5fee11ab6bab3d`.
- Completed descendant: `ef4ebb23ded522c41569eb2355ee7f4a465aa4cd`.
- Final Git tree: `604e4c1b808e395bde56b1068f4460774942425e`.
- The Agent repository checkout used for Git-object verification was clean.
- The diff from `ee710…` is exactly five added files, all committed:
  `presenter_crop_capture.mjs`, `presenter_crop_capture.py`,
  `presenter_crop_entry.mjs`, `presenter_crop_partial_capture.mjs`, and
  `test_presenter_crop_partial_physical.py`.
- All eight manifest product/source hashes match the descendant blobs; no
  presenter product file changed.
- The reviewed patch's SHA is
  `9624922e36ff9668d2458704368a16ea87d4e82551959e46d9e0b197ca122d5c`, and
  the independently generated `git diff --binary ee710… ef4ebb23…` has that
  same SHA.

## Controller and manifest

- New corrected controller:
  `handoff-vw-m3-mouth697-clean-source-descendant-controller.py`
- Controller SHA256:
  `005b01bc3ed95a7da5ee5f6e5035fda27db30d66357d90ee5eafd38c813a84fb`
- Manifest SHA256:
  `8d3d3d2842b88516725a799ea5a8a10f4c178f86ffaf205857769686eea9694a`
- The controller binds the exact manifest and patch hashes, base revision,
  final revision supplied by the future command, all listed product source
  hashes, dependency/browser identities, and a clean Git source state. The
  final revision/tree plus the exact five committed blobs bind the added test
  code; the manifest's patch hash independently binds the complete reviewed
  diff.
- Dirty-source validation runs before `RUN_STARTED` is created. Postflight
  rechecks source, peers, browser, and tool bytes before writing
  `POSTFLIGHT_OK` containing the final source SHA.
- The old approved controller with the wrong recycled Node path remains
  historical and is not referenced by the runnable command below.

## Contract retained

- Partial raw input is exactly `mouth: {x: 151, y: 104}` with width omitted.
- The future physical case is exactly frames `[0, 3]`, public/legacy crop
  `(298, 202, 339, 219)`, area `697`, and the unchanged strict `> 2%`
  comparator with a 20-pixel negative.
- Default and malformed/raw-invalid source cases remain unknown/no-inspection.
- Existing explicit-width controls remain unchanged: four stills `[0, 3, 4,
  5]`, crop area `799`, erase area `387`.
- This is component-level only. It does not regenerate or bypass runtime
  admission or a stale root manifest.

## Environment gate

- Retained Node path:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node`
- Node SHA256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`,
  version `v20.19.4`.
- Dependency graph: ref `f8164bef73215272562c4d6974acadbd82c2898a`, 21,488
  entries, tree SHA256
  `9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425`; all
  six manifest peer hashes match.
- Immutable public12 artifact SHA256
  `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, with
  77 regular files.
- Chrome package `155.0.8059.84-1`; 255-entry tree SHA256
  `5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e`.
- Controller requires at least 10 GiB free plus a 512 MiB temporary budget.
  Read-only preflight observed 12,265,742,336 bytes free versus
  11,274,289,152 required.
- Controller requires the viewing quiet marker to be absent, the external
  flock `/tmp/timeline-viewing-browser.lock` to be held, a 0700 private temp
  directory, and one-shot pre/post markers. These were statically audited;
  no browser/render/socket execution was attempted.

## Checks rerun

- `git archive ef4ebb23…` source extraction and manifest/product/blob/patch
  audit — **PASS**.
- Retained Node `--check` on all three new `.mjs` files — **PASS**.
- Python bytecode compilation of both new Python files — **PASS**.
- `pytest --collect-only` for
  `tests/packs/rendering/test_presenter_crop_partial_physical.py` — **1
  collected, PASS**.
- No browser, render, socket, network, install, grant, full suite, or runtime
  admission operation was run.

See the companion `handoff-vw-m3-mouth697-frozen-clean-gate-COMMAND` for the
literal future command and `...-fingerprint.json` for machine-readable hashes.
