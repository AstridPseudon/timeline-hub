# Public S2 literal-media mixed journey

Worker: `rt-m2-public-s2-literal-journey-control`, 2026-10-20.

**Qualified: the separately authored literal-media control on the actual current Runtime/Agent pair. Original historical audio remains unresolved.** Central final result: **2 passed, 1 strict xfailed in 16.71s**, exit 0. No full suite was requested or run.

## Qualified subset

The existing positive mixed-journey body now runs for two independent films. The new `literal-film` uses the existing `_publication` request builder and real first-import publication ingress, followed by normal startup baseline verification. It has its own shot and internal-timeline identities, a title child, opaque values in the config/shot/child/parent clip, and one real managed WAV. `client.media.import_bytes` imports an actual 96,044-byte mono PCM WAV (8 kHz, 16 bit, 48,000 silent samples). Its authored source duration is read back with `wave`: frames/rate = 6 seconds. The test verifies retained CAS bytes and the media location. It does not invent a duration for the historical film.

The first-import setup occurs before the renderer tripwires. Every measured edit, restart, retry, undo and public read then runs with scene imports blocked and Runtime scene evaluation raising. This qualifies renderer-independent command saves, not renderer-independent legacy import.

The real CLI syntax is taken from current `cli_native.commit_trim`, `_trim_selector`, parser/tests, and the existing public M1 journey:

```sh
astrid timelines edit literal-film --clip parent/clip:literal-media --trim-out 4 --idempotency-key public-s2-cli-trim --project PROJECT --json
astrid timelines undo literal-film --publication PUBLICATION --project PROJECT --json
astrid timelines show literal-film --published --revision-id REVISION --project PROJECT --json
astrid timelines show literal-film --published --revision-id REVISION --layers --clip literal-media --project PROJECT --json
astrid timelines visualize literal-film --published --revision-id REVISION --mode inputs --format md --project PROJECT --json
```

The control proves:

- CLI captures its native trim and original revision/publication, exact disk-flight body/path/key and original guards before a real HTTP POST is paused outside the store lock.
- An independently authenticated Python editor commits `track.set` on `parent/track:music`; the stale CLI trim is rebased onto that publication, preserving the label and trimming only from/to/hold to 0/4/4 in both canonical mirrors.
- The server durably accepts the trim, then the existing `_send` seam drops its ACK. The original disk flight survives a real Runtime stop/start and is resent byte-for-byte under its original path/key. The identical receipt returns while semantic-provider execution is forbidden; the entire durable store dump and history remain unchanged.
- CLI guarded undo restores the complete labelled document, preserving the other author's label. Parent, shot/internal revision payloads, dependency manifest and opaque values are checked, as are retained verified media. Original history entries remain unchanged.
- Exact accepted and undo revisions are readable through show, layers and inputs visualize, including the older accepted revision after undo advances HEAD. Layers and inputs assert exact authored clip/track values and source identity; inputs explicitly remains `declared_inputs` evidence. No pixel/render qualification follows.

The historical archive and its original film are not changed. The separate film setup checks the original closure and history remain exact. No schema overlay, fake semantic provider, positive SQL history writes, product/API changes, new fixture archive, dependency install, pin change, merge or publication occurred. Only the existing test module changes in the repo (+158/-20). The shared test-service allow-list gained one bounded current-source suite; it writes no shared dependency or integration checkout.

## Original audio requirement

The complete historical mixed-intent success expectation remains in the same parametrized test, with its original `music-documents` capture, `clipType: audio`, and absent authored duration. It still requires capture before POST, stale rebase, lost ACK, restart, exact retry, undo, full closure and public revision views. It is not rewritten to expect refusal.

Only the historical parameter has `xfail(strict=True, raises=HistoricalAudioCaptureGap)`, linked to this requirement. That exception is raised only after an unchanged whole-store dump and absent disk flight are checked, and only for this exact CLI result:

