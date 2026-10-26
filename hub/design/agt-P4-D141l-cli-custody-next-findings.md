# P4 D141l CLI custody findings

Result: `PASS_EVIDENCE`.

1. The actual returned native service is independently identified as
   `agent-p4-current-becfe-http-3legs-1026103939-14092`, with terminal PASS and
   exit 0. The service directory, request, status, summary, exit, snapshot,
   external tuple, and terminal custody record agree.

2. The selected CLI test genuinely passed: 1/1, with zero failures, errors, or
   skips. JUnit, body log, body exit, launcher command, runmanifest, and the
   service summary align on selector and counts.

3. Admission is genuine: named LIGHT/5,000,000,000-byte P4 admission was
   available, the 4,714,564,096-byte controller observation was not used as an
   override, and no force, rename, guard bypass, or second heavy body is shown.

4. The genuine manager disk trace begins before the worker, spans queue,
   running, pass, and terminal states for this exact service, samples at about
   five-second intervals through terminal, and remains above both the 5 GB
   admission and 4 GB stop floors. No stop request occurred.

5. The dispatcher did not emit `disk-trace.tsv`. This is a bounded limitation;
   the manager trace is retained and used directly, with no copied or
   backfilled samples.

6. Source custody is clean and unchanged for the qualified Agent/Runtime/App/
   Composition tuple. Manifest, runmanifest, JUnit, profile, Node, launcher,
   registry, and publication-receipt checks are consistent. Historical
   10086/19479/8912 and original3/correction/App0254 evidence is not retargeted.

7. Scope is intentionally finite: this review credits only the one selected
   CLI proof, not the other P4 lanes or a product-suite qualification.
