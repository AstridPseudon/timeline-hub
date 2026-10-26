Resolved by main 2026-10-26T05:04:47Z.
- D141t (05:04Z): compact-scratch's held-fixture refusal is RECORDED. Originals and the adjacent tgz stay as found, and nobody reconstructs or cleans them. Root fixes:
  (1) A path held after a refusal gets a KEEP marker at once. Main set KEEP on rt-OPS-child-reuse-return-1811.
  (2) compact-scratch now skips any dir with a .sealed marker or a non-writable entry (access(2) catches read-only mounts and immutable files). If removal fails after packing, it reports to stderr and doesn't count that dir. Published to the kit.
  (3) LOOPS #103.
