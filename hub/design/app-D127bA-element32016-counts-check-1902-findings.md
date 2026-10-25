# D127bA independent counts/privacy check

Verdict: **PASS**, with the bounded result `PASS_WITH_EXACTMISSING`.

- The current request has an honest sample population of 828 and 15 lost samples; loss is reported separately.
- The exact available descendant and parent-to-child edge row sets are both empty. No sampled chains or authentic full counters were retained, so no inclusive, self, edge, root-membership, outside-root, unrepresented, truncated-chain, or top-25 rank value is claimed.
- Inclusive counts are not summed against 828: frame membership overlaps across samples. The available exact chain coverage is 0/828, and ranking coverage is unavailable.
- The retained request-1 evidence has 57 lifecycle events, 5 thread dumps, and 65 frame records, but only summary/event structure; no call count, invocation count, or wall-time value is inferred.
- The documented rule preserves frame and parent-to-child edge identity, deduplicates each once per sample, and uses the innermost relevant frame for self counts. No recursion or line identity is reconstructed without chains.
- The actual count ceiling is 828; with zero exact rows, no observed count exceeds it.
- Public artifacts parse, obey the safe count/limit field allowlist, contain no private custody or sensitive transport fields, and remain mode 0600. Raw source artifacts remained mode 0600 with unchanged hashes before/after the check.

No product, test, generated, or repository files changed. No test suite was run because this was the authorized data-only quick check.
