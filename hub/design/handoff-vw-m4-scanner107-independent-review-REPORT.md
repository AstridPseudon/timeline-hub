# Scanner 1.0.7 independent review — APPROVE

2026-10-20. I read PLAN.md, COMMON.md, and the exact Agent rejection review design/agent-review-scanner-1.0.6.md. This was a read-only review; no repository files, artifacts, branches, refs, shared dependencies, or owner data were changed.

## Decision

APPROVE candidate artifact owner-film-viewing-tools-v1.0.7.tgz for the reviewed Agent policy requirements.

- Artifact: 15,630 bytes, SHA-256 baf2fd28f96670b02e4dc63e21bc680e2ab0339a97671515d79ab91f9cbd3e27.
- Current Agent root: /home/user/work/agent, clean tl/integration at 0e951d6891cc95e2cb7483497adb002cb9563a1a.
- Candidate archive and flat handoff files are byte-identical for all four members.
- No owner-film closure was available or used; no real-film or macOS claim is made.

## 1.0.6 to 1.0.7 review

The source diff is narrow. It changes the version, adds _unreadable_look_names() to probe the existing Agent clip_fields.describe codec one authored field at a time, and on an unreadable look emits only its bounded authored source path, marks the inventory/finding unknown, and makes the scan incomplete. Tests add four malformed look cases and extend the explicit-clear test with an opaque extension field. README coverage is updated accordingly.

Static inspection and a dynamic probe confirm:

- project_runtime_parent_composition is called exactly once per scan.
- It remains the only whole-document closure boundary. There is no second validator or semantic rewrite; audio_curves.validate is only field-level curve validation, and the other calls are existing public Agent codecs/helpers.
- Top-level imports contain no socket, HTTP, urllib, requests, media, credential, or network machinery.
- No old test function was removed. Exact 1.0.6 cases remain green (36 cases); 1.0.7 adds one parametrized test with four cases.

## Artifact and flat-file integrity

The private archive check read the tarball without trusting extraction. It found exactly four regular members: README.md, owner_film_cliplook_scan.py, tests/conftest.py, and tests/test_owner_film_cliplook_scan.py.

Each member matched the metadata byte count/hash and the corresponding flat handoff file. Extraction was performed only under the worker-owned folder; all members were checked for relative paths, regular-file type, and absence of symlinks before writing. No traversal or symlink member was present.

## Required behavior

- One projector: PASS — dynamic wrapper observed one projector call.
- IDs/path-only output: PASS — output contains bounded IDs, property names, source paths, pins and intervals; no authored raw values are emitted.
- Secret markers: PASS — synthetic opaque, credential, opaqueSecret, and raw markers are absent from output; malformed-value markers and exception text are also absent.
- Malformed describe failure: PASS — opacity, crop-left, entrance duration, and exit duration each produce status incomplete, clean_claim false, the exact bounded ... is unreadable error, and retained unknown media/overlap rows for the affected clip.
- Explicit clear and unknown fields: PASS — asset: None remains None; an unknown extensionData object survives Agent projection, while its opaque marker is not copied into scanner output; input JSON remains byte-stable.
- No clean claim: PASS — clean_claim remains false even for complete synthetic scans.

## Exact test commands and results

All commands used the shared Agent venv read-only, python -I -B, and disabled pytest cache writes. Extracted tests and private comparison copies lived under /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner107-independent-review/.

    /home/user/work/venv-agent/bin/python -I -B -m pytest -q -p no:cacheprovider /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner107-independent-review/archive-extracted/tests --agent-root /home/user/work/agent
    40 passed in 7.34s

    /home/user/work/venv-agent/bin/python -I -B -m pytest -q -p no:cacheprovider /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner107-independent-review/baseline-1.0.6/tests --agent-root /home/user/work/agent
    36 passed in 5.71s

The independent red-before run used the exact 1.0.6 scanner with the 1.0.7 test file containing only the four new cases:

    /home/user/work/venv-agent/bin/python -I -B -m pytest -q -p no:cacheprovider /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner107-independent-review/old-1.0.6/tests --agent-root /home/user/work/agent
    4 failed, 36 passed in 5.63s
    The four failures are exactly opacity, cropLeft, entrance, and exit.

The candidate dynamic probes additionally passed: one projector call; marker redaction; all four incomplete/unknown-retention cases; explicit clear/opaque-extension preservation. Static AST checks found one projector call at scanner line 588, no removed old test function, and no network imports.

## Logs and limits

- [archive integrity log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner107-independent-review/archive-check.log)
- [candidate 40-test log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner107-independent-review/candidate-1.0.7-pytest.log)
- [exact 1.0.6 baseline log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner107-independent-review/baseline-1.0.6-pytest.log)
- [red-before four-case log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner107-independent-review/before-1.0.6-new4-pytest.log)
- [independent behavior probes](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner107-independent-review/independent-probes.log)
- [1.0.6 to 1.0.7 flat diff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-scanner107-independent-review/flat-1.0.6-to-1.0.7.diff.log)

No full suite, browser, socket, media, credential, owner-data, install, network, or test-service run was requested or performed. No blocker remains for this review. Product worktree status is clean.
