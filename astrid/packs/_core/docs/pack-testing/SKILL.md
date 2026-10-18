---
name: pack-testing
description: "Write, review and run tests for an Astrid pack. Use when adding or changing a pack's tests, choosing between a unit test, the real Runtime daemon fixture and an editing scenario, putting a red test in known_failures.txt, deleting an obsolete test, or reviewing a pack change for test quality."
metadata:
  short-description: "Test Astrid packs: fewer, truer tests"
---

# Pack Testing

The yardstick and rulings (R-1 to R-13) are in the
[testing plan](../../../../../docs/development/testing-plan.md); this is the
part a pack author needs day to day. Build the pack with
[pack-builder](../pack-builder/SKILL.md).

## What a good test is

- **Fewer, truer tests.** A test earns its place by catching a failure nothing
  else catches. If another test, the validator or a conformance suite already
  fails on that break, do not add a second one.
- **Assert behaviour and identity** (R-8): "the output is revision R", "the
  task ended in state X", "the manifest lists these three files". Not private
  attributes, source strings or the wording of a message.
- **Durations are recorded, never judged** (R-10). Nothing fails for being
  slow; only a genuine hang does. The suite-wide hang guard is
  `timeout = 600` in [pyproject.toml](../../../../../pyproject.toml); a
  legitimately long test raises it with `@pytest.mark.timeout(N)`.
- **A fake is trusted only for what it reproduces from recorded real
  responses** (R-4). Anything else runs against the real thing.
- **Old checks go only once their assertions have homes** (R-1). Name where
  each useful assertion now lives before deleting the old test.
- **Red is never normal** (R-6): fixed, or owned and expiring (below).

## Where a pack's tests go and how they run

Put them in `tests/packs/<pack>/test_*.py`, with an `__init__.py` so a file
name shared with another pack cannot collide (as in
[tests/packs/video_editing/](../../../../../tests/packs/video_editing/)).
Never inside `astrid/packs/<pack>/`: collection is `testpaths = ["tests"]`, so
they would never run. The cross-pack contracts in `tests/packs/test_pack_*.py`
(layout, discovery, validation, recoverability) already cover every pack.

```sh
python3 -m astrid.core.pack.cli validate astrid/packs/<pack>   # structure only, not behaviour
python -m pytest tests/packs/<pack>                             # the default lane
python -m pytest tests/packs/<pack> -m integration             # that pack's integration tests
scripts/check-before-push                                       # before every push (R-12)
```

Lanes are defined in [tests/lanes.py](../../../../../tests/lanes.py) (R-2).
The default run deselects four markers; the nightly lane runs exactly those:

| Marker | When |
|---|---|
| `integration` | a pack host or other long-lived subprocess, Node, ffmpeg or Remotion, the network, or a second checkout (such as the Runtime) |
| `darwin_native` | native macOS APIs (skipped elsewhere) |
| `live` | real provider credentials |
| `opt_in` | explicitly opt-in, never in the default lane |

Choose the lane honestly: mark a test, or a module with
`pytestmark = pytest.mark.integration`, for what it really needs. Import a
declared dependency plainly (`pytest.importorskip` fails in a required lane);
load a module only the integration lane has with `require_module` from
`tests/lanes.py`.

## How to test an action

1. **Pure logic: a unit test.** Import the function from the action's module
   and feed it small, deterministic input, as
   [tests/packs/music/test_music_pack.py](../../../../../tests/packs/music/test_music_pack.py)
   does with synthetic signals. No Runtime, no subprocess.
2. **Runtime behaviour: the real daemon.** Use the `real_runtime` fixture from
   [tests/conftest.py](../../../../../tests/conftest.py). `real_runtime()`
   starts a daemon on a temp realm, `real_runtime(realm, support_root=...)`
   restarts one at a given realm, and every daemon is stopped at teardown. The
   Runtime is found by the one locator in
   [tests/helpers/runtime.py](../../../../../tests/helpers/runtime.py)
   (`ASTRID_RUNTIME_CHECKOUT`, or the `astrid-runtime` sibling).
   These tests are `integration`. Example:
   [test_runtime_publication_chain.py](../../../../../tests/packs/video_editing/test_runtime_publication_chain.py).
   Do not construct `RuntimeDaemon` yourself.
