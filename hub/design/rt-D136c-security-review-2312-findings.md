# D136c independent security/privacy/production-path review

## Verdict: PASS

No findings. The final candidate is exactly commit `2f1fbb1fc2954dc54eda7f29656de8f15e38683a`, tree `37cfcd4f6108c1fdda401e563e3674503bc328ef`, with the three-file scope named in `source-manifest.json`.

### Production-path proof

- The existing `command_output` missing-observation refusal remains at `runtime_protocol/timeline_commit_auth.py:2267-2280`; the guard still tests `ref in result` and keeps the exact refusal message.
- `require` forwards an optional detail object only to the existing `reject` serializer (`timeline_commit_auth.py:18-21`). The new helper is called exactly once, from that guard; no dead helper or recorder/collector was added.
- `timeline_commit_store.reject` preserves the existing refusal envelope and conditionally adds only `details.safe_diagnostic` (`timeline_commit_store.py:36-50`). An AST call-site audit found no other `safe_details` caller.
- The real service path converts `CommitRejected` with `public_failure` (`runtime_protocol/service.py:2566-2579`), while an outcome failure uses the same serializer (`service.py:2560-2564`). The mounted POST route calls `commit_timeline` (`runtime_protocol/server.py:301-340`) and the standard handler emits `RuntimeErrorBase.as_dict()` (`server.py:416-423`). No alternate diagnostic transport was introduced.
- Existing authorization, CAS/head checks, SQL/materialization guards, evaluation transaction, and rollback path are outside the changed lines and remain intact. The focused production test observed no durable-row changes.

### Safe-detail review

The detail object is closed to `_SAFE_OBSERVATION_DETAIL_KEYS`: fixed phase/enums, booleans, bounded ordinals (`0..1_000_000`), `UNKNOWN`, and a one-way `sha256:` hash of an already-valid `sha256:` digest. It does not serialize identifiers, path components, labels, keys, user content, URLs, private paths, or raw digests. Adversarial sentinel identifiers/path/content/URL/private-path input was reduced to the allowlist with no unbounded output.

Presence and uncertainty semantics are retained: missing/invalid ordinals become `UNKNOWN`; missing bindings yield `binding_state=ABSENT` and ownership/continuation `UNKNOWN`; actual supplied bindings yield the corresponding bounded enum; invalid digest content yields `physical_digest_hash=UNKNOWN` and is never echoed.

### Prior evidence consumed

The App D136a final inventory is retained as PASS for finite static identity only. App D136b primary and independent reviews classify all 135 B022-B036/original9 cases UNKNOWN and prove no product gap or skipped setup. Original D136a/2136 remains NO_GO/HELD: nine setup errors, zero pass/fail/skip. No actual cause was inferred or converted into a product finding here.

### Remaining limits

This is targeted evidence only. It does not qualify original9, the full auth family, browser/HTTP live behavior, or any downstream App outcome. Runtime integration merge remains manager-owned; no backport or App change was authored.
