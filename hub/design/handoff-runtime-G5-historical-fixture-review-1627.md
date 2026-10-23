# Runtime G5/R2r historical-fixture review (1627)

## Verdict

**PASS for the independent source/custody review; G5 fixture readiness remains
FAIL/BLOCKED.** The previous audit correctly found no exact carrier in the
inspected Runtime catalog, but its conclusion was too narrow: lack of an
existing backup does **not** establish that an authentic old-writer fixture is
impossible to author.

The existing pre-cut Runtime capture path can author this fixture through the
old public service and normal authenticated backup/restore. That exact authoring
and restore/adopt run was not executed here. Therefore the exact parent digest,
publication receipt, predecessor pair, and full closure remain unqualified.

## Required target

The expectation packet is expectation-only, not accepted history:

- packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/g5-sdk-fixture-expectation-20261023-b6069d1d.json`
- manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/g5-sdk-fixture-expectation-20261023-b6069d1d.manifest.json`
- required parent digest: `sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb`

The source mutation is the four-line target setup in Agent's
`tests/editing_conformance/test_commit_runtime_m1.py:35-47`: add the
`music-other` audio track and clip, set the complete legacy `word:word-1`
application object including explicit nulls and opaque values, and mirror
`config.clips`. The literal `m1-journey-baseline` revision is not required.

Qualification must retain three shots, three internals, all physical sharing
and occurrences, the registry and both music clips, `music-other`, the legacy
app declaration, absent-versus-null distinctions, opaque values, all required
CAS/media, and a genuine publication receipt with predecessor ancestry.

## Custody/search result

The earlier Agent/Sol audit evidence covers 28 retained parent images across 12
Runtime 9ce archives and found zero exact payload matches. I independently
searched beyond that bounded catalog:

1. The frozen R4 SDK, Runtime, App, and Composition refs were inspected with
   `git ls-tree`; none contains a matching Runtime realm/archive or the target
   digest.
2. Read-only filename/content inventory covered `/home/user/work`,
   `/home/user/peteromallet`, `/home/user/banodoco`, and the current ORCH
   archive/worker/design area, excluding only `.git`, `node_modules`, and
   Python caches. No target digest, `m1-journey-baseline`, or `music-other`
   carrier was found outside the already-known evidence/docs.
3. All discovered `precut-*.tar.gz`/`precut-*.tar.xz` copies reduce to the same
   12 unique archive hashes. The known Runtime archive hashes include the
   default `e3047732…54a6b5`, `music-documents` `f955ea28…a094db`,
   `anchor` `19033fe2…16d47`, and `raw` `e5eb4b5c…93cdb5`; no additional
   operator/current-ORCH carrier appeared.

This establishes **existing capture not found** within the searched custody,
not universal proof that an unlisted operator backup cannot exist.

## Existing author/restore capability

The source supports authoring an authentic carrier:

- `tests/precut_realm_fixture.py:46-69,148-176` is the existing safe archive
  extractor, verifier, and two-copy `restore_backup` loader. It is restore
  tooling, not a DB injector.
- `tests/timeline_commit_film_fixture.py:28-45` adopts the loader's pins and
  opens only the duplicate root, preserving the captured source and CAS.
