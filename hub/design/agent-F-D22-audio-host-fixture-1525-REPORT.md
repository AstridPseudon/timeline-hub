# Agent F-D22 audio host fixture report

The two audio compile-contract positives now pass through the existing authenticated normal-audio producer. The test fixture verifies managed WAV bytes and SHA-256 registry identity, uses the real invocation asset server, requires the generated `render_source.file` to be under the attempt directory and server base URL, and reads back the produced RIFF bytes over that URL. No mock source, evaluator, renderer, or API was added.

Evidence: central targeted service **PASS**, 39 passed in 15.97s; scoped Ruff **PASS**; scoped mypy **PASS**; `git diff --check` **PASS**. Readonly production source hashes match `HEAD`: `normal_audio.py` `00e46437f1199488260fa6b3409297eddbb2b827ec7a1d0be1b6fff3fbf2b74a`, `root_preparation.py` `71e38ad87d9dd52a9f18a58b2c6122fa87a49d5b2fcc1b07e575f8400c61a61b`. Full suite was not run.
