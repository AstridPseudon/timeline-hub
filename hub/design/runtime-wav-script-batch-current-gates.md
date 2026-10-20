# Runtime WAV + script batch current gates

Date: 2026-10-20 UTC

## Verdict

**APPROVE the bounded current-integration evidence only.** The requested WAV
settlement/selection/replay, producer publication-only input ownership and
script retention, current HTTP/actor/project-scope boundaries, canonical
no-write guards, and stable continuation cases all passed on the current
Runtime snapshot. This is generic Runtime API proof only. It does not qualify
the Speech SDK, an actual outer voiceover workflow, a renderer/browser journey,
a public release, a consumer pin, or activation.

## Exact source and merge scope

- Local Runtime HEAD: `285a3b437c69d20e2af281c3d7fdd212cb784d1a`
- Merge parents: `4ec5d592176355bd5758a74dec696d8be7ef9b0c` (WAV topic) and
  `0113bc7d558d67816d88e4531c299d72a01eccb3` (script-input topic)
- Requested base: `285a3b437c69d20e2af281c3d7fdd212cb784d1a`
- Worktree was clean before and after testing; no Runtime source or test files
  were changed by this worker.

The merged topic delta is limited to the intended Runtime settlement/input
ownership paths and their tests:

```text
runtime_protocol/cas.py
runtime_protocol/service.py
runtime_protocol/store.py
tests/test_generation_publish_v1_settlement.py
tests/test_timeline_producer_guards.py
```

No public artifact path was touched by either topic diff.

## Exact central request and snapshot

One bounded targeted request was submitted; no full or whole-repository suite
was requested:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  rt-m2-wav-script-batch-current-gates targeted \
  --files "tests/test_generation_publish_v1_settlement.py tests/test_timeline_producer_guards.py tests/test_timeline_media_selection.py tests/test_timeline_verified_media.py tests/test_timeline_verified_media_http.py tests/test_timeline_source_document_boundary.py tests/test_task_continuations.py tests/test_timeline_authority_door.py")
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Request ID: `rt-m2-wav-script-batch-current-gates-targeted-1020173628-11584`

Snapshot:

- source tree: `b2b731c486f53d7a94589b71da18c665f67333e0`
- request key: `95af1afcdfe99f2fb465f6ee0d9c1a1a`
- request time: `2026-10-20T17:36:28Z`

The central runner executed:

```text
/home/user/work/venv-runtime/bin/python -m pytest -q \
  tests/test_generation_publish_v1_settlement.py \
  tests/test_timeline_producer_guards.py \
  tests/test_timeline_media_selection.py \
  tests/test_timeline_verified_media.py \
  tests/test_timeline_verified_media_http.py \
  tests/test_timeline_source_document_boundary.py \
  tests/test_task_continuations.py \
  tests/test_timeline_authority_door.py
```

Result: **120 passed in 30.71s**, exit 0. Per-file counts were 15, 42, 13,
28, 5, 2, 3, and 12 respectively. No skip, xfail, or new expectation was
added or reported.

The direct sandbox attempt reached 100 passed, but its socket-dependent cases
could not start `RuntimeDaemon` because this worker sandbox denies socket
creation (`PermissionError: [Errno 1] Operation not permitted`): one WAV HTTP
case failed at daemon startup and 19 HTTP/source/door cases errored. The
central run is the authoritative result for those same explicit files and
passed all 120 cases.

## What the bounded run proves

- Valid, invalid, explicit-null, and zero-rate WAV duration boundaries; exact
  selected-media reads; authenticated HTTP verified-media access; replay and
  stale-fence atomicity.
- Publication-only producer dependencies remain ordinary explicit CAS inputs,
  not continuation-derived inputs. The real foreign-project refusal,
  immutable admitted-target checks, exact proposal/artifact matching,
  private-capture dependency checks, single-consumption protection, atomic
  supersession recheck, and accepted replay all pass.
- UTF-8 voiceover script input remains pinned to the admitted CAS object across
  source-document update, Runtime restart, and exact task retry.
- Actual actor rechecks, credential/door-origin checks, foreign project scope,
  source-document scope, exact media identity, and no-write behavior pass. The
  source-boundary checks use the real Runtime HTTP/API and store snapshots; no
  source-guard implementation was monkeypatched. The existing no-renderer
  assertion is only a tripwire proving ordinary source commit does not invoke
  the renderer.
- Current stable continuation cases pass: declared-order admission and
  pagination, replay conflict and restart at admission, and failure/cancel/
  selected-retry/stale-settlement behavior. No source-permission or epoch
  behavior was altered by this worker.

## Public 0.2.13 byte preservation

Read-only checks passed:

```sh
/home/user/work/venv-runtime/bin/python generators/generate.py --check
/home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
```

The checked-in public release is `0.2.13`. The manifest contains exactly 75
artifacts with version
`sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.
Independent byte verification reported:

```text
public_artifacts=75 changed=0 missing=0
```

The merged-topic diffs contain zero paths from the 75-entry public manifest.
`git diff --check` passed and `git status --short` remained empty.

## Limits and next steps

No full, broad, all-repository, speech-model, Speech SDK, actual outer
voiceover, renderer, browser, or public-release qualification was run or
claimed. No shared dependency, generated artifact, source file, test
expectation, skip, or xfail was changed.

Per the settled request, the Runtime manager may request its one full suite
after the post-17:22 marker patch lands and its own checks are green. This
worker did **not** request that full suite.
