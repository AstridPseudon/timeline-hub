# Served PCM guard final review

## Verdict

**APPROVE — whole scope freeze-ready.** The guard-fix handoff closes the two
predecessor defects without changing product code or weakening the fixture:

- tracked and untracked source state is checked before the run;
- the complete source/project/helper/archive/package/dependency/environment
  preflight repeats in `finally` after pytest;
- a postflight failure turns a successful pytest into failure and preserves a
  nonzero pytest result;
- every original and prepared URL read is pinned to the live
  `InvocationAssetServer.port`;
- the native byte oracle, same-clock/envelope swap check, double-apply,
  forgery, wrong registry/asset, managed-digest/selected-byte, partial-batch,
  interruption, and cleanup assertions remain present.

The frozen artifacts match the READY handoff hashes exactly:

```text
controller 72f5c85e73082e068b2898e62ce33ce3bb6733129f929eb9333e8de734f63c3e
fixture    2298b10a512fe5b32a6ba20ed5b806a189ed4e6a065f125833bc91709b734ba8
regressions d7aa4ee955aca24bc72f48ff2a0cb805e4df41f97c88fd853a3575135c9f17d5
```

## Freeze-ready scopes

`--scope whole` is exactly seven central-only module cases:

1. native served WAV positives at 30 and 30000/1001 fps;
2. forged binding and double preparation;
3. changed staged bytes with sibling preservation;
4. partial preparation failure with owned-batch cleanup;
5. wrong managed bytes/digest before server start; and
6. interrupted consumption with server, attempt, staging, and source cleanup.

The whole scope is ready for one central run after the manager supplies the
final committed producer SHA, approved installed public12 project, exact Node
20.19.4 executable, and named suite registration. This review did not run that
listener-backed scope.

`--scope with-phase` is **DEFECT / NOT GRANTABLE**. It adds the two ordinary
RED cases for actual window and layer phase preservation. The source-owner
join prerequisites remain: retain the actual original compiled occurrence,
carry the trusted original/current pair through validation and serialization,
invoke the producer with that pair, and preserve the served-WAV/native-byte
assertions. No xfail, skip, refusal, second compiler, or tolerance widening is
appropriate.

## Required future-test proposal (not applied)

The frozen phase test currently slices with `RenderService._window_timeline`
first and then calls `prepare(props)`; that is the predecessor RED shape. The
current inactive producer interface now accepts the real entry directly, so a
future phase fixture should keep `props` unsliced and call:

```python
output = prepare(
    props,
    window=FrameWindow(start_frame=15, end_frame=45, fps_rational=(30, 1)),
    tracks=tracks,
)
```

It should retain the existing HTTP URL binding, native oracle, input
immutability, and window/layer assertions. This proposal is only for the
future phase test; the frozen guard-fix fixture was not edited. Until that
real-entry test is run centrally and the source-owner transport is proven,
the whole pass must not be described as phase coverage.

## Checks run

```sh
D=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check \
  "$D/handoff-vw-m3-served-pcm-guard-fix-controller.py" \
  "$D/handoff-vw-m3-served-pcm-guard-fix-test_normal_audio_served_sources.py" \
  "$D/handoff-vw-m3-served-pcm-guard-fix-guard-regressions.py"
```

**PASS** — `All checks passed!`

```sh
T=$(mktemp -d /tmp/vw-m3-served-pcm-guard-review.XXXXXX)
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=/home/user/work/wt/vw-m3-served-guard-final-review \
/home/user/work/venv-agent/bin/python -B -m pytest -q \
-c /home/user/work/wt/vw-m3-served-guard-final-review/pyproject.toml \
-p no:cacheprovider --basetemp "$T" \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-served-pcm-guard-fix-guard-regressions.py
```

**PASS** — `4 passed in 0.33s`.

`git diff --check` — **PASS**; review worktree remains clean.

No source grant, HTTP listener/socket, browser, fixture execution, central test
service, full suite, install, or repo product/document change was run or made.

## Next steps

Freeze the three artifact hashes, obtain the manager’s final producer SHA and
approved public12 project, register one `whole` central suite, and run it once.
Keep `with-phase` blocked pending the real-entry test proposal and the four
source-owner join prerequisites.
