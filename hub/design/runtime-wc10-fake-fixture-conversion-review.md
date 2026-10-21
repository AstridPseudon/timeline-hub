# WC10 fake-positive assertion-conversion review

## Verdict

**APPROVE the bounded fixture delta in `b3bc0f75f98352c209545d9621021b8867f21e0a` for the ULID/native-positive test only.** This approves the test-fixture repair, not the WC10 product migration, custom-canvas positive, stage landing, or legacy-route retirement.

The custom-canvas positive remains an explicit `@pytest.mark.xfail(strict=True)` at `tests/v10/test_timelines_create.py:233`, with the reason that native `timeline.init` does not preserve the custom legacy canvas. That unresolved positive is unapproved and continues to block the whole migration merge, as required by the handoff.

## Exact review basis

- Reviewed commit: `b3bc0f75f98352c209545d9621021b8867f21e0a`
- Parent: `a9f16a9ae1aec61de5dbcb42a0774cfda874bfc3`
- Reviewed tree: `99211b6b810acf1ede9719419a138d3f1715e45a`
- `a9f` tree: `e39cc79bc76de02727617915dcf4b82fdafe7d72`
- Original pre-stage commit: `5a625dd4c01149a085a9df85952b34cad70801f9`
- Original pre-stage tree: `d305ffabf98dcdb615979d7d18a44daec60abb4c`
- Diff scope: `tests/v10/test_timelines_create.py` only; `46 insertions, 7 deletions` (`git diff --numstat a9f16a9ae b3bc0f75f -- tests/v10/test_timelines_create.py`)

The original pre-stage test had three direct SDK tests: shell then whole-parent head, generated ULID/default empty parent, and shell refusal. `a9f` converted both positive tests to strict xfails. `b3` removes the xfail only from the ULID test, adds a native session/history-shaped fixture, and leaves the custom-canvas xfail unchanged.

## Original-to-native assertion mapping

| Original positive | Repaired native positive | Result |
| --- | --- | --- |
| Generated timeline ID is a ULID (`is_ulid`) | Same `is_ulid` assertion remains at line 278 | Preserved exactly |
| Default empty config was `{"tracks": []}` in the old parent publication | The no-config path is exercised; the native `timeline.init` command is asserted exactly, including schema/version/select and native default output resource (`1280x720`, `30`, `output.mp4`, null background fields) | Equivalent native positive; the old parent-config shape is not silently asserted as native data |
| Project/timeline reached the shell | `writer.calls[0]` still requires `("render-smoke", timeline_id)`; the replay/history lookup also requires `("P-1", timeline_id)` | Preserved/equivalent |
| Native name/default resource identity was implicit in the old path | Exact native command requires `args.name == timeline_id`, lower-case slug, and the complete output resource | Strengthened native assertion |
| Head idempotency key was `${result.idempotency_key}-head` | Native session capture requires the same key | Preserved equivalently |
| Old parent publication was the head write | Receipt result must contain exactly the captured native command, and no `publish_parent_composition` call is allowed | Correct native replacement; legacy write is positively rejected |

The shell-refusal test and all CLI tests remain unchanged. No negative test, malformed-input case, envelope assertion, or help test was removed. The only remaining xfail in this target is the explicitly documented custom-canvas positive.

## Fake safety and evidence boundary

`_Writer.list_timeline_commits` returns the ordinary history page shape (`items`, `next_cursor`), and `_NativeSession.commit` returns the ordinary accepted commit envelope through the existing `_accepted` helper (`data` with status/revision/commands plus a `timeline.commit` receipt). The test captures the command with a deep copy and compares it field-for-field; it is not a silent pass-through because a wrong command fails the exact assertion. The fake is test-local and does not add production authority or a special runtime path.

This remains unit fake coverage only. It is not installed-pair, native-daemon, HTTP, socket, renderer, schema, or pin proof. The prior handoff's native qualification requirement and the custom-canvas hold remain outstanding.

## Test evidence

Ran the one repaired test requested for this review:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" PYTHONDONTWRITEBYTECODE=1 \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/v10/test_timelines_create.py::test_remote_create_empty_generates_ulid_when_no_id_given
```

Result: `1 passed in 0.25s`.

No full suite, whole6/18 run, socket/browser/render/schema/pin run, install, or product edit was performed.
