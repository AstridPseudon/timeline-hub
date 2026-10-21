# Agent Gate7 typecheck environment recipe

Date: 2026-10-21 UTC

## Disposition

**DESIGN ONLY / NOT QUALIFIED.** This report records a private environment
recipe and local inventory. No package was installed, no network was used, no
mypy run was started, and no Agent source, ignore, stub, target, or baseline
file was changed.

The requested input
`design/agent-gate7-typecheck-environment-recipe.md` is absent from this
worktree, `docs/design/`, and the shared ORCH design directory at the time of
inspection. The available authoritative nearby notes were
`agent-current-check-gate.md`, `agent-baseline.md`, and the settled PLAN. This
file is the requested shared design report, and does not change the settled
decision.

## Local interpreter

The usable local Python 3.11 executable is:

```text
/usr/bin/python3.11
CPython 3.11.17
pip 24.0 (system installation)
ensurepip and venv modules available
```

The shared Agent environment is Python 3.13.16, so it is not evidence for the
Python 3.11 Gate7 run.

## Existing 164-entry inventory and NumPy branch

The exact existing 164-entry child inventory is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/provision/venv-agent-child-s2.txt
sha256 478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761
164 lines / 164 package entries
```

It is a Python 3.13 child freeze, not a Python 3.11 lock: the provisioning
helper creates it with `python3.13`, and its line 78 is the unconditional
`numpy==2.5.2`. It also carries `PyYAML==6.0.3` (line 125) and
`mypy==1.17.0` (line 76). Its `astrid @ file:///home/user/work/wt/.orch-astrid-d8749a9c`
source path is absent now, so it must not be used as an install source or
current Agent identity.

The repository’s existing universal runtime/proof locks select the precise
Python branch needed for Gate7:

```text
requirements/runtime.lock:596
numpy==2.4.6 ; python_full_version < '3.12'

requirements/runtime.lock:669
numpy==2.5.2 ; python_full_version >= '3.12'
```

Therefore Python 3.11 must use NumPy **2.4.6**, with the hashes already listed
under the first branch at `requirements/runtime.lock:597-668` (the same branch
is in `requirements/proof.lock:600-671`). Do not carry the 164-freeze’s
2.5.2 value into the Python 3.11 environment. No local NumPy 2.4.6 wheel or
cached wheel body was found, so the branch is declared by the repository lock
but is not locally materialized here.

## `types-PyYAML` inventory

No `types-PyYAML` wheel is present in the local wheel files or pip cache, and
no installed `types-PyYAML` distribution is present in either shared Agent
environment inspected. The repository’s `pyproject.toml`, runtime lock, proof
lock, and 164-entry inventory also declare no `types-PyYAML` entry. The only
local/locked YAML package is `PyYAML==6.0.3`; it is runtime code, not typing
stubs.

Consequently the cached `types-PyYAML` version and SHA-256 are **absent**. No
version or hash is invented here. A later owner must supply one exact local
wheel and record its filename and SHA-256 in the private environment
provenance, or make an explicit dependency decision. This task does not edit
the project declaration or lock files to add it.

## mypy 1.17 closure and declared dev tools

`pyproject.toml:49` declares `mypy==1.17.0`. Its package metadata requires:

```text
mypy==1.17.0
typing_extensions>=4.6.0  -> existing exact 4.16.0
mypy_extensions>=1.0.0   -> existing exact 1.1.0
pathspec>=0.9.0          -> existing exact 1.1.1
tomli>=1.1.0 only when Python < 3.11 -> not required on 3.11
```

Thus the exact mypy closure for Python 3.11 is the four-package set
`mypy==1.17.0`, `mypy_extensions==1.1.0`, `pathspec==1.1.1`, and
`typing_extensions==4.16.0`. The last package is already selected by the
runtime lock at `requirements/runtime.lock:1196`; the other two closure
packages are present in the 164 inventory at lines 77 and 91.

The declared dev tool pins needed by the normal CI install are unchanged:

```text
pytest==9.0.2
pytest-cov==7.1.0
pytest-split==0.11.0
pytest-timeout>=2.4       (164 freeze resolves 2.4.0)
ruff==0.12.0
build==1.4.0
setuptools==80.9.0
wheel==0.46.3
```

The 164-entry closure also contains the normal transitive test/build pieces,
including `coverage==7.16.2`, `execnet==2.1.2`, `iniconfig==2.3.1`,
`pluggy==1.7.0`, `packaging==26.3`, `pyproject_hooks==1.2.0`, and the
Python-3.11-compatible `typing_extensions` above. It includes the declared
VCS dependencies `runpod-lifecycle` at commit
`db79345536985c701b7aff2eb5eec36667aae204` and the timeline schema at commit
`242f9c4306bf3b501222cb041a9eb246ef47bc85`.

