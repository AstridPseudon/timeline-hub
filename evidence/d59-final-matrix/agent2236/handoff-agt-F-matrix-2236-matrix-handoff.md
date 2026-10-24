# F/P4 D59 finite matrix handoff

Status: **PENDING final tuple**. This packet is a finite handoff to Runtime
matrixLuna2228. It does not authorize a run, registry installation, D59 credit,
or final-core/render readiness.

## Source identity and guard

The current Agent source is `7c485e5b612a31a9b4f6e9a67163612a4a3313d4`,
tree `742a1195e33b1b94cbd7d817c5b4d8167c4a20d5`. Its tree is byte-identical
to the tested actual Agent `c2a63bbee9369b84bec7f4bfec06f447df02c27b`,
tree `742a1195e33b1b94cbd7d817c5b4d8167c4a20d5`; the commit identity is not
silently substituted in the final tuple. Runtime is `732c48c6f5a9441a65c61b24595d454a1cd3e180`,
tree `7ed0559c6f0a05954427cc668e303b6cd2f51586`. The current App is
`bceb0350326f22beefdde5c5ba275412bb09b419`, so the old actual 29429 App pin
must not be presented as final. The final four-repository tuple is therefore
PENDING.

Launcher source is
`tools/p4-d73-pinned-launch.sh`, SHA-256
`cec561761cb90adbe94dbcc1b1f6b62afb107f1a90e079c6ce2b823405a072d1`, Git
blob `2844cec15b97fa995ecaf120961fc891b8e13b1c`. The single CAS installer is
`tools/install_p4_launcher.py`, SHA-256
`46595ea2b6e0738736ebf181f731930144737ac8d39902e4903b94e23c2c94f2`, Git
blob `eb43fe81c426f2a85797d7cee491b8e822490eda`. The Runtime schema input is
`/home/user/work/venv-agent/lib/python3.13/site-packages` with digest
`sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`.
The exact identity record is `source-identity.json`.

## Existing actual P4: 29429, five selectors

The live suite row is copied byte-for-byte as `current-live-five-row.txt`.
It is distinct from the final three-selector candidate and from the older
1755 core scope. Its actual tuple is preserved in
`actual-29429/handoff-agt-D84a-29429-tuple.manifest` and its checkout receipt
in `actual-29429/handoff-agt-D84a-29429-checkouts.txt`:

```text
Agent c2a63bbee9369b84bec7f4bfec06f447df02c27b / tree 742a1195e33b1b94cbd7d817c5b4d8167c4a20d5
Runtime 732c48c6f5a9441a65c61b24595d454a1cd3e180 / tree 7ed0559c6f0a05954427cc668e303b6cd2f51586
App 5fcb9ad5cf8af93709d682ab994bcdb1af207f07 / tree 8f6c14f184297659b4bc0500c8d18f84c42baeee
Composition 635f4de06fda22a85fc2e4cfc764d0153a4c9f40 / tree 5ab5191a296980a0a6bcd1178ab6902d6478a148
```

The exact parsed body command was:

```text
-m pytest -q -o addopts= -p no:cacheprovider --timeout=45 -m integration --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-R2-D84a-five-2214/evidence/p4-r2-d84a-five-run.xml tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo tests/core/test_timeline_element_publication_runtime.py::test_public_helper_restart_exact_retry_later_head_inverse_redo\[False-None\] tests/core/test_timeline_element_publication_runtime.py::test_public_helper_restart_exact_retry_later_head_inverse_redo\[False-public-element\] tests/core/test_timeline_element_publication_runtime.py::test_public_helper_restart_exact_retry_later_head_inverse_redo\[True-None\] tests/core/test_timeline_element_publication_runtime.py::test_public_helper_restart_exact_retry_later_head_inverse_redo\[True-public-element\]
```

Service `agent-p4-current-becfe-http-3legs-1024221732-29429` returned NO-GO,
exit 1: four of five selectors passed; the ten-note selector timed out at
45.314 seconds. The four positive Runtime-publication selectors were 10.486,
11.308, 7.360 and 7.470 seconds; JUnit time was 84.318 seconds. The exact
XML, log, exit, receipt and outcomes are copied under `actual-29429/`.
This result is evidence for the existing actual row only; it is not a final
three-selector result and does not authorize an Agent-side rerun or diagnosis.

## Final P4 candidate: exactly three original selectors

The finite final candidate is the three original P4 files only:

1. `test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back`
2. `test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo`
3. `test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document`

