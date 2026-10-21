# Agent current-owner review: legacy beat preservation

Reviewed source commit `60d95d69f81ccff1a113c5aec66b6be6d6bee876` and the
source worker report against Main `model._MomentContext.beats` and
`core.timeline.moments.Context.beats`.

The source change had three concrete gaps. Its pure resolver admitted parent
and visual beat carriers although Main's context only iterates audio clips in
placed occurrences; its native replay guards omitted placement geometry,
`hold`/`duration`, clip track and track kind; and captured transcript word
window filtering used timeline duration as source duration, which loses source
words after the first source-duration/speed interval. These are now corrected
in the worker tree. The resolver still uses the existing numeric
`app.astrid.beats`/`downbeats`/`bars` carriers and existing timing Context; no
generic marker publication, new DTO, selector, pin, or endpoint was added.

The added checks cover bool/null carrier entries, changed carrier timing and
placement/track inputs, unchanged neighbor behavior, and representative
Main-`Checkout` versus native compiler parity on
`tests/fixtures/timeline_editing/tiny_publishable.json`.

Evidence:

- `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timing_compiler.py tests/sdk/test_timing_cycles.py` — **57 passed**.
- The beat/native plus checkout focused lane — **9 passed, 142 deselected**.
- `ruff check astrid/sdk/timeline/_timing_evaluators.py astrid/sdk/timeline/native_word_anchor.py tests/sdk/test_timing_compiler.py` — **passed**.
- `git diff --check` — **passed**.

No full, HTTP, renderer, browser, install, schema/pin, or cross-product suite
was run. A broader Ruff command including untouched `astrid/sdk/timeline_intent.py`
reports its pre-existing compressed-style E701/E702 findings; the focused
touched-file check is clean.
