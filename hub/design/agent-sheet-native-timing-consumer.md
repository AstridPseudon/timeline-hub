# AG03 native sheet timing consumer

Status: bounded `timing.for.card` slice complete; AG03 remains partial.

## Mapping and decision

| Main-positive fixture | Connected NativeSheet carrier | Result |
| --- | --- | --- |
| `timing.nudge-seconds.card` (`for 1s` → `on +0.1s for 1s`) | edit the retained row's absolute gutter; `NativeSheet.preview` emits existing `clip.move` against the original `parent/clip:<id>` ref | Already covered; no new code needed |
| `timing.nudge-frames.rocket` (`on "viral"` → `on "viral" -3f`) | requires a word-relative frame offset | Held: public `clip.move` v1 accepts an absolute authored `on` only, so adding this would require a new semantic/operation |
| `timing.for.card` (`for 1s` → `for 1.5s`) | NativeSheet's retained `hold=1` cell; existing `clip.set` capture updates source `hold` and the existing static `app.for` path | Implemented |

The missing `for` case was not a display-ID problem. A retained cut-owned row carries `app.cut` and `app.for`; `_hold_extent` already recorded the `for` read and write, but rejected the unrelated cut-ownership read before capture. The narrow fix permits `cut` as retained ownership metadata while keeping all extent, source, media, occurrence, and static-`for` guards. No parser format, operation, schema, pin, or fallback writer was added.

The NativeSheet test uses the original row binding and original bundle/basis, asserts the exact existing `clip.set` command, preserves the opaque cut/layer metadata, checks inverse and a disjoint rebase, then commits through the existing connected session and undoes it. The old no-client scenario assertions remain untouched.

## Evidence

From `/home/user/work/wt/agt-m2-sheet-one-native-timing-consumer`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_native_sheet_ordinary.py tests/editing_conformance/test_native_sheet_current.py tests/sdk/test_timeline_sheet_native.py
102 passed in 12.09s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_clip_scalar_provider.py
110 passed in 14.16s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_conformance.py -k 'timing.for.card or timing.nudge-frames.rocket or timing.nudge-seconds.card'
9 passed, 139 deselected in 2.05s
```

No full suite, live HTTP, browser, or currentserver run was requested or claimed.

## Remaining deletion blocker

AG03 cannot be marked deleted. The Main conformance sheet path is still
`tests/editing_conformance/runner.py::_apply_sheet` → CLI `apply` without
`--native` → `timeline_sheet.apply_sheet` → `_apply_parsed`/`merge_sheet` and
the detached Checkout save/journal. It must remain for unsupported Main-positive
sheet behavior (including creation/media/group/follow/narration/look/structure
and the remaining timing grammars). The native connected/default path and
explicit `--native` path retain their original basis and do not use this legacy
writer; this change does not remove or weaken that old path.
