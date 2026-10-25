# F/D141 independent pristine-source review

## Verdict

**FAIL.** The frozen tuple and historical D134 census are conserved, but the
prep commit is not publishable as an exact operational evidence packet. The
failure is documentary/guard completeness only; no product adoption or body
execution was performed.

## Retained claims

- The four frozen tips, trees, and official origins are exact:
  Agent `8b6ed2116fd1803d24b2be5bc08bd9490407fe4a` / tree
  `0a3691a49b63fd7b0c22fb3478e9cf1947f266ed`, Runtime
  `fa9cd5464a8b37b02f971de375e56be846cd69e2` / tree
  `124e10dbcd54fb90219e783ec11aa34f8c91590c`, App
  `7ca61bb3280beca21d98a854af266a382f7ce5df` / tree
  `974de7cd08900872eeb0bd6f6004d44323e01fab`, and Composition
  `67b8aa3d0d6831d3e3504a340ff583c3da253707` / tree
  `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`.
- The five named roots recorded absent from frozen Agent are absent in that
  Git tree, and the D73 launcher and manager manifest-maker are absent there.
- The D134 packet conserves 52 disjoint groups and 370 unique IDs. Its finite
  classification remains 132 setup/expectation proved, 0 product fault proved,
  212 UNKNOWN, 14 UNVERIFIED_CURRENT_REG, and 12 PRIOR_UNKNOWN.
- `media48` is a subset of `managed105`/`root-019`: exact sets are 48 and 105,
  so the prose sum 153 is not additive. The seven named slices and all 370
  IDs were checked against the controlling per-ID/root files.
- The C0 request/reply inventory in the prep notes retains the required fields,
  including preview `would_status` with null receipt/writes. No production
  caller change is implied; Runtime’s registered `commitTimeline/provider`
  remains the production seam.
- `NOT_READY` remains the correct disposition. No controls, proof, REG, core,
  acquisition, checkout creation, Store write, or product/test result is
  credited.

## Findings

1. `git diff --check` is not PASS on the exact prep commit. The exact command
   returned exit 2: `evidence/notes-input.md:244: new blank line at EOF.`
   This directly contradicts `evidence/validation.md`.

2. `evidence/recipe.sh` does not run the advertised controls. It checks the
   retained stub hash and reads counter files, but has no `P4_STUB_COUNT`, no
   `dry` launcher call, no stub call, and no poison-manifest launcher call. Its
   only launcher invocation is a positive-manifest `run` body. Therefore the
   service row’s expected positive `0/17/1` and poison `1/0` outcomes are not
   produced by this recipe.

3. The recipe’s `env -i` body omits `P4_D73_EVIDENCE` and
   `P4_D73_REQUEST_ID`, both required by the reviewed current launcher. Binding
   `EVIDENCE_ROOT` is not equivalent. A future invocation would fail before
   the advertised launcher preflight/evidence capture.

4. The finite missing-input inventory omits three current-launcher-required
   P4 sources, all absent from frozen Agent:

   - `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py`
   - `tests/editing_conformance/test_p4_ten_note_v2_runtime.py`
   - `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`

   The current launcher’s self-location guard and `original_p4_test_hash`
   guard therefore cannot simply target pristine. This is an additional
   missing-input fact, not permission to copy or overlay those files.

5. The prep packet uses `4700000000` as its only disk start threshold. The
   assigned review scope requires source floor `4600000000` and stop
   `4000000000`; the controlling source-only qualification distinguishes that
   from the separate one-time core start `4700000000`. The packet must not
   collapse these settings.

6. No truly supported pristine-compatible external route is evidenced. The
   current Agent launcher is real and hash-verified, but its source-location
   guard requires it to live under the pinned Agent checkout. The identified
   manifest-maker is a manager recipe, not a standalone pristine generator,
   and the Composition D73 candidate explicitly says
   `CANDIDATE_NOT_INSTALLED`/`NOT_READY`. The hypothetical external route in
   `supported_route` must remain unbound.

7. The prep’s own dependency/manifest inventory is not exact-source complete.
   It checks presence but does not publish or verify the D73-required Node
   version, profile lock/archive/registry hashes, schema digest, composition
   version, runtime.lock source/file hashes, parent guards, or
   `original_p4_test_hash`. Those are later launcher guards, not evidence that
   the prep has already satisfied them.

## Exact scope questions

- Who supplies a real external launcher/manifest-maker that satisfies the
  pristine self-location and P4-source guards without source copy/overlay?
- Is this row source-only, or does it also own a future core body? Preserve
  both `4600000000` source admission and `4700000000` one-time core start if
  both apply.
- Where is the final U2 freeze receipt/head and the fresh positive/poison
  manifests/counters? Until those exist, retain `NOT_READY`.

## Review boundary

Only read-only Git object/tree checks, source inspection, JSON parsing, the
finite set comparison, hash checks, and shell syntax validation were used.
No pytest/import/provider/collection/control/full/body/acquisition/checkout or
Git write was performed by this reviewer.
