# PASS_SOURCE

Reviewed candidate commit `9428f515fcd8dccaef26193438b3ac89f903f5aa`, tree
`7952f3e9e155320720664ea9d151fe79114bd6`, and maker SHA-256
`0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`.

The live maker preimage is SHA-256 `1243cb6c203b7f9c23015f2fc0e3fe4722eb53c1c703f171b89123cf9c8afd0b`.
The candidate differs only in `STORE_BUILD`: it always creates authenticated
`.source-inputs/{agent,runtime}.tar` carriers and installs those archives in
both seeded and unseeded branches. `STORE_PY` and `STORE_VERIFY` are byte-exact
with the live preimage. No metadata allowlist, RECORD grant, ignored foreign
path, symlink/hardlink/hash/mode/owner bypass, trust change, or public protocol
change was found.

The real shell producer branch was exercised with exact-argument Git and
installer doubles. The installer double intentionally models build/lib and
egg-info writes without invoking pip or building a real package; the unchanged
embedded verifier then accepts the archive candidate and refuses the parent
directory-install control. The modeled refusal census is exhaustive for its
fixture and reports 10 extra paths. Seeded archive routing remains covered.

Acceptance evidence:

```text
bash -n ops-child-custody/make-child-venv                         PASS
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v
                                                                   PASS (29 tests)
/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests
                                                                   PASS
git diff --check                                                   PASS
```

The unittest run also compiles all seven embedded Python blocks in memory.
There is no configured Python mypy/pyright baseline in Composition, and no
product TypeScript changed, so typecheck is N/A. The first test attempt used
the harness-provided `tmpdir` path, which is a regular file; it failed before
fixture creation with `NotADirectoryError`. The same exact suite passed after
selecting a private `/tmp` fixture directory, with no source changes.

The independent `rt-Agent-D128-custody-wholepath-1637` report was read. It
attributes the original no-seed failure to setuptools `egg_info` generation,
but the actual retained offending path is `EXACTMISSING`. Main diagnostic and
live child/build/install/acquisition were not run here. Therefore this is a
source verdict only; actual retained-layout rows, STORE_VERIFY acceptance in a
real child, registration/adoption/reuse/publication/READY, and full/core/body
acceptance remain unverified.

Protected live hashes for the maker, `bench_store.py`, and
`verify_dependency_seed.py` remained unchanged. The exact pinned Agent and
Runtime source trees were clean, with 3565/694 and 535/33 committed
file/directory counts respectively and no unsupported Git entries. D131
reserves remain 5905580032 normal-child bytes and 8589934592 runtime/
diagnostic bytes.

