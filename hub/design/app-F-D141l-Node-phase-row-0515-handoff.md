# D141l handoff

The service now has exactly one new normal row:

```text
app full-d141-node-phase npm run test:node
```

This is registration only. It does not establish test coverage or REG0 and does not alter the existing full row, checks, source, pins, paired kit, or Composition documentary host.

Later receiving must use the source snapshot selected by the normal test service. Request the qualified App full pin `app-pin-5344c53e` first; if its `npm test -- --maxWorkers=3` result is Node `NOTRUN`, request the exact standalone row above. Then receive pristine upstream `d822d2f5d2bd05187b4ff5b6071c3e13945d4747` with its own exact `test:node` script, serially through the same normal no-cache service and normal admission. Preserve raw `KEEP` evidence for each phase.

The two expanded scripts are intentionally source-bound. The qualified source adds only `scripts/installer/update-manifest.test.mjs`; the pristine source does not contain it. The caller must derive each command from its source package blob and must not copy or normalize the lists.

The existing C0 request/reply envelope and merge semantics remain controlling: no envelope or product edits were made. The later body uses the normal 5.2 GB wait, has no paired-kit dependency, and must stop under the existing 4 GB policy rather than using a floor exception.

The preserved C0 request shape remains `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, `commands[schema_version,op,version,select,args,created]`, `label`, `steps[id,label,intent,tags,command_ordinals,patch,reads]`, `merge` (`fields|atomic`), `reads`, `Idempotency-Key`, `dry_run`, `source`, `rationale`, and `group_id`. The later receiver must retain accepted/merged `data`, `receipt`, `canonical_document`, `document_digest`, `provider_version`, `compiler_version`, normalized commands, `id_map`, base/previous, accepted revision/publication pairs, `rebased_onto`, `merge_mode`, complete steps, records, bindings, effects, dependencies, history, undo_steps, publisher, and echoed annotations; conflict `reason`/`head`; invalid `code`/`path`/`hint`/`suggested_command`; and preview `would_status`/null `receipt`.
