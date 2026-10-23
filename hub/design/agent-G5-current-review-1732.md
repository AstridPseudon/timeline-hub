# Agent G5 current-port preservation review

Date: 2026-10-23

## Exact verdict

**PASS — bounded current G5 DRAFT preservation review; P1 remains NO-GO and
the draft must not be merged or activated.**

Reviewed commit `bda966e9c491e1fa4b683cda8913dddeaa14c63d` on
`tl/agt-G5-current-port-1725`, whose sole parent is the current integration
base `6531622c8f198c3efb509217e303fcad0126c47b`. This is a mechanical
preservation ACK only. It does not approve G5 activation, the original SDK
FOUR/public redo qualification, P1/P4, a merge request, a pin, or any
whole-suite claim.

## Source path map and preservation

- `git diff --name-only 6531622c8..bda966e9c` contains exactly 47 paths.
- `git diff --name-only bac094180..dc5c84b9a` contains exactly the same 47
  paths; the sets are equal.
- Every one of those 47 current final blobs equals the corresponding donor
  final blob at `dc5c84b9a`. There are zero final-blob mismatches.
- The donor source is the reviewed `bac094180..dc5c84b9a` port (the reviewed
  `9da584010` current fixture plus the `dc5c84b9a` authentic Runtime fixture).
  The authentic fixture path is already included in the 47-path set; no extra
  path was added.
- All paths outside that set are base-identical. In particular, the current
  inverse work (`ccbb528dc`), R1 private/atomic/source-history work, validation,
  the `4faad4bcb` F-D22 fixture, and the remaining F-D22 files are unchanged
  from `6531622c8`. Explicit protected checks passed for:
  `inverse.py`, `_commit_patch.py`, `_commit_preview.py`, `_root_inverse.py`,
  `_step_undo.py`, `commit.py`, `_commit_timing_validation.py`, and
  `validation.py`.
- There is no unreviewed merge ancestry: the reviewed commit is one child of
  the exact current base.

## Retirement and caller audit

The production scan found no active `--commands-file`, `commands_file`,
`publish_bundle`, `three_way`, `document_diff.py`, `separate-publish`,
`separate_publish`, `separatepublish`, or legacy `--publication` route. The
legacy `publish` CLI command is absent.

The remaining write callers use the existing commit boundary: detached
document commits call `Timeline.commit`; ordinary move/trim/sheet paths call
`TimelineSession.commit`; and the document/restructure paths use
`emit_document_commands` followed by `TimelineSession.submit`. The retained
SDK `Checkout.publish` name is a façade over that normal emitter/session path,
not a separate publication writer. Accepted inverse is the required canonical
`TimelineSession.undo` path, not the retired CLI `undo --publication` route.
The only live `--native` parser is `show --native --as sheet`, a read-only
sheet projection; there is no `apply --native` or native write parser.
No alternate film executor was found in the active timeline write paths.

No C0 contract, schema, generated client, or pin path is among the 47 changed
paths. The existing request/reply carrier and the production caller remain the
full C0 path; this review made no wire-shape change.

## Fixture and test preservation

The four authentic SDK test functions retain identical AST bodies and
decorators across `9da584010`, `dc5c84b9a`, and the reviewed current tree:

- `test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore`
- `test_checkout_reload_undo_cli_redo_uses_retained_history`
- `test_open_bundle_keeps_http_rows_raw_and_round_trips_canonical_images`
- `test_retained_restore_does_not_reopen_consumed_draft_steps`

The fixture retains the real archive SHA
`2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3` and the
catalog Runtime source pin `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`. No
fake authority, global pytest plugin, test deselection, skip, xfail, or
assertion weakening was introduced. The module uses its existing integration
fixtures and has no `pytest_plugins` injection.

## Evidence

Reused the author’s evidence after proving the reviewed tree and donor blobs
are identical:

```text
184 tests collected
184 passed in 50.01s
```

The scoped checks run on this review tree were:

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/reshape/compare_ruff_baseline.py
=> Ruff findings: current=2148 baseline=2148

PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-03eb258414/g5-mypy-cache \
  /home/user/work/venv-agent-typecheck-v2/bin/python \
  scripts/reshape/compare_mypy_baseline.py
=> Mypy findings: current=1911 baseline=1911

PYTHONPATH=. /home/user/work/venv-agent/bin/python \
  scripts/vendor_lock.py check runtime.lock.json \
  --producer /home/user/work/wt/rt-pin-34eac004
=> ok runtime.lock.json (matches producer manifest)

PYTHONPATH=. /home/user/work/venv-agent/bin/python \
  scripts/artifact_manifest.py --check
=> artifacts.json is current

git diff --check
=> PASS
```

The initial shared `venv-agent` mypy attempt was environment-incompatible
(missing YAML stubs and Python-3.13 NumPy syntax); it was not counted as a
pass. The prescribed private typecheck environment produced the passing
`1911 = 1911` result above. The review worktree has no tracked or untracked
source changes.

## Limits and next steps

No original SDK FOUR/public redo, C271, P1/P4, full suite, browser, live
socket, or native/browser-body run was performed. The 184-test result is
reused only because the current tree was verified byte-for-byte against the
author-qualified donor tree. The authentic archive remains an external test
input. Keep the DRAFT/P1-NO-GO boundary and request a separately authorized
meaningful public qualification before any merge or activation decision.