- The existing variant capture runner
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-capture-variants/capture.py:50-105`
  demonstrates the complete supported capture shape: load a pre-cut realm,
  run an old Runtime `RuntimeService` public setup, call `create_backup`, then
  `verify_backup` and `restore_backup`. Its recorded command was:

  ```sh
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=/home/user/work/wt/rt-m2-precut-fixture:/home/user/work/wt/rt-m2-precut-fixture/tests:/home/user/work/wt/rt-m2-precut-fixture/packages/python \
  /home/user/work/venv-runtime/bin/python \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-capture-variants/capture.py
  ```

- `tests/capture_direct_render_fixture.py:26-53` independently proves the
  old-source pattern: assert the selected old Runtime source, execute only the
  public setup prefix, call `create_backup`, and archive it. It explicitly
  forbids using the capture tool as a compatibility writer.
- The old `tests/test_timeline_commit_integration.py::film` setup used by that
  runner already publishes a second audio clip through the old public
  `RuntimeService.publish_parent_composition`, then captures the realm. The
  target setup has the same supported publication shape; its exact four target
  mutations are visible at the Agent source above.
- The old Runtime publication implementation resolves existing shot/internal
  records from occurrences, validates the parent and media dependencies, and
  records a normal event/idempotency receipt. `create_backup` then captures
  the resulting SQLite/CAS closure. This is the required coupling for genuine
  predecessor, publication, receipt, child closure, and CAS custody.

Classification:

| Question | Finding |
| --- | --- |
| Existing exact capture found? | **No** in the searched catalog/custody. |
| Existing tooling capability unsupported? | **No evidence of unsupported capability.** Old public publication + backup/restore already authors analogous variants. |
| Exact target authoring executed? | **No; unexecuted.** |
| Exact target restore/adopt executed? | **No; unexecuted.** |
| Four Agent bodies run? | **No, correctly held.** |

The `anchor` and `music-documents` carriers are not substitutes: they differ in
track identity and/or legacy app/null/opaque fields. The current Runtime route
is retired and the current Agent semantic provider correctly refuses an invalid
new legacy orphan; neither fact blocks an old-source capture through the
pre-cut public service.

## Minimal bounded next author brief

**Owner:** Runtime fixture owner. **Custody:** a private worker temp root during
capture; after verification, preserve the authenticated archive and manifest
under the ORCH design/evidence path, then expose it to the Runtime fixture lane.
Do not modify the current integration worktree or the existing 12 archives.

1. Pin the old Runtime source used by the existing capture runner and assert
   `runtime_protocol.service.__file__` resolves inside that source. Use the
   existing `precut-v31` loader to obtain a disposable duplicate.
2. Read the original canonical parent through `RuntimeService`/`verify_baseline`.
   Apply exactly the four target mutations from Agent lines 35-47, without
   changing children, registry media identity, occurrences, or source docs.
3. Call the old public
   `RuntimeService.publish_parent_composition(project, timeline, body,
   idempotency_key=...)` with `expected_head` equal to the retained original
   head and any non-special authentic revision spelling. Do not use SQL,
   `store.conn`, direct CAS writes, a current retired route, a provider
   acceptance, a guard waiver, or forced history/receipt IDs.
4. Immediately read back the publication and `verify_baseline` on the private
   duplicate. Assert the exact `b6069d1d` parent digest, all three shots and
   internals, registry/media/CAS, `music-other`, legacy/null/opaque fields,
   predecessor head, event chain, idempotency receipt, and manifest.
5. Use existing `create_backup` with the test fixture key, then existing
   `verify_backup` and `restore_backup` into a second disposable root. Run the
   existing baseline verifier/installer and read the same facts back. Preserve
   the archive hash, manifest, receipt, and actual revision/publication pair.
6. Run only narrow fixture-loader/restore tests and a read-only closure check.
   Do not run the four bodies, full suite, browser, or live journey in this
   authoring task. The manager may later run the original four unchanged after
   the carrier is independently reviewed.

The capture is supported in principle but must be marked **unexecuted** until
the source command above produces the exact digest and the restore/adopt checks
pass. If the old public service rejects the exact target, record that as a
concrete tool-capability result with the refusal and source line; do not replace
it with a current-route attempt or fabricate history.

## Consumer boundary preserved

The fixture is only setup authority. The original bodies must continue using
the normal production caller: Agent `WorkspaceClient`/`TimelineSession` over
the Runtime commit transport with the normal v2 request scope, base revision /
publication pair, commands, label, steps, merge mode, declared reads, dry-run
form, source/rationale/group and idempotency key. Preserve the existing
`accepted`/`merged` replies with `{data, receipt}`, conflict reason/head,
structured invalid code/path/hint/suggested-command, and receipt-free preview
status. No alternate executor or new API is inferred.

The frozen producer/client and schema references `34eac0041b0891e9011966b39bcbd26053fde5bc`,
`d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`, and the
`819acf` App artifact remain untouched. No contract decision is made by this
fixture review.

## Changes and limits

- No product, test, generated fixture, schema, pin, branch, ref, database, or
  shared dependency was changed.
- The Runtime worktree was clean (`git status --short` empty).
- No network, provisioning, dependency installation, host/daemon, or permission
  retry was attempted.
- No pytest suite was run; this was a read-only source/custody audit. The exact
  fixture authoring and restore/adopt evidence is therefore still pending.