The schema URL differs between the old 164 freeze (`banodoco/ArtAgents.git`)
and current `pyproject.toml:57` (`banodoco/astrid-agent.git`) despite the
same commit ID. Do not silently treat those URLs as interchangeable: the
current declaration is the authority for the later private setup.

## Concrete private recipe

Use a disposable private root, never `/home/user/work/venv-agent` or another
shared environment. The following is a recipe for the later environment;
the placeholder wheelhouse must be populated before execution:

```bash
PRIVATE_ROOT=/tmp/astrid-gate7-mypy-<frozen-agent-sha>
PY311=/usr/bin/python3.11

"$PY311" -m venv "$PRIVATE_ROOT/venv"
V="$PRIVATE_ROOT/venv/bin/python"

# Materialize the repository’s hashed runtime lock with the Python 3.11
# marker selecting NumPy 2.4.6. The wheelhouse is private and local.
"$V" -m pip install --no-index --require-hashes \
  --find-links "$PRIVATE_ROOT/wheelhouse" \
  -r requirements/runtime.lock

# Install the exact frozen current Agent source privately, without exposing a
# checkout through PYTHONPATH. The selected Agent source/wheel must be frozen
# by the manager before qualification.
"$V" -m pip install --no-index --no-deps \
  "$PRIVATE_ROOT/wheelhouse/astrid-<frozen-agent-version>.whl"

# Materialize the declared dev closure from private wheels, retaining the
# exact versions above and the exact VCS commits above. Include the one
# owner-supplied types-PyYAML wheel only after its version/hash is recorded;
# it is not a repository pin.
"$V" -m pip install --no-index --no-deps \
  "$PRIVATE_ROOT/wheelhouse"/*.whl

# This is the normal CI target and must remain unchanged.
PYTHONDONTWRITEBYTECODE=1 make PY="$V" mypy
```

The later setup should additionally run the normal CI’s pinned Runtime/client
installer (`scripts/ci_install_runtime.py`) from private local Runtime
artifacts for the frozen `runtime.lock.json` source commit
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`; the current script itself uses a
GitHub archive URL and therefore cannot satisfy this task’s no-network
constraint. The typecheck qualification command remains `make PY="$V" mypy`,
which invokes the existing `scripts/reshape/compare_mypy_baseline.py` and
does not change target, flags, or baseline.

## Missing prerequisites

All of the following must be supplied before a meaningful private Gate7 run:

1. A private Python 3.11 wheelhouse containing every selected
   `requirements/runtime.lock` artifact, especially NumPy 2.4.6 for the local
   Linux/CPython 3.11 platform. The shared Python 3.13 environment and its
   NumPy 2.5.2 install cannot substitute.
2. A frozen current Agent source/wheel matching the exact commit being
   qualified. The 164 freeze’s old `/home/user/work/wt/.orch-astrid-d8749a9c`
   path is missing and is not an authority.
3. Local source/wheels for the declared VCS dependencies at their exact
   commits: `runpod-lifecycle` at `db793455...` and the current declared
   `banodoco/astrid-agent` timeline schema at `242f9c...`.
4. One owner-authorized `types-PyYAML` wheel with an exact version and
   SHA-256. It is absent locally, absent from the repository declarations and
   locks, and cannot be named by this report.
5. Private Runtime and generated-client artifacts for the exact
   `runtime.lock.json` source commit if the environment is to mirror the
   normal CI setup; the checked-in installer is network-backed and was not
   run.
6. A provenance record tying together the Agent commit/tree, the selected
   Python executable, the 3.11 lock hash, every locally supplied wheel hash,
   the `types-PyYAML` hash once supplied, and the Runtime/client source
   identity. None of that should be written into shared installs.

Not prerequisites for this scoped typecheck recipe: a full pytest run, browser
or live-socket services, Remotion/Node, renderer parity, or a source/config
change. Those remain separate CI gates and were not run.

## Evidence run

Read-only checks performed:

```text
/usr/bin/python3.11 -V                         -> Python 3.11.17
wc -l venv-agent-child-s2.txt                  -> 164
sha256sum venv-agent-child-s2.txt              -> 478af081...034761
pip/cache/file searches for types-PyYAML wheels -> none found
git status --short                              -> clean
```

No mypy, pytest, full suite, install, source edit, baseline edit, network
request, or test-service request was made.
