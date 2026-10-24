## Result

Read-only investigation complete; no source files changed.

### Source chain and failure owner

- Requester: `scratchpad/orch/bin/request-child-venv:12-78,249-255`
- Store lifecycle: `scratchpad/orch/bin/bench_store.py:636-715`
- Child build/verify: `scratchpad/orch/bin/make-child-venv:301-315,375-396`
- Relocation metadata updates: `make-child-venv:540-558`
- Installed dependency verifier owner: `scratchpad/orch/bin/verify_dependency_seed.py:178-244`

The candidate `agent=0c2c28da...`, `runtime=becfe6db...` completed installation, provenance, shebang/origin/path relocation, and readonly-source checks, then failed only at:

`verify_dependency_seed.py:209-211`

```text
unsafe or overlapping dependency RECORD: numpy
```

The failed candidate’s installed tree and staging directory are absent.

### Accepted transformations

The verifier accepts:

- Exact package name/version and one physical `site-packages`.
- Original wheel files with matching bytes and RECORD hashes.
- Unhashed self-`RECORD`.
- Valid generated `.pyc` files under `__pycache__`.
- Same-dist `INSTALLER`/`REQUESTED`.
- Ordinary RECORD hash/size recomputation.

It refuses:

- Duplicate or cross-distribution-overlapping RECORD paths.
- Absolute paths, backslashes, traversal, symlink-resolving paths, or paths escaping the root.
- `.data` wheel layouts.
- Unowned extra files, missing original wheel rows, malformed records, ambiguous layouts, or wrong versions.

### Hypothesis

The retained NumPy 2.5.2 wheel is valid: 926 RECORD rows, no duplicate archive members, no `.data` members, and declared console scripts `f2py` and `numpy-config`.

Static analysis indicates the likely benign culprit is a pip-generated console-script RECORD row such as:

```text
../../../bin/f2py
../../../bin/numpy-config
```

Those rows are legitimate pip installation output but fail `path.resolve() != path` at the verifier’s safety predicate. This remains a hypothesis: no installed NumPy RECORD rows are available to confirm it.

If the actual failing row is instead under `numpy/` or `numpy-2.5.2.dist-info/`, the cause could be duplicate ownership, overlap, symlink/path corruption, or another real integrity failure.

### Evidence comparison

- Source-only wheel proof validates archive metadata, RECORD structure, hashes, tags, and traversal safety. It cannot observe pip-generated console scripts.
- Existing strict installed synthetic tests pass traversal, overlap, symlink, mutation, and ownership negatives. They prove the guard works, but do not establish that console-script RECORD traversal is an intended legitimate transformation.
- No guard waiver, retry, reconstruction, install, or verifier patch was performed.

### Missing finite evidence request

Please provide one immutable read-only export from the preserved failed child:

1. Raw `numpy-2.5.2.dist-info/RECORD`.
2. Ordered `owned` path set immediately before NumPy verification.
3. For any rows outside `site-packages`—especially `f2py` and `numpy-config`—the lexical path, resolved target, lstat type, SHA-256/size, and whether it matches a wheel member.

That single export distinguishes benign console-script RECORD entries from overlap, traversal, symlink, or byte corruption.

### Checks

- Retained-wheel stdlib metadata/RECORD audit: PASS.
- Static predicate demonstration for normal paths, console-script traversal, and escape traversal: PASS.
- `git diff --check`: PASS.
- `git status --short`: clean.
- No full/browser/live or candidate-install tests run, per task constraints.

Required commit message and `DONE` marker were written.