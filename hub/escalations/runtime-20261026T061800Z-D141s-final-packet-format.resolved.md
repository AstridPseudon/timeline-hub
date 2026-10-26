Resolved by main 2026-10-26T06:18:28Z.
- D141s-c (06:18Z): the paired App kit is DROPPED now under the existing D141s rule. No schema2 derivative, no adapter, no further round. Reasons:
  (1) Its controls can't read the genuine schema3 packet without a new format step, which would start another loop.
  (2) It would not unblock anything now anyway. App is at about 4.38 GB, below even the pair's 4.6 GB admission.
  WIP 14822e88 (tl/rt-OPS-D141s-final-literals-0601), App packet 0545 and source 2733c720 stay retained as they are, uninstalled. App's journeys (P1, P2-six, P3, popup ADD) run under the normal floors: the D89d measured floor per body kind where retained receipts exist, otherwise D89. They wait for headroom, which in practice means the owner's hub-repack approval. Runtime's live kit 56f2/f674 is unchanged.
