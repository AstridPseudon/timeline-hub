# D33 whole-path validation

Status: `UNQUALIFIED`, read-only inventory only. No source, wrapper, fixture,
Store, installation, service row, or test assertion was changed. No service was
submitted or retried.

## Actual 1810 boundary

The durable 1810 wrapper passed its numeric preflight and the ordinary service
ran once under `env -i` with an empty log. The service exited `1` at the first
guard, `test -x "$RUNTIME_PYTHON"`, because
`/home/user/work/venv-runtime/bin/python` is absent. The wrapper therefore did
not reach the source archive, `--write-inputs`, wheel build, fixture Git
commits, `Store.initialize`/`--prepare-venue`, parent maker, candidate maker,
sealed verifier, or adversarial checks. The 1810 evidence records all bodies as
zero/`NOTRUN`; there was no safety, permission, or classifier refusal.

## Static and local checks

Commands run directly and results:

```text
bash -n <1810 durable inventory_whole_maker.sh>                         PASS
exact Avail parser: valid header/data + missing/noninteger/multiple/negative PASS
Python 3.13.16 venv-agent isolated imports (stdlib, build, setuptools, wheel) PASS
Python 3.13.16 system isolated stdlib imports                          PASS
JSON parse of source/evidence manifests (6 files)                      PASS
AST parse of current maker/e2e/support and source1747 e2e/support         PASS
sha256 source/helper/maker/artifact/bootstrap wheels                    PASS
tar -tzf bootstrap artifact                                              PASS
parent STORE_VERIFY == candidate STORE_VERIFY                            PASS
git cat-file source commit/files                                         PASS
```

`/home/user/work/venv-agent/bin/python` and `/usr/bin/python3.13` are both
present, mode `755`, Python `3.13.16`, and byte-identical. Only the Agent venv
has the required `build` module (`1.4.0`); the system interpreter lacks it, so
the Agent venv is the minimal valid `RUNTIME_PYTHON` binding for the wrapper's
write-input/build-wheels/prepare route. The child Python binding
`/usr/bin/python3.13` is present and valid.

The current free-space observation was `6,702,477,312` bytes, above the exact
unchanged `5,905,580,032`-byte reserve and `4,000,000,000`-byte stop line.

## Whole-path inventory

The wrapper's absolute inputs are the protected helper, bootstrap artifact,
Agent build/runtime Python, `/usr/bin/python3.13`, the source commit object and
the worker evidence path. Its relative input is `$PWD`, used as the Git source
repository for `git cat-file`, `git archive`, and the candidate maker hash.
All source and wheel hashes match the 1747/1810 controls. The source1747 tiny
layout is recorded in `source-manifest.json`; the exact source manifest and
wheel hashes are recorded in `prerequisites.json`.

The service PATH resolves the shell tools to `/usr/bin` (with `python3` resolving
to `/usr/bin/python3.13`); `echo` is a shell builtin. The e2e runner invokes
`git`, `bash`, and the configured Python; the unchanged maker additionally
requires its PATH tools (`git`, `tar`, `mktemp`, `sha256sum`, `cut`, `grep`,
`sed`, `find`, `chmod`, `mv`, `df`, `awk`, `timeout`, `python3`).

## Further portability defects after the first failure

1. The wrapper binds the absent runtime venv. Bind `RUNTIME_PYTHON` to the
   existing qualified Agent Python, or pass an equivalent validated absolute
   path. Do not use the system Python for the whole wrapper because it lacks
   `build` for the offline dependency-wheel phase.
2. The wrapper's archive-only source root is not executable as the source1747
   runner: it omits `ops-child-custody/make-child-venv`, while `support.py`
   resolves that sibling from `__file__`. Independently, the runner's parent
   comparison calls `git show` with `cwd=MAKER.parents[1]`; a tar extraction
   root has no `.git`. The minimal wrapper binding is a real temporary Git
   checkout/worktree at the exact source commit, preserving the expected maker
   sibling and Git object database. Adding only the maker file to the archive
   does not repair the second defect.

The hard-coded `support.ORCH` constant is not used by this e2e runner path;
the active runner passes the prepared helper explicitly. It remains a latent
portability hazard for any support helper path that uses that constant, but is
not a further first-pass body failure.

## Evidence limits and next step

No fixture Git/Store/maker/verifier body was exercised in this audit, and no
full suite or source-unit repeat was run. The wrapper author should repair the
two bindings above, then obtain one fresh admitted ordinary service run. The
source/E2E result remains unqualified until parent-RED, candidate-GREEN, sealed
registration, and unchanged adversarial checks pass in that run.

## Final independent binding and one authorized service

The exact corrected wrapper was independently rechecked without modification:

- wrapper SHA256 `564716bca87c9b48251ceecb3b6455bea40147e94cae9b5e25d98dee9747fa3f`;
- suite row SHA256 `fcfd280bb6441a462707e645743187efec6a6ff95d83528903579bac67b0fd8f`;
- source1747 `f6b9d4d52802d3cc5cd6bf9be070cd4c40d1e2fe`, runner and manifest hashes exact;
- candidate maker `c3226b`, parent maker `0857a5`, support import and Git parent lookup exact;
- Agent/build Python, child Python, setuptools `80.9.0`, wheel `0.46.3`, offline wheel hashes,
  source modes, numeric disk guard, fresh physical TMPDIR, default-off network and no mocked
  verifier/installer all passed.

The manager-authorized service was submitted once and only once. It reached the genuine
fixture path and produced the first authentic result, but exited `2` at the parent maker
inventory-refusal assertion. The result is intentionally not promoted to GREEN: parent RED,
candidate GREEN, sealed verification, registration, and adversarial checks are all false or
unreached in `e2e-result.json`. This is not a safety, classifier, or permission refusal.
No retry was submitted.
