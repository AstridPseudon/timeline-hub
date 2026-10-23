# R2 + F-D09 integrated readonly qualification — PASS

Date: 2026-10-23 UTC. This is a read-only qualification of the already merged
Agent integration head; no tracked worktree edit was made.

## Integrated snapshot and merge scope

- HEAD: `bf40ca73862a5368d9c0e10a3a797a234ade9bf0`
- tree: `bbb8eaf144390ffecb5f9af30043c06e02d8dabf`
- first parent: `4178d1d7065177e9bb4ced40f512256583d1180a` (R2 merge)
- second parent: `6562cde02c937d70b395718b8e2b71c4f01a1eb8` (D09 fixture)
- R2 reviewed commit: `7d58e0682253b7c2e204652ee14a48a39c7105ff`
- D09 reviewed commit: `6562cde02c937d70b395718b8e2b71c4f01a1eb8`

Exact blob checks passed:

- `tests/editing_conformance/test_inverse_stage_runtime_regressions.py` at
  HEAD is byte-identical to the reviewed `7d58e...` blob.
- `tests/integrations/test_d09_managed_scene_only.py` at HEAD is byte-identical
  to the reviewed `6562c...` blob.

The R2 merge changed only the seven-test R2 file. The integrated first-parent
delta changed only the D09 fixture. Excluding those two reviewed test blobs,
the integrated tree has no diff from the pre-merge R2 base. This preserves the
other product files and the protected current identities: Runtime producer
source commit `34eac0041b0891e9011966b39bcbd26053fde5bc`, canonical schema
SHA-256
`d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`, and the
approved Composition archive SHA-256
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

The actual Runtime checkout used by the local run was clean before and after
at `49ce53289bc37d9387a7d9e6b9c9b16072162181`; no sanctioned checkout repair
was needed.

## Required local qualification

Exact command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_inverse_stage_runtime_regressions.py
```

Result: **7 passed in 14.07s**, exit 0. The test itself checked the actual
Agent/Runtime module origins and source hashes around all seven cases. This is
the new seven-test R2 regression set, not the lost original 58-case probe.

## Required central qualification

Requested exactly once after the integrated head was frozen:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-R2-D09-integrated-1121 d09-current-v3-1113
```

Result directory:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-R2-D09-integrated-1121-d09-current-v3-1113-1023112232-12241/
```

Result: **pass, exit 0**, 1 passed in 133.45s (central wall time 136s), on
Agent tree `bbb8eaf144390ffecb5f9af30043c06e02d8dabf`. The executed node was
the approved existing D09 node:

```text
tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result
```

The central environment retained Node 20, the f1012 installed wheel record,
the supported environment bindings, and the `agent-remotion-v3-819acf-1110`
profile. No installer companion, rebuild, dependency/provisioning, guard,
source, pin, suite/profile, or orchestration change was made.

## Disclosures and limits

The archived profile's separate `npm run typecheck` failed because the archive
lacks generated registry files and two external `threejs-live-editor` modules.
That failure is disclosed as profile-level evidence only; this report makes no
whole-profile typecheck claim. The approved custody and live D09 result remain
qualified.

No full suite, original-58 recovery, HTTP/browser, native14, daemon, installer,
Git write, shared-dependency mutation, new tuple, tool bypass, or safety/
autoclassifier-denial path was run; no denial occurred. D17 copy-4 inverse
failure and G4 created-alias remain separate open items and were intentionally
not repeated.

No new review is required for this conflict-free merge of the two independently
reviewed test blobs. Recommended next step: record the PASS on the manager board
and retain the separate D17/G4 open dispositions.
