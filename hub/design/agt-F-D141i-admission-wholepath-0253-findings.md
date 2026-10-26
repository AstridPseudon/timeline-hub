# D141i whole-path admission findings

## Result

The exact production request reached the registered command, but the one genuine core body did not start. The authoritative terminal result is service `agent-agent-core-full-1026025151-24049`, exit `78`, with:

```text
REFUSED: controller admission disk floor not met: 4687142912 < 4700000000
```

## Why 0246 PASS missed the timing

The 0246 review was a command qualification, not a production admission run. Its brief and handoff explicitly exclude `request-test`, queue/admission operation, installation, and body execution. It therefore validated the wrapper's source/manifest/launcher controls but never exercised the interval in which the service creates its snapshot and dependencies.

The production sequence is:

1. `request-test` records the request and service ID.
2. `test-run` classifies `agent-core-full` as heavy and applies its inclusive 4,700,000,000-byte named-suite floor before starting the background run.
3. The background run acquires the bench lease and performs snapshot preparation before executing the suite command.
4. The registered 0238 wrapper starts, captures source/interpreter custody, then performs its own `source_admission` measurement.
5. That later measurement is 4,687,142,912 bytes, 12,857,088 bytes below the wrapper threshold, so it exits before launcher/body entry.

The manager's earlier dispatch witness was 4,821,594,112 bytes. The recorded drop to the wrapper measurement is 134,451,200 bytes. Under settled D89c, own preparation does not create a new admission decision; the continuous 4,000,000,000-byte stop remains unchanged. This report adds no gate or floor.

## Custody and finite blocker inventory

The suite row materialized exactly once at `suites.conf` line 31 and matches the reviewed row byte-for-byte. The wrapper, positive/poison manifests, source manifest, pinned four-repo tuple, and launcher hash all match the reviewed 0238/0246 packet.

The actual wrapper retained clean four-way `source-before` and `source-after` records, interpreter receipt, status, and the one-line disk trace. `service.txt`, `callerargv.txt`, launcher evidence, XML, raw stdout/stderr, runner exit, and monitor exit remain empty/not-started because the refusal occurs before those writes or before body launch. That is expected for this boundary and is separately recorded as “no body artifacts,” not as a test result.

Existing receipts provide bounded controls: pristine 27388 reached a body under materially higher headroom, and P4 10086 ran the exact cut tuple through the pinned launcher with 3/3 PASS. Neither is substituted for the missing core body.

No additional source, row materialization, launcher, dependency, product, behavior, REG/nonREG, or ship blocker is established from existing evidence.