The exact membership is `final-p4-three-selector.membership.tsv`; the exact
parametric D73 body is `final-p4-three-selector.command.sh`. It intentionally
uses `$P4_LAUNCHER`, `$P4_D73_MANIFEST`, `$P4_D73_EVIDENCE` and
`$P4_D73_REQUEST_ID`, not historical literals. `final-p4-pending-input.env`
is the non-runnable manifest recipe: every four-repo SHA/tree/parent/path and
the original-test hash must be rendered from fresh receipts before use.

## D73 manifest and launch sequence

The launcher requires these manifest fields: `format`, four `*_sha` values,
four `*_tree` values, `agent_parents` plus optional other `*_parents`, four
absolute exact checkout paths, `python`, `node`, `profile`, `schema`,
`node_version`, `profile_lock_sha`, `profile_archive_sha`,
`profile_registry_sha`, `composition_version`, `original_p4_test_hash`,
`service_versions`, and `junit_paths`. The actual 29429 values are retained
only in the historical actual manifest; the pending template has placeholders.

The sequence is fixed and guarded:

1. Obtain four normal checkout receipts and render one manifest; do not chase
   moving heads or mint a new checkout in this handoff.
2. Invoke the existing launcher with `MANIFEST run -- COMMAND`. It validates
   format, SHA/tree syntax, absolute real checkout paths, launcher provenance,
   exact HEAD/tree/clean status, parent predicates, and the aggregate hash of
   the three original P4 files.
3. It records the manifest, request id and runmanifest, then preflights Python,
   Node, schema, profile node_modules/non-symlink, package-lock/archive/
   registry hashes, Node version, Runtime lock (15 files), import origins,
   client `0.2.14`, schema digest and Composition package version.
4. Only after preflight does it run the body from the Agent checkout with
   `PYTHONNOUSERSITE=1`, Agent+Runtime `PYTHONPATH`, Runtime source variables,
   profile variables, and the pinned Python executable. It records command,
   log and exit status. The original 45-second timeout remains unchanged.

The launcher preserves the existing positive/poison behavior: a harmless dry
stub must be exactly one call with exit 17; a poisoned SHA must fail before the
stub with zero calls. No real body was run by this worker.

## Prepared final-core 1755 scope

`prepared-1755/` is the existing preparation packet, not a final run. Its
collection had 8,817 collected nodes across 392 files: 8,814 core-blocking
nodes, one D13 environment node, and two D23 deferred known-gap selectors.
The three original P4 HTTP selectors are excluded from that core collection
and remain the separate final P4 candidate above. The D13 and D23 membership
is retained in `final-core-collection.json`/`final-core-nodes.txt`; no skip or
xfail was invented here. Current worker 2234 owns the active full-core
rehearsal and its registry row and must refresh this prepared scope.

The exact old 1755 candidate row is copied as
`prepared-1755/final-core-row-1755.txt`; it contains historical literals and
is explicitly known-scope only. The exact collection command and input are
also preserved in `final-core-collection.json` and
`final-core-prep-dry.manifest`. The prepared collection output, XML, source
hashes, dry positive (`count=1`, exit 17), poison (`count=0`, nonzero), and
CAS verification are copied byte-exact. There is no final-core body XML or
green result in this packet.

## Existing CAS install entry (not executed)

The only install entry is the existing helper:

```text
/home/user/work/venv-agent/bin/python -P tools/install_p4_launcher.py CANDIDATE_SUITES_CONF REGISTRY_SUITES_CONF EVIDENCE EXPECTED_REGISTRY_SHA256
```

It locks the registry, checks mode 0600 and the expected before hash, requires
exactly the three owned keys (`p4-current-becfe-http-3legs`, `p4-current-single`,
`final-core`), writes one timestamped 0600 backup, atomically replaces the
registry, fsyncs the directory, verifies the after hash, and verifies all
outside rows are byte-identical. This handoff does not execute it and does not
touch any shared registry or row.

`missing-files.txt` lists the deliberately absent pending outputs. The
top-level `sha256manifest` covers every packet file and is regenerated after
the packet is assembled.

## C0 wire-shape reminder

The production caller is the real Runtime commit/provider. The v2 request
fields are `api_version`, `project_id`, `timeline_id`, `base_revision_id`,
`base_publication_id`, `commands`, `label`, `steps` (`id`, `label`, `intent`,
`tags`, `command_ordinals`, `patch`, optional `reads`), `merge` (`fields` or
`atomic`), optional `reads`, `dry_run`, `source`, `rationale`, `group_id`, and
HTTP `Idempotency-Key`. Replies retain accepted/merged closure, records,
effects, bindings, history and receipt; preview has `would_status` and a null
receipt; conflict has `head` and `reason`; invalid has `code`, `path`, `hint`
and `suggested_command`. The 45-second, security, freshness, ABA and ABI
guards remain unchanged. No client, schema, generated, provider, or product
change is part of this handoff.