```python
(1, {'data': None,
     'error': {'code': 'timeline_edit_error', 'details': {},
               'message': 'clip.trim applies to media clips'},
     'idempotency_key': '', 'ok': False, 'receipt': None})
```

Any other error or later assertion remains a failure; success becomes a strict XPASS requiring removal of the marker. Fixing only the audio type while leaving missing duration will expose the next failure rather than masking it. No claim that all Main trim/media forms are supported is made.

## Exact final sources and run

- Actual Runtime: clean integration `b748ae723b51c6d578ba7a393209ce37d6e2b0c3`, tree `1711b198be7f693f11ee4640eb0922ec0d0da952`.
- Actual Agent: clean integration `8e3107853d17453758a933d1f47215cc1c002660`, tree `7b395a0165b00808b9b554213ff015838e813e51`; observed unchanged after the run. Its staged-inverse guard is included.
- Actual Agent normal013 lock remains producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, contract/client `0.2.13`, artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.
- Assigned Runtime base: `a64cb4c55384350d705e5cbd4b5b15143a4805cb`; final candidate-test snapshot tree `7d2306bb9e665dc57b489ff3688568a0e6d75e39`.
- Final test module SHA-256: `727d77e12e79eff40c686cc11ef267d46578b6f92cb82b71d5e521811cc5f843`.

The assigned Runtime branch predates current integration's empty-shell/strict-JSON repair. Therefore final qualification explicitly loads the real current Runtime package before pytest, guarded by exact HEAD, clean status and its absolute `__file__`. This is ordinary source selection, with no copied or patched Runtime/schema files. The service still snapshots the candidate test changes; it records the actual Agent integration head in the external cache identity. Both actual source checkouts stayed read-only. This named command is also bound to the Runtime hash in the cache key.

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
"$ORCH/bin/request-test" rt-m2-public-s2-literal-journey-control public-s2-literal-current-integration --files 'tests/test_timeline_public_s2_mixed_cli_journey.py tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider'
"$ORCH/bin/wait-test" rt-m2-public-s2-literal-journey-control-public-s2-literal-current-integration-1020134500-16187 1
```

Exact central command, from the candidate-test snapshot:

```sh
test "$(git -C /home/user/work/runtime rev-parse HEAD)" = b748ae723b51c6d578ba7a393209ce37d6e2b0c3 && test -z "$(git -C /home/user/work/runtime status --porcelain)" && env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=/home/user/work/runtime:$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P -c 'import runtime_protocol, pytest, sys; assert runtime_protocol.__file__ == "/home/user/work/runtime/runtime_protocol/__init__.py"; print("Runtime source:", runtime_protocol.__file__, flush=True); raise SystemExit(pytest.main(sys.argv[1:]))' -q -p no:cacheprovider -m integration tests/test_timeline_public_s2_mixed_cli_journey.py tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider
```

The log confirms `Runtime source: /home/user/work/runtime/runtime_protocol/__init__.py`. Result: **2 passed, 1 xfailed in 16.71s**, exit 0. [Full log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-public-s2-literal-journey-control-public-s2-literal-current-integration-1020134500-16187/log.txt).

Direct fixture-neighbour check:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_commit_film_fixture.py
```

Result: **6 passed in 1.96s**. Final `git diff --check` and AST parsing also pass. Earlier candidate setup failures and the exact linked-child read refusal are retained in [DetailedReport](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-public-s2-literal-journey-control/DetailedReport.md).

## Handoff

No task execution blocker remains. Agent still owns historical audio capture/authoring with trustworthy source duration; Runtime owns this journey. Keep the original positive and its narrow strict marker until that requirement is restored. Review/merge the bounded test change through the orchestrator, then rerun on any successor source tuple. Investigate the separately recorded cross-timeline linked-child SDK read refusal independently. No full suite, browser/App journey, pixel/audio parity, all-writer or delivery gate is qualified by this result.
