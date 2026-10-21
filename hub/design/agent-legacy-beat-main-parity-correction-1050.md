# Agent legacy beat Main/native parity correction

## Corrected tree

- Worktree: `/home/user/work/wt/agt-m2-legacy-beat-main-parity-correction-1050`
- Branch: `tl/agt-m2-legacy-beat-main-parity-correction-1050`
- Base/source HEAD: `e6168133f32e908ce984ee3855ebb690e838acfa`
- Corrected tree is the uncommitted diff from that HEAD; binary diff SHA-256: `8f331b066d71762ae84e18adcaeb30bc70a3fd42aa6835bd5210b015d099be31`
- Changed files: `astrid/sdk/timeline/_timing_evaluators.py`, `astrid/sdk/timeline/compiler.py`, `astrid/sdk/timeline_intent.py`, `tests/sdk/test_timing_compiler.py`

## Carrier decision

`bars` is not a supported Main downbeat carrier. `origin/main` (`497714c73531f164082555ec81b61ca5bc8b6554`), approved current integration (`b3c96a758c1cfa2a609d1498e0e9ee401b32cc40`), and frozen R4 candidate SDK (`11caf1d9de291d76f491cf69f7942606b7471d7a`) all implement `beat_sources()` as `downbeats` for `downbeat` and `beats` for ordinary `beat`; none falls back to `bars`. The same sources retain `bars` when normalizing/storing a beats file, so preservation of the opaque/stored field is distinct from moment resolution.

The native alias was introduced by the beat port in `astrid/sdk/timeline/_timing_evaluators.py` (`60d95d69f`, lines 149–151 before correction). The current Main helper had no fallback in origin/main or current integration, so no Main fallback was accidentally removed and Main was not edited. The correction removes only the native `bars` fallback. The compiler capability text is restored to describe the implemented numeric `beats`/`downbeats` support, and the unused `Iterable` import from the landing is removed.

## Assertion mapping

- `beats` carrier: positive preserved in `tests/sdk/test_timing_compiler.py::test_main_numeric_beat_carrier_resolves_legacy_moment_without_mutating_neighbor` and the real-fixture Main/native parity case.
- `downbeats` carrier: genuine positive preserved in the same fixture case and explicitly checked against Main (`1.0`) and native (`Fraction(1)`).
- `bars`-only carrier: the invented positive is converted to refusal in `test_numeric_beat_carrier_refuses_unsupported_bars_alias`; the real-fixture case asserts both Main and native refuse it.
- Existing malformed-carrier, empty-table, source speed/window/half-open, ownership/order, replay guards, placed-audio selection, and transcript correction assertions remain unchanged.
- No schema/client/pin/authority/retry/threshold changes.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timing_compiler.py -k 'beat or native'` — **9 passed, 40 deselected**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_checkout.py -k 'beat'` — **2 passed, 102 deselected**.
- `/home/user/work/venv-agent/bin/python -m ruff check --select F401,I astrid/sdk/timeline/_timing_evaluators.py astrid/sdk/timeline/compiler.py astrid/sdk/timeline_intent.py tests/sdk/test_timing_compiler.py` — **passed**.
- `git diff --check` — **passed**.
- Direct probe after correction: `downbeats` gives Main `1.0` and native `1`; `bars` gives Main `TimelineEditError` and native `TimingCompileError` (`0 downbeats`).

No full, repeated-57, native/HTTP, browser, renderer, or live-socket suite was run.


## Current-forward ready packet

- Approved source/tree: `da7312fe1ec88107da33ce33d557891a5345ab85` / `06cd859fa0b73490db404580a052d692d5c7cd79`.
- Current base/tree: `00e73f9252ce9dc45ade5819f7b044d5c190933a` (current00e).
- Forwarded blobs, byte-for-byte from the approved source: `astrid/sdk/timeline/_timing_evaluators.py`, `astrid/sdk/timeline/compiler.py`, `astrid/sdk/timeline/native_word_anchor.py`, `astrid/sdk/timeline_intent.py`, and `tests/sdk/test_timing_compiler.py`. No other source/test blob was forwarded.
- Uncommitted five-file binary patch SHA-256: `046787db15ba571bb8aae34d3d927f4e548940928574710ac930eb916cacdc98`.

The one-to-one conversion is retained exactly: ordinary `beats` and genuine
`downbeats` remain positive in Main and native timing; the invented
bars-only native positive is converted to the existing Main refusal, with the
native alias removed and both paths refusing. Existing malformed/empty carrier,
source speed/window, placed-audio ownership, replay-guard, and transcript
correction assertions remain. Current non-legacy blobs remain byte-for-byte
preserved. No marker authority, schema, client, pin, endpoint, or activation
was added.

Evidence is reused from the exact approved blobs: the 49-case compiler lane
and the prior 9 + 2 focused lanes, plus the approved direct Main/native
downbeat and bars-only probe. No new join was needed, so no compact product
lane was rerun; no full, HTTP, native, renderer, browser, body, or live-socket
suite was run.
