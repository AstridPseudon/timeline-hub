## Result

Supported route confirmed: ordinary `pip download` can prepare the wheelhouse input.

Source facts:

- Runtime base: `33fc06bbd5b0a778517ac6f7c161b2a556ab80c4`
- Agent source: `bb50a43c915ec00c05c5ee34569a040bab8e817c`
- `requirements/proof.lock` SHA-256: `236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778`
- Verifier SHA-256: `8f95cdaee258b87dde8e859e99fb955e9cde91dfeec9e7191f4837a5ced6714f`

Packet:

1. Derive the lock exactly as the maker does:

```bash
git -C /home/user/peteromallet/astrid-agent \
  show bb50a43c915ec00c05c5ee34569a040bab8e817c:requirements/proof.lock |
grep -v -e '^astrid @' -e '^pip==' -e '^setuptools==' -e '^wheel==' \
> /absolute/worker-owned/proof.lock.filtered
```

2. Using the same compatible maker interpreter/platform (`CHILD_VENV_PYTHON`, default `python3.13`) and a private physical worker-owned destination:

```bash
python3.13 -m pip download \
  --require-hashes \
  --no-deps \
  --only-binary=:all: \
  --no-cache-dir \
  --disable-pip-version-check \
  --progress-bar off \
  --dest /absolute/worker-owned/child-wheelhouse \
  --requirement /absolute/worker-owned/proof.lock.filtered
```

The verifier remains authoritative for marker selection, compatible tags, exact versions, listed SHA-256 hashes, one wheel per active package, archive identity, and installed-byte/RECORD checks. Bootstrap `pip`, `setuptools`, and `wheel` remains separate. `.data` relocation layouts, sdists, extra files, symlinks, duplicate wheels, and missing compatible wheels are explicit refusals.

The stated Agent checkout path was unavailable, so I used the exact committed file via read-only `git show`; no substitute checkout was used.

Checks:

- `python3 -m pip download --help`: passed; required options documented.
- Source/hash checks: passed.
- Product tests: not run; task explicitly required source-only assessment.
- No download, network, cache inspection, provisioning, or environment/credential output performed.
- Worktree remains clean. Completion marker and commit message were written as required.