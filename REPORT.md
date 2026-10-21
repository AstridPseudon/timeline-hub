# vw-m3-partial697-retained-one-physical-0923

## Outcome

**FAIL before physical capture.** The one authorized central request ran the
partial697 collection and selected test only, then failed in fixture setup
because the central snapshot did not contain the installed public13
Composition package at its generated `remotion/node_modules` path. The
browser/renderer capture body did not start. This is not a pixel qualification,
and no equivalence is claimed.

No product/source assertion, browser codec, API/DTO, authority, or pin was
changed. The live Agent worktree remained clean at source revision
`b97a36d80c96865f30ab3474201930ca8c2f1458`, tree
`e6c592cc558da4310d921b86832eddc18ec69035`.

## Central run

- Registered suite:
  `agent e2e-viewing-partial697-retained-one-physical-0923`
- Test ID:
  `vw-m3-partial697-retained-one-physical-0923-e2e-viewing-partial697-retained-one-physical-0923-1021092730-22788`
- Request: exactly one `request-test`; waited on that same ID; no retry,
  alternate, full suite, or second request.
- Result: **FAIL**, exit 1, 6 seconds.
- Collection: both presenter-crop tests were collected; only
  `test_actual_registered_presenter_partial_crop_pixels` was selected.
- Failure:
  `ValueError: cannot verify missing rendering components: installed public
  Composition package is missing at
  /home/user/work/wt/.test-vw-m3-partial697-retained-one-physical-0923-e2e-viewing-partial697-retained-one-physical-0923-1021092730-22788/remotion/node_modules/@banodoco/timeline-composition/package.json`
- Central log:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-partial697-retained-one-physical-0923-e2e-viewing-partial697-retained-one-physical-0923-1021092730-22788/log.txt`
  SHA-256 `778cff72f4f75d7f94a776ef7218f95aa9be252446d8d53c426bcb041a6e3cce`.
- Retained result directory:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m3-partial697-retained-one-physical-0923-result`
  contains no raw PNGs, inspection JSON, comparator JSON, or manifest because
  setup failed before capture.

The Gate6 pinned worker had no live packet process and had written its own
preflight block before this suite was submitted; the central browser lock was
free afterward.

## Preflight commands

- `bash -n .../handoff-vw-m3-partial697-retained-one-physical-0923-COMMAND` —
  PASS.
- Reviewed runner `--retention-control` — PASS.
- Source/tree cleanliness, four source hashes, public13 archive hash
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
  Node20.19.4 hash
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`,
  Chromium1194 hash
  `63eca986a3fe7f523d2d6e79d9f13daf4f1c73c1d9013c2c4a05b123510145b4`,
  archive 77 members/no symlinks, isolation, lock guard, and disk floor —
  PASS.
- Collection command:
  `/home/user/work/venv-agent/bin/python -m pytest --collect-only -q
  -o addopts= -p no:cacheprovider
  tests/packs/rendering/presenter_crop_capture.py` — **2 collected**.
- Available storage at final preflight: `11722416128` bytes, above the
  `10737418240`-byte floor.

## Private/public statistics (source fixture only; unqualified)

The approved source assertions define, but this failed run did not physically
measure:

| crop | box | area | strict planted threshold | padding-16 statistic |
|---|---|---:|---|---:|
| private697 | `(298,202,339,219)` | 697 | count 15 is `>.02`; count 16 is `>.02` | `16/697` |
| public/compat799 | `(298,202,345,219)` | 799 | count 15 is `<=.02`; count 16 is `>.02` | `16/799` |
| erase | `(300,206,343,215)` | 387 | above threshold for planted controls | `0` |

Natural pair fractions, source/public registration, frame-zero, defaults
(private `None`, public `null`), raw-invalid behavior, and any
private/public equivalence remain **unqualified**. The explicit799 physical
run was not replayed.

## Next step

The central test environment needs the exact public13 Composition package
installed at the snapshot's `remotion/node_modules` path before any future
manager-authorized run. This worker did not retry or alter that environment.

