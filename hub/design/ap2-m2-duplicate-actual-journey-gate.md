# AP2 M2 duplicate actual-journey gate

The test-only patch is `ap2-m2-duplicate-actual-journey-source.patch`. It adds one case to the existing real three-products Playwright spec; it does not change product/shared seams, fixtures, dependencies, generated files, or packages.

The case uses the existing Runtime door, `seedThreeProducts`, command outbox inspection, CLI capture/commit, first-commit fault injection, Runtime restart, and recovery helpers. It drives the real canonical shot-group context menu and asserts:

- native `occurrence.duplicate`, caller-reserved occurrence/shot IDs, exact retry request bytes, and copied raw occurrence/shot opaque data;
- a disjoint Agent track-label publication after the duplicate and a newer local App label intent retained behind the lost acknowledgement;
- page reload, Runtime restart, explicit recovery, idempotent retry, server rebase, and two guarded inverses;
- the duplicate is removed by the second inverse while the Agent label and opaque fields remain; and
- no POST other than `/v1/.../commit` plus zero legacy composition-revision traffic occurs during the gesture.

## Central prerequisites

Run this against the exact App candidate containing the current duplicate helper/shared-port packet and this test patch. The current App profile contains `occurrence.duplicate` in its generated contract and helper, so use the stated normal safety tuple:

- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55` (safety keeper; resolve/use this exact full SHA);
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` (normal 0.2.13 producer);
- App: the harness-committed tree containing this patch, with its normal Runtime 0.2.13 lock and generated contract; and
- Linux Chromium, the real Runtime venv, and the Agent checkout/Python required by the existing `three-products` harness.

Do not substitute the ordinary014 pin or guess a shorter Agent SHA. The Runtime must admit the generated `occurrence.duplicate` operation and the App/Astrid/Runtime schema digests must agree. The test remains unqualified until this exact candidate tuple passes centrally.

## Named central suite proposal

The configured suite file has a broad `full-e2e-three-products` entry but no one-case Playwright entry. Add a named suite, without changing the test, equivalent to:

```text
app e2e-m2-duplicate-three-products npm run test:e2e:three-products -- --grep "M2 native occurrence duplicate"
```

Then the exact central request is:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-duplicate-actual-journey-source e2e-m2-duplicate-three-products) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Bind the exact App tree, Agent SHA, Runtime SHA, retained producer checkout, venvs, private Playwright output, and cache paths in the central suite command before requesting it. Do not run this browser/socket command locally.

