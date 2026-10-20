# Runtime preflight ancestry-label correction

This corrects the interpretation in
`runtime-current-main-delivery-preflight.md` without rewriting its historical
snapshot. The original source and tree SHAs remain raw evidence; its three
`0/N; no merge base` labels are misclassifications. A `0/N` count in the
complete histories recorded by the approved contract is consistent with
`origin/main` being reachable from `tl/integration`, not with an absent merge
base.

## Historical snapshot to preserve verbatim

| Repo | `origin/main` (tree) | `tl/integration` (tree) | Original label | Correction status |
|---|---|---|---|---|
| Agent | `96b283d5d6fd8031538f881e486bb2ebf45dce75` (`1e31c58ff3aa35229ba07a8f6bb9c04dc31dd795`) | `79b33f8a1e69b27fd53f3cd5230301b84d0d4ef1` (`6de356067d251e644101da19272c5424fa4f3a68`) | `No; 0/247, no merge base` | Misclassified; historical pair is ancestor-shaped. |
| Runtime | `240d5bb202af709294551045554012f079fd06ca` (`2e77d0df220885e978c5fbdf5d6072292ac07284`) | `e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd` (`94c5ffbc0b636e25475c0f351bfb384dd06ee8ab`) | `No; 0/165, no merge base` | Misclassified; historical pair is ancestor-shaped. |
| App | `86d7def4f7c2b8bc1ae1b50031bfea6750256517` (`1ac90a1e3ca57341537c6e76f2c463c715597b79`) | `22788084f9b9a69322fca1c6aff35d17c5c2c189` (`ecd3d0f250b8ca597a1627832c35003441a79186`) | `Yes; 4/148` | Valid only for this historical pair; not a current-ref classification. |
| Composition | `67b8aa3d0d6831d3e3504a340ff583c3da253707` (`62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`) | `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8` (`13e375534fffd704305eced5686699d2c8c9c948`) | `No; 0/40, no merge base` | Misclassified; historical pair is ancestor-shaped. |

## Append the approved read-only classifications

These are the current-ref results recorded by the approved
`runtime-main-history-delivery-contract.md`; they are not a refresh:

| Repo | Approved refs (`origin/main` -> `tl/integration`) | `merge-base --is-ancestor` | Counts | Shallow boundary | Correct label |
|---|---|---:|---:|---|---|
| Agent | `96b283d5` -> `c73b1ab1` | 0 | `0/249` | none | Ancestor; ranged patch shape. |
| Runtime | `240d5bb2` -> `e2db1e8c` | 0 | `0/165` | none | Ancestor; ranged patch shape. |
| App | `bebadd0e` -> `0d5009e1` | 1 | `6/153` | shallow at `3f05489e` | Divergent; classify truthfully, with no “main ahead” inference. |
| Composition | `67b8aa3d` -> `5a4e9b72` | 0 | `0/40` | none | Ancestor; ranged patch shape. |

The approved delivery shape stays unchanged: produce the linearized binary
patch; use the ranged bundle when the ancestry prerequisite is present and the
full bundle fallback for an unrelated-root snapshot. Do not add a blanket
`is-ancestor` refusal or change the approved script.

An owner-controlled M4 refresh and one four-repo source-freeze manifest remain
mandatory before the final ZIP. No refresh is requested before the M2/M3 gates;
no fetch, source-ref mutation, test, dry-run, full suite, or ZIP is claimed by
this correction.
