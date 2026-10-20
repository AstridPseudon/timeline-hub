# Corrected Main014 full blocked by central storage
Corrected candidate6e845a/tree7f11d7 is targeted-green and its ONE full is authorized, but free space is7.35GiB,694337536 bytes below the real8GiB floor.
Owned worker exhausted compact-scratch/sweep-tmp and recycled eligible own worktrees; report: workers/rt-m4-corrected-full-owned-headroom/report.md.
Preserved active snapshots, leases, pinned checkouts, shared dependencies, receipts and all reports; no floor bypass or full retry.
Recommended action: central owner release at least1GiB, preferably3GiB, outside Runtime-only cleanup scope; Agent environment move may supply this. Gate worker is waiting and can start without another approval once real floor passes.
Not covered because: safe self-service Runtime cleanup is exhausted; remaining shared or peer-owned storage is outside this manager's cleanup authority.
Rule that would let me decide next time: centrally owned bounded storage-release queue for gate workers after own safe cleanup is exhausted.
