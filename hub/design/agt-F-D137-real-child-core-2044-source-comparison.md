# Source comparison

The authorized request carriers were used exactly as named:

| Component | Requested commit | Requested tree | Request result |
|---|---|---|---|
| Agent | `a4e016b6a9f91fbe372672bdcf382c630bf59186` | `60d45288145414ee4702fcce61af7c7810c2a3df` | child preflight passed; core not reached |
| Runtime | `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` | `de2954a0ceadb4455903d9abdfec3b773318a50f` | child preflight passed; core not reached |
| App | `d8a1cd40b866c49c0ab415682391f0ec87a7a8e7` | `dd2afd6c5c7a1ac73feaac4390cc64d7f31fe7b9` | core binding not reached |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | core binding not reached |
| Remotion | `819acf` | `b01dca9b3b24f54093c20b7c5657316f997725db` | core binding not reached |

No candidate retarget, alternate checkout, overlay, or fallback interpreter was used.