3. **A fake Runtime, only where it is verified.** A fake may answer only the
   operations recorded in
   [tests/fixtures/runtime-responses/](../../../../../tests/fixtures/runtime-responses/)
   (vendored under a lock), and it must be added to the shape checks in
   [tests/sdk/test_runtime_response_conformance.py](../../../../../tests/sdk/test_runtime_response_conformance.py).
   Do not write another general-purpose `FakeRuntime`.
4. **Editing intent: a scenario.** A timeline-editing verb gets one YAML
   scenario at `tests/editing_scenarios/<area>/<id>.yaml` (area is timing,
   structure, look, audio or code). The runner applies it through the CLI, a
   cut sheet and Python, and checks the documents agree, undo and redo, and
   idempotency. Format and fixtures:
   [tests/editing_conformance/README.md](../../../../../tests/editing_conformance/README.md).
   Run `python -m pytest tests/editing_conformance`.
5. **Contracts every pack meets.** Errors follow the
   [recoverable-error contract](../../../../../docs/contracts/error-model.md),
   held by [tests/test_recoverability_conformance.py](../../../../../tests/test_recoverability_conformance.py)
   (no bare raises or direct stderr writes). A render backend joins
   [tests/core/rendering/test_conformance.py](../../../../../tests/core/rendering/test_conformance.py)
   or [tests/packs/test_renderer_parity.py](../../../../../tests/packs/test_renderer_parity.py).

**Reap what you start** (R-9). Launch subprocesses through the
`owned_process_groups` fixture (`owned_process_groups.popen(...,
start_new_session=True)`, or `add_cleanup`). A leaked daemon or host process
group, or more than 64 leaked file descriptors, fails the session.

A change to `astrid/packs/rendering/**`, `remotion/**` or the host files also
needs the smoke before merge (R-11); `scripts/check-before-push` tells you.
Steps and options: [docs/development/journeys.md](../../../../../docs/development/journeys.md).

## Known failures

[tests/known_failures.txt](../../../../../tests/known_failures.txt) has one
line per known red test:

```text
<node id> | <owner> | <expires YYYY-MM-DD> | <reason naming file:line>
```

- **Owned and expiring.** An expired line fails the whole run: fix the test or
  renew the line. A line whose test is gone from a collected file fails too.
- **Strict.** A listed test runs as a strict xfail, so once it passes the run
  fails until you remove its line, in the commit that fixes it.
- **`flaky:`** A reason starting `flaky:` names an intermittent product race
  and runs as a non-strict xfail. It is owned and expiring like the rest.
- **Capped and shrinking.** The list only shrinks and ends at most 10 lines per
  repo. A line is for a product defect a test exposed that is too big to fix in
  the same commit (R-13), never for a test that is simply wrong. A small,
  unambiguous product fix rides with the test that exposed it.

A test of a removed design is deleted, not skipped and not fixed (R-7), with
a line in [tests/removed.yaml](../../../../../tests/removed.yaml) (`test`,
`reason`, `removed_by`). A test of a deliberately changed design is updated to
assert the new behaviour.

## What not to do

- **Sleep to synchronise.** Wait on an event, a file or a gate (R-10).
- **Pin strings.** No assertions on source text, log wording, private
  attributes or file absence as a proxy for behaviour.
- **Mock what you can run.** If a temp realm, a small fixture file or the
  `real_runtime` fixture can do it, use that instead of a mock.
- **Skip forever.** No `@pytest.mark.skip` for a retired design and no
  `importorskip` for a declared dependency. Delete, or put it in a lane.
- **Judge durations or add a framework.** No `elapsed < N` assertions, no
  tight timeouts, no new harness, runner or universal fake (R-7).

## Checklist

- [ ] Each test catches what nothing else catches, and asserts behaviour.
- [ ] Files are in `tests/packs/<pack>/`, with an `__init__.py`.
- [ ] Each test is in the lane it really needs; declared imports are plain.
- [ ] Runtime behaviour uses `real_runtime`; any fake is checked against recordings.
- [ ] Editing verbs have a scenario; errors pass the recoverability contract.
- [ ] No sleeps, string pins, duration assertions or permanent skips.
- [ ] Every subprocess is owned and reaped.
- [ ] Any known failure has an owner, an expiry and a file:line reason; any
      deleted test has a `removed.yaml` line and its assertions a named home.
- [ ] `python3 -m astrid.core.pack.cli validate` passes, the capability
      catalog is regenerated if actions changed, and
      `scripts/check-before-push` is green.
