# Runtime M3 authorized Theme preparation seam

Status: proposal only; no Runtime product change is authorized until Agent,
App, and Viewing directly ACK the carrier and its authority boundary.

## Finding

The closest existing Runtime preparation path is the normal project-scoped
`rendering.render` admission in `RealmStore.create_task()`:

1. `_freeze_managed_render_inputs()` resolves the Runtime-owned timeline,
   exact saved or candidate authority, canonical config/registry, selected
   profile, and required execution facts.
2. `rewrite_spec_snapshots()` uses the existing `prepare_snapshot()` /
   `publish_snapshot()` CAS path before the task is durable. That path retains
   the exact snapshot object and adds its digest to `input_object_ids`.
3. The existing named-input binding then accepts an already-authorized
   descriptor in the ordinary input manifest. The relevant shape is:

   ```json
   {
     "name": "theme",
     "object_id": "sha256:<digest>",
     "digest": "sha256:<digest>",
     "filename": "theme.json",
     "required": true
   }
   ```

   `InputBinding` requires `object_id == digest`; Runtime checks the ordered
   manifest and project association, and GenericHost materializes the named
   object only after admission. This is a valid transport carrier, but it is
   not source authority: membership in `input_object_ids` cannot establish
   which Theme was selected.

There is no current pre-admission path that supplies authoritative Theme
bytes. The timeline snapshot contains projected `config` and `registry`; its
`theme` is a metadata slug and `theme_overrides` is config data. The current
`theme.json` materialization is post-admission. `RuntimeService.ingest()` is
the existing normal project-object API, but the renderer/requester credential
cannot be granted `projects:write`; using it from the renderer would violate
the custody boundary. Therefore no existing flow suffices by itself.

## Smallest extension proposal

Extend the existing managed render invocation with a **private internal
preparation mode**, reusing the current managed invocation custody and result
shapes. This is not a new endpoint, public DTO, store, resolver, journal, or
certificate:

1. The private mode calls the same `_freeze_managed_render_inputs()` path and
   carries only the Runtime-selected timeline reference, saved accepted or
   candidate authority tuple, exact config/facts/profile, and the existing
   idempotency identity. Candidate preparation must retain its exact base and
   candidate binding.
2. Runtime obtains the producer's already-authorized project Theme source
   through the existing managed-input custody path. The mode must not accept a
   caller `theme_id`, inline Theme JSON, caller hash, browser-resolved value,
   arbitrary object descriptor, or a renderer-held `projects:write` token. If
   the current producer cannot expose that source through existing custody,
   Agent/App/Viewing must first agree which existing producer owns the source;
   Runtime must not infer it from the slug.
3. Agent receives only that Runtime-authorized `theme.json` carrier alongside
   the exact frozen config, calls exactly one existing
   `_resolved_theme_for_render(timeline_path, runtime_theme_path)` resolver,
   and canonicalizes the complete `{id, visual}` result.
4. The resulting bytes are retained with the existing project-owned CAS
   publication/ingest machinery under Runtime-managed custody. The requester
   is returned the existing named descriptor above, with `object_id` and
   `digest` equal, filename `theme.json`, and its position preserved in the
   ordered input manifest. No caller-provided digest is accepted as identity.
5. Final render admission reuses the existing exact CAS retention and recheck:
   project association, digest/bytes, selected saved or candidate authority,
   config/facts/profile, idempotency, and ordered named-input binding. Generic
   Host then uses its existing post-admission Theme materialization and Agent's
   existing task adapter forwarding. An absent carrier keeps the current
   default fallback and remains uncertified for explicit-theme parity.

The private mode is the smallest bounded change because it joins the existing
pre-admission snapshot freeze, existing project CAS publication, and existing
named descriptor without adding a second Theme resolver or a new authority
record. The precise existing producer/source lookup is the remaining cross-area
decision; it must be explicit before Runtime code is written.

## Agreement requested and ownership

- **Agent:** confirm that the only accepted source is the Runtime-authorized
  materialized `theme.json`, that Agent performs exactly one resolver call, and
  that the descriptor is emitted only after the complete `{id, visual}` bytes
  are canonicalized.
- **App:** confirm that it can request this private preparation as part of its
  existing requester-authorized managed invocation, without supplying slug,
  inline, browser, or caller-hashed authority, and that it consumes the
  existing named descriptor unchanged.
- **Viewing:** confirm that its existing task adapter forwards the named
  descriptor/materialized object without creating a second transport or
  source-selection rule.
- **Runtime (next owner after those ACKs):** implement only the private
  managed-invocation continuation and final recheck, reusing the existing
  custody/CAS/result types. Runtime owns transport membership and retention;
  Agent owns selected-source resolution. Neither side may treat transport
  membership as selected-source authority.

## Witness and limits

The existing normal-source witness is the Runtime snapshot preparation and
named-input path, not an explicit Theme positive case. The focused tests below
prove snapshot freeze/publication, exact replay retention, and named input
ordering. They do not certify the missing explicit-theme source join. No
product implementation, full suite, renderer/browser run, or default-five-case
replay is included in this proposal.

Evidence from this worker:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-m3-theme-authorized-preparation-seam-focused-nosocket tests/test_direct_render_admission.py tests/test_canonical_render_admission.py tests/test_remote_worker_deployment.py tests/test_task_admission_replay_identity.py::test_changed_snapshot_and_identity_refuse_before_any_store_publication tests/test_task_admission_replay_identity.py::test_exact_inline_snapshot_keeps_published_spec_and_admission_hash tests/test_task_admission_replay_identity.py::test_proven_exact_replay_retains_inline_snapshot_republication
# 141 passed in 15.18s
```

A broader file-level run also passed 234 tests, but five replay tests attempted
to start `RuntimeDaemon` and were blocked by the sandbox's socket prohibition
(`PermissionError: [Errno 1] Operation not permitted`). Those localhost tests
were excluded from the passing witness above; no full or live suite was
requested.
