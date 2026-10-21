# D13 current final source review

## Verdict

**REQUEST CHANGES.** The final source fixes the concrete defects from
`agt-review-d13-current-port-custody-parity`, but the exact source does not
pass its real installed-positive control, so selected installed staging must
not use it yet.

Reviewed final `HEAD` `d803c7c48aee2abe477c9277572d1d17b2cb41c0`, tree
`1df439979bd1b18794aec68612bf6790689e6f0f`.

This is bounded to the existing coherent immutable installed-set/controller
trust contract. It makes no pre-entry active-tamper claim and does not claim
native, live Runtime, renderer, full-suite, or 688-replay proof.

## Prior REQUEST CHANGES resolved

- `astrid/sdk/host_bootstrap.py:715` probes exactly the eight required origins:
  `host`, `child`, `action`, `client`, `sdk`, `runtime_protocol`,
  `runtime_protocol.platform`, and `astrid_runtime`.
- `host_bootstrap.py:755-757` now requires exactly that same eight-key set.
  The final validator and `tests/sdk/test_host_bootstrap_source_identity.py`
  are byte-identical to donor `c2ba60bebc5edeff80c5cfbcf0e8e16b70e69bf4`.
- The donor AST/no-import assertions and the ambient Runtime negative are
  present, including `test_installed_profile_does_not_use_ambient_runtime_checkout`
  at `tests/sdk/test_host_bootstrap_source_identity.py:479-503`.
- `astrid/packs/rendering/pack.yaml:52-54,87` now accurately says legacy
  admissions are refused before execution; the stale Runtime-publication
  wording is gone.

## Remaining concrete blocker

The real private installed-pair control fails before a valid positive origin
result. `tests/sdk/test_installed_runtime_source_identity.py::test_exact_installed_pair_passes_real_origin_and_child_checks`
and the four `test_runtime_substitution_after_real_probe_fenced_at_child_import`
cases fail because the isolated probe exits with:

```text
KeyError: 'astrid.packs'
```

The traceback is from `PathFinder.find_spec(name, search)` at
`host_bootstrap.py:722`, when resolving a dotted parent such as
`astrid.packs` without importing product packages. The probe's no-product-
imports strategy therefore cannot successfully validate an otherwise coherent
copied Agent/Runtime/client installation. This is a source defect, not a
native/socket capability limitation.

Required correction: keep the no-import boundary, but resolve dotted modules
using explicit parent search paths and leaf names (or an equivalent
non-importing resolver) so a clean installed set succeeds. Retain the exact
eight-origin checks and add/keep a real positive installed-pair regression
showing the probe emits all eight origins before the negative substitution
cases run.

## Preservation review

The final tree is current integration `2aa1233d207b558fbc08a5d2b3dc3c605d922b10`
plus the current integration preservation commit and the D13 port. The only
changes from the preservation parent `db6b8dc5868364cfa183b59cd627f711d1fda5cd`
to the final are the fourteen intended D13 paths; the unrelated current
changes in `_remote_timeline.py`, `docs/architecture/timeline.md`, and
`tests/sdk/test_authoring_revision_diff.py` are preserved byte-for-byte.
No worktree product files were edited by this review.

## Evidence

Passed compact controls:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_strips_source_pythonpath_and_probes_selected_interpreter \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_refuses_checkout_origins_from_isolated_probe \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_does_not_use_ambient_runtime_checkout \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_origin_probe_resolves_without_product_imports \
  tests/sdk/test_host_bootstrap_source_identity.py::test_python_source_loader_can_read_cache_before_bytecode_write_policy \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_legacy_assembler_admission_refuses_before_execution_and_keeps_artifacts
7 passed in 1.35s
```

The exact run included the selected-interpreter/PYTHONPATH guard, checkout
origin refusal, ambient Runtime negative, no-import AST assertion, loader AST
assertion, isolated launch identity, and legacy refusal/artifact preservation.

The real installed-control run was:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_strips_source_pythonpath_and_probes_selected_interpreter \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_refuses_checkout_origins_from_isolated_probe \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_does_not_use_ambient_runtime_checkout \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_origin_probe_resolves_without_product_imports \
  tests/sdk/test_host_bootstrap_source_identity.py::test_python_source_loader_can_read_cache_before_bytecode_write_policy \
  tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter \
  tests/sdk/test_installed_runtime_source_identity.py \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_legacy_assembler_admission_refuses_before_execution_and_keeps_artifacts
13 passed, 5 failed in 7.13s
```

The five failures are the positive/substitution cases listed above; missing-
Runtime and symlink refusals passed. `git diff --check 2aa1233d2 HEAD`, AST
parsing of all 14 changed Python files, exact donor parity, exact current
unrelated-file preservation, and the probe/validator eight-key/metadata
checks all passed.

No native/full/688 replay was run. After the probe fix, rerun only the compact
installed-origin controls on the exact resulting tree; native proof remains
unobserved.
