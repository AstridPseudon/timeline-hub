# Scanner 1.0.8 repair — HELD

Prepared a new immutable delivery from the exact rejected 1.0.7 archive and its four matching flat members. No repository product files changed; no git mutation, install, listener, browser, render, full Agent suite, network call, or owner-data run was performed. All 40 original scanner cases are preserved, with their test file byte-for-byte as the prefix of the new file. Added 84 regression cases; none skipped, weakened, or marked expected-to-fail.

## Delivery

- Archive: [handoff-vw-m4-scanner108-codec-repair-1.0.8.tgz](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner108-codec-repair-1.0.8.tgz)
- Exact bytes: **18,116**
- SHA-256: `e87e88705679e320bc83b6c72dff31fe23bbd0122981f314b5890411d6449cfb`
- [SHA sidecar](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner108-codec-repair-1.0.8.tgz.sha256), [metadata/member hashes](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner108-codec-repair-1.0.8-metadata.json)
- Four flat members: [scanner](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner108-codec-repair-1.0.8-scanner.py), [tests](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner108-codec-repair-1.0.8-tests.py), [conftest](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner108-codec-repair-1.0.8-conftest.py), [README](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner108-codec-repair-1.0.8-README.md)

Archive contains exactly four regular files: `README.md`, `owner_film_cliplook_scan.py`, `tests/conftest.py`, `tests/test_owner_film_cliplook_scan.py`. USTAR paths sorted; mode 0644; uid/gid/mtime zero; owner names empty; gzip filename empty and mtime zero. Two independent archive builds were byte-equal, and rebuilding after extraction remained equal. Every extracted member matches both its flat file and metadata hash. The existing 1.0.7 archive and four flat member hashes were rechecked unchanged.

The new metadata's `source_archive` and `source_sha256` identify this exact 1.0.8 archive, and match its `archives.tgz` entry. Historical 1.0.7 provenance is separate under `based_on`; 1.0.7 metadata was not modified.

## Repair and policy decisions

- Enumerate Agent `FieldSpec.stored_at` and `stored_at_audio`, checking each present declaration with its Agent Draft-07 schema and `FieldSpec.to_stored`. No copied numeric bounds, animation catalog, whole-document schema, or new projector. The one `project_runtime_parent_composition` call is regression-tested.
- Check original authored values before projection so an occurrence transform cannot hide malformed stored data. Retain only authored source paths in bounded errors, without authored values, exception text, or reference IDs. Keep affected findings/inventory unknown. Non-object audio params point to the openable `.params` container. Unreadable speed retains an unknown single-clip finding with an empty range and does not invent overlap timing; a refused closure has no findings.
- Shared entrance/exit paths use the general animation spec, preserving non-fade animations. Null clears and open extension/animation params are preserved. Volume is checked as a declared field without widening the scanner's look-category inventory.
- Unknown string curve IDs retain the existing complete/unknown policy; non-string curve shapes make the scan incomplete. This distinction preserves all 40 existing tests and follows the codec-matrix recommendation. Incoming transition mappings retain their existing free-form ID/type allowance rather than being routed through a closed catalog codec.
- Consumed the independent read-only [codec matrix report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner-codec-matrix-REPORT.md) and JSON matrix. Its seam recommendations agree with the repair. This is coordination, not policy approval.

## Exact tests and results

All scanner commands used Agent root `/home/user/work/wt/vw-m4-scanner108-codec-repair`, HEAD `86405964ecb713ad42a375f9de7960b3f9dc259b`. The extracted scanner suite is the requested delivery target, not a full Agent-suite claim.

Original exact 1.0.7 source and original 40 cases, before appending regressions:

```sh
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/package
/home/user/work/venv-agent/bin/python -I -B -m pytest -p no:cacheprovider --basetemp ../pytest-baseline --agent-root /home/user/work/wt/vw-m4-scanner108-codec-repair -q tests
```

**40 passed in 5.55s**, exit 0. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/baseline.log).

Final 124-case suite with the untouched exact 1.0.7 scanner in a separate private directory:

```sh
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/red-package
/home/user/work/venv-agent/bin/python -I -B -m pytest -p no:cacheprovider --basetemp ../pytest-red-final --agent-root /home/user/work/wt/vw-m4-scanner108-codec-repair -q tests
```

**68 failed, 56 passed in 6.73s**, exit 1, expected red-before. Failures include rejected entrance strings/lists, numeric booleans, audio duration strings/lists/objects/booleans at both directions and all authored source layouts, malformed curves/params, and the single-codec/placement regressions. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/red-final.log).

Final repaired private package:

```sh
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/package
/home/user/work/venv-agent/bin/python -I -B -m pytest -p no:cacheprovider --basetemp ../pytest-final --agent-root /home/user/work/wt/vw-m4-scanner108-codec-repair -q tests
```

**124 passed in 6.13s**, exit 0. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/green-final.log).

Freshly extracted exact 1.0.8 archive, four members byte-compared against flat files before execution:

```sh
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/extracted-1.0.8
/home/user/work/venv-agent/bin/python -I -B -m pytest -p no:cacheprovider --basetemp ../pytest-extracted --agent-root /home/user/work/wt/vw-m4-scanner108-codec-repair -q tests
```

**124 passed in 5.93s**, exit 0. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/extracted-tests.log).

Agent's neighboring existing codec suite:

```sh
cd /home/user/work/wt/vw-m4-scanner108-codec-repair
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m4-scanner108-codec-repair /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider --basetemp /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/pytest-codec -q tests/core/timeline/test_clip_fields.py
```

**102 passed in 0.38s**, exit 0. [Log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/agent-codec-tests.log).

Explicit lint scope with the repository's selected rules (the normal repository include globs exclude private delivery files):

```sh
/home/user/work/venv-agent/bin/ruff check --no-cache --isolated --target-version py311 --select E4,E7,E9,F,I,BLE /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/package
```

**All checks passed**, exit 0. `git status --short` empty and `git diff --check` passed. Worktree bytecode caches and private pytest temp directories removed after verification. Shared dependencies were not installed or altered by any explicit operation.

Reproduction builder: [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/build_archive.py](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/build_archive.py). [Archive verification](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner108-codec-repair/archive-verification.log).

## Remaining review

Implementation and packaging are complete; no worker blocker. **HELD pending independent review and Agent canonical-policy review of these exact bytes.** No owner-film closure supplied; no owner-film, macOS, full Agent-suite, playback, or render claim. Recommended next step: independent reviewer reruns this archive's 124 cases and checks bounded errors/source paths, then Agent reviews policy before release/ZIP adoption.
