# Runtime Main-merged014 corrected paired candidate

**SHARED PRIVATE CANDIDATE — NOT PUBLISHED.** No `PUBLISHED` marker, consumer
pin, integration adoption, or peer pin is authorized. Manager acceptance of the
corrected full is still pending; the corrected full is RED.

## Exact server tuple

| Field | Value |
| --- | --- |
| Runtime server SHA | `6e845a187684919c162b29568496c015bda1a591` |
| Runtime server tree | `7f11d7e159d46a88a22111c414aa7bdf7b599d9d` |
| Parent / generated producer | `4dd643808e93be431f8250c0b6d34320918776ec` / `8d53e2e1043eddfcfd92fe5983a5404b94745d63` |
| Main-merged base | `8bd92de606647d6ffc8887436a3dde3f95ea2330` (tree `d964d7138be203f7f18d8ff1f4f109805161cf5d`) |
| Main parents | `7a956c027cbbcb498a50de59d85f3b424897f70b` + `b535646faaad2f8ae7968dfe0f4fa3057f960264` |
| Contract/client version | `0.2.14` / `0.2.14` |
| Raw Agent schema | `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` — 55 definitions / 29 operations |
| Runtime schema digest | `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816` |
| Health schema | `sha256:dcaec4238eec1633683b3bc223c039f78e7f9066effb18d80667a4a903f4510e` |
| Services schema | `sha256:10614b9c5a8f044b4c6727701147197b91410ddaf4230b8fa990b78255574018` |
| Raw commit bundle | `sha256:6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3` |
| Full 76-artifact manifest file | `sha256:a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d` |
| Full 76-artifact producer/version | `astrid-runtime` / `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac` |

The corrected source preserves the generated/client/schema/package and raw
artifact bytes from the approved 76-path manifest. The official App artifact
source is `contract/artifacts.json` at this exact server SHA/tree; App must use
its normal `scripts/vendor-lock.mjs` updater after manager acceptance, not a
hand-copied or public-013 artifact.

## Required Main behavior and qualification counts

- Health responses require `status`, `protocol`, `schema_digest`,
  `runtime_epoch`, `runtime_session_id`, and `runtime_instance_id`.
- Health service entries require `name`, `state`, `last_exit`, and
  `restart_count` (optional `reason`). Service declarations require
  `version: 1`, `services`, and per-service `name`, `argv`, and `restart`
  (optional `env` and `ready.file`/`timeout_seconds`).
- Generated clients use the `/v1` door. The qualified local-door operations
  are `commitTimeline`, `listTimelineCommits`, and
  `getProjectMediaSelection`; there is no `/astrid/v1` route or paired relay.
- Contract/artifact/generation: **1,581 local tests passed; 76/76 artifacts**.
  Commit integration: **11 passed**. Door suite: **1,293 passed**. Gate 4:
  **29 Python + 61 TypeScript passed**. Corrected source gates: **50 direct
  passed, 146 central passed**. Gate 2 corrected subset: **7 passed**;
  historical 51-case proof remains retained. Gate 7 dry run `32417` passed
  all four bundle/linearized-patch tree comparisons; no final ZIP.

## Full results and remaining gates

The prior full on `4dd6438` / tree `d396f8f` remains RED exactly:
**5,981 passed, 5 failed, 1 error, 26 skipped, 17 xfailed**. The independent
review of the six failure repairs is **APPROVE**; it restored Main startup
semantics and scoped the platform `os.open` fixture without weakening tests.

The corrected full is a separate run on `6e845a1` / tree `7f11d7e`, not a
reinterpretation of the prior result:

```text
rt-m2-main014-corrected-current-candidate-compose-full-1020230205-26822
5740 passed, 3 failed, 245 errors, 26 skipped, 15 xfailed, 12 warnings
319.51s; exit 1
```

The three failures are the foreign-owned-shot refusal and the service/HTTP
historical text-binding exact-retry cases; the 245 errors are concentrated in
reference-authority/catalog HTTP cases. This result is not accepted as green.

Remaining gates are manager acceptance/classification of this corrected RED
full, then a new matched Agent/App consumer cohort against this exact tuple,
their `/v1` door qualification, and coordinated adoption. No publish,
`PUBLISHED`, peer pin, or public artifact mutation may occur first.

## Consumer handoff (after acceptance only)

Root must provide an immutable checkout at the exact server SHA as
`RUNTIME_PRODUCER`. Agent’s one normal producer-lock command is:

```sh
python3 scripts/vendor_lock.py update runtime.lock.json --producer "$RUNTIME_PRODUCER"
```

Then Agent must run its normal lock check; App’s official source remains the
exact Runtime `contract/artifacts.json` above and its normal updater/checker.

For identity only: current public Runtime `0.2.13` producer is
`2c4ac180c2220bdad966bc01e95ad230e99ce26a` with its unchanged 75 artifacts.
The old private comparison is Runtime `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`
with artifact version `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.
Neither is the corrected 0.2.14 candidate; do not relabel either one.
