# D139 independent source/security review — FAIL

Candidate `86a1a97617445905694e63ca6bb118879a7ecedd`, tree
`049e8b5bec9da892b0ea9d1003e2f09f1d361d46`, parent
`cf80cfcb918ee9e311a294fb7291ad5e11c48d0b`.

## Decision

FAIL / NOT_READY. The source-only candidate has useful fail-closed inputs and
the existing Agent/Runtime custody checks remain visible, but schema authority
is not safe to release. The maker accepts a live physical directory whose bytes
are not authenticated to the D73 source tree, and it can change after the Store
identity digest is computed but before archive/build. No CAS, install, child
request, body, or source acquisition was performed.

## Findings

- **SRC-001/SRC-002/SRC-003 — blocker/high:** `--schema-source` is checked as a
  physical directory with a few required files, not as an authenticated D73
  carrier. The manifest fields are self-asserted; there is no Git/tree/archive
  comparison, owner/mode/hardlink policy, or closed source set. The source hash
  at lines 463–466 is followed by live `tar` reads at lines 832–845 without a
  schema CAS/recheck. A Store key can therefore bind source A while the child
  receives source B.
- **AUTH-002 — blocker:** the current machine has no portable pinned schema
  source carrier. Agent2136 is valuable qualified distribution/RECORD/direct-URL
  evidence for `0.0.2`, but it is not permission to copy the shared venv or use
  an old overlay. Input2149 is static census evidence, not source authority.
- **AUTH-003 — high:** schema hashes enter the Store identity/key, but the
  provision report and local inventory expose only distribution metadata and
  direct URL; they do not carry the exact manifest/source identity needed for
  independent receipt binding.
- **CAS-001 — unverified:** the candidate is
  `7905232e0dc4b77921ecf257f89f2a951614e0dcbc9eea547c08c992062e5792`, 81,516
  bytes. The parent/current installed helper is
  `f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f`, 75,541
  bytes; the prepared manager route instead expects live D137 preimage
  `4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`, 75,503
  bytes. The route is internally guarded but was not run and is not an f07
  preimage proof.
- **CENSUS-001/CENSUS-002 — high:** the executable checker treats relative
  names such as `.sdk`, `_base`, `_command_state`, `_common` and `_doc_patch`
  as absolute installed distributions, and explicitly treats external
  `typing_extensions` as stdlib. The author’s 602 misses therefore cannot be
  interpreted as missing distributions.
- **CENSUS-003/CENSUS-004 — bounded only:** input2149 reports a useful static
  closure (431 roots, 1146 unique imports, 1001 reachable source modules, no
  parse errors) and clearly limits dynamic/plugin execution. The checker’s
  literal-dynamic boundary and broad guard classifier remain non-exhaustive.
- **EXEC-001/EXEC-002 — blocker:** no genuine registered child receipt is
  available. `/usr/bin/python3.13` is a system interpreter, not proof of a
  Store entry. The author’s historical check-only positive is not a current
  receipt; the same current system interpreter without `PYTHONPATH` failed all
  six bounded imports. The check-only tool never invokes the launcher, Store,
  installer, inventory verifier, registration, or smoke.
- **EVID-001 — high:** the 44-test suite has no schema-binding, manifest-tamper,
  source-race, schema inventory-identity, or check-only CLI tests. The prepared
  E2E is honestly `NOTRUN / WITHDRAWN`, so it supplies no positive-path proof.
- **EVID-002 — pass:** author evidence is honest and keeps the blocked result
  visible; it is not being upgraded to release evidence.

The existing Agent/Runtime archive, direct-URL, RECORD, import-origin,
marker, and ownership checks were preserved by source inspection and the
embedded blocks compiled, but that is source preservation only, not a real
child qualification.
