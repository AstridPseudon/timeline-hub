# OPS D21 runtime maker independent review/install — 2026-10-23

## Result

PASS. Independently reviewed Sol 1343's candidate and installed it only after the required idle proof.

- Candidate/live SHA-256: `9fc7f72a7d03fcb4618310ad57f5c9cf111b78a59b2c02caa702073d0951fd09`
- Exact predecessor backup: `$ORCH/bin/make-runtime.20261023T135414Z.bak`
- Predecessor/live backup SHA-256: `5245f264336d65c4a5847d9e4f05734e77d25ede0dd35d64008e5a4c45aac0e6`
- Install time: `2026-10-23T13:54:14Z`
- Live file remains a root-owned regular `0755` file.

The only authorized shared mutation was the timestamped predecessor backup and atomic `.new` → `mv` replacement of `$ORCH/bin/make-runtime`. No product, test, generated, pin, contract, daemon, child-maker, request-writer, queue, or Git files were changed.

## Independent review

The candidate is limited to the requested exact-source positional carrier and registration plumbing. The request writer and dispatcher RUNTIME branch are unchanged. The approved remote template was explicitly selected as `remotion-env-nodes`; no retired `0012` row or guessed default was introduced.

Approved template facts independently rechecked:

- suite-row SHA-256: `ffdb0b13c65f106d7b818208343feb3f438dfc943f4af57c5f612ddcf73dc036`
- env SHA-256: `e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02`
- Agent source: `f6116e1b658514021cbbf08d5a6f16a240523f1a`
- Runtime source: `8592822fd11275540f596562f43c715676f2bc0f`
- lock SHA-256: `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`

Independent private smoke command:

```text
python3 /tmp/rt-OPS-runtime-custody-review-install-1351/independent_route.py
```

It passed the real copied `request-runtime`, the exact dispatcher RUNTIME branch, a throwaway name, private roots, and `env -i` with all `RUNTIME_*` identity variables absent. External builder/tool work was stubbed only; candidate argument parsing, registration, source identity checks, immutable publication, and guards were real. The emitted env and suite guard carried both exact source identities. The supported production command shape is:

```text
$ORCH/bin/request-runtime agent-remotion-ap2-p1-f611-1351 f6116e1b658514021cbbf08d5a6f16a240523f1a f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d /home/user/work/wt/agt-pin-f6116e1b /home/user/work/wt/rt-pin-8592822f 8592822fd11275540f596562f43c715676f2bc0f remotion-env-nodes
```

Those sanctioned checkout paths were not mounted in this review namespace, so no real provisioning or fresh immutable bench was claimed. Proof remains the owner of that later bench.

## Tests/checks

- `bash -n` on candidate, unchanged request writer, and unchanged dispatcher: PASS.
- `shellcheck`: unavailable in the environment; precise static review performed instead.
- Independent request → dispatcher → candidate smoke above: PASS.
- Candidate/installed diff reviewed against installed `5245f...`: only the intended argument/registration changes.
- Sol inherited controls: author evidence records 30/30 PASS; this review retained those artifacts and independently checked the route-specific behavior.
- Author queued route controls: 20/20 PASS; route artifacts retained for comparison, with the independent seven-argument `remotion-env-nodes` run above.
- Extracted actual JavaScript module-version checks: 4/4 PASS in author evidence; no real Remotion provisioning was run per D21.
- Canonical bootstrap/build and immutable-publication source proofs remained byte-identical per protected-source proof.

No full Runtime/product suite was run or requested; this is an isolated host-kit review and the task forbids real build/download/package installation.

## Idle/install/publication custody

At `2026-10-23T13:54:14Z`, the fresh normal non-hidden pending inventory was empty. Under the unchanged dispatcher semantics, a RUNTIME record remains pending until `make-runtime` returns, so this proved no dispatcher-owned make-runtime target was active. The dispatcher heartbeat was current at `2026-10-23T13:54:09Z`. The worker process view was recorded but is not represented as a host-wide process view.

The live/backup/hash/stat evidence, protected-source hashes, queue inventory, and bounded publication observation are under `workers/rt-OPS-runtime-custody-review-install-1351/evidence/`.

The normal hub kit/HEAD publication path was not mounted here (`$ORCH/hub` contains inbox only). A bounded five-sample, 50-second read-only observation recorded both paths absent; no sync daemon, host script, direct kit write, or Git write/integration operation was invoked. Manager/normal publication must be observed externally.

Required manager board line:

`KIT CHANGE: make-runtime 9fc7f72a7d03fcb4618310ad57f5c9cf111b78a59b2c02caa702073d0951fd09 — exact Agent/Runtime positional custody carrier; predecessor 5245f264 backed up at 20261023T135414Z.`

## Next steps / limitations

1. Observe normal hub kit and committed HEAD propagation externally; do not queue a fresh real bench until that propagation and actual exact checkout receipts are present.
2. Proof owner may run the report-all immutable bench on Agent `f611...` / Runtime `859...` using the explicit `remotion-env-nodes` command above.
3. Do not treat this kit PASS as production readiness or as P1/P3 evidence.

Report-only Runtime branch; no commit or merge performed by this worker.
