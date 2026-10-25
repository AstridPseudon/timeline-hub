# Retained descendant aggregation

Status: `EXACTMISSING`.

The approved current request has a sample population of 828 and 15 lost samples. Its retained artifacts contain 57 lifecycle events and thread-dump text (5 thread dumps, 65 frame records), but no original per-sample call chains and no authentic full counters. The existing top-frame summary was not used to reconstruct descendants.

Exact descendant rows under `_timeline_commit` are therefore unavailable. No inclusive count, self count, rank, root-membership, outside-root bin, or truncated-chain bin is inferred. The exact available row set is empty.

If sampled chains or authentic counters had been retained, normalization would preserve each original frame identity while reducing paths to Runtime/Agent/stdlib/package-relative module paths; private host/project prefixes would be removed. Each frame and parent→child edge would be deduplicated once per sample before inclusive counting, and self count would use the innermost relevant frame. Inclusive sums would not be forced to equal the population because samples overlap across frames.
