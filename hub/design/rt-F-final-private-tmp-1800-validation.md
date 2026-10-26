F-final validation

- Preflight: PASS against the controlling independent installation/readback review. The registered delivery-v2-final command, source11, registry postimage, source/gate tuples, final heads/trees/bases, and canonical notes matched the settled inputs.
- Dispatch: exactly one normal `request-test integration:runtime delivery-v2-final --no-cache` request, with `TEST_KEEP` and `TEST_PRIVATE_TMP=1`. The request private temporary directory was root-owned mode 0700 and its TMPDIR/TMP/TEMP mapping was accepted by the service.
- Service: terminal `fail`, exit 2; D68 delivery status FAIL after all-four-repo staging. The service lifecycle reports normal termination, sampler exit 0, one reaped child, no 4GB stop trip, and trace PASS.
- Packaging: no ZIP, checksum, manifest, bundle-tree acceptance, or final artifact review exists because the builder failed before package acceptance. Per authorization, no retry, repair, source/config change, alternate route, or cleanup was performed.
- Product tests/typecheck/lint: N/A; this task made no product changes.

Raw service receipt and retained staging paths are recorded in `result.json` and the normal service request directory.
