# D111a corrected distribution

Scope: exact final 0827 run `1792917417224776367-32439` only. The 0843 output is preserved; this is a corrected own output.

The durable profile stores aggregate frame occurrences, not the per-sample stack matrix. The table therefore reports a corrected at-most-once membership cap and marks exact distinct membership `EXACTMISSING`; recursive occurrence totals are retained only as audit inputs. No frame cap exceeds 235 and no fraction exceeds 1.

Request wall: 6179.286447 ms. Samples: 235 × 20.0 ms = 4700.0 ms nominal, 76.06056201% of actual request wall. Sample offsets span 15.136463–6166.091824 ms; lost samples=0. This is uneven sampling coverage, not continuous coverage. Observer CPU was 141.658980 ms (2.29248120% as a scale comparison), measured only while the request was active.

## Top 10 normalized stack-membership caps

| normalized frame | aggregate recursive occurrences | membership cap (≤1/sample) | estimator (ms) | share of whole request wall |
|---|---:|---:|---:|---:|
| `<stdlib>/copy.py:deepcopy` | 1083 | 235 | 4700.0 | 76.06056201% |
| `<stdlib>/copy.py:_deepcopy_dict` | 649 | 235 | 4700.0 | 76.06056201% |
| `<runtime>/runtime_protocol/service.py:wrapped` | 468 | 235 | 4700.0 | 76.06056201% |
| `<runtime>/runtime_protocol/timeline_commit_store.py:evaluate` | 297 | 235 | 4700.0 | 76.06056201% |
| `<stdlib>/copy.py:_deepcopy_list` | 292 | 235 | 4700.0 | 76.06056201% |
| `<runtime>/runtime_protocol/server.py:_dispatch` | 235 | 235 | 4700.0 | 76.06056201% |
| `<runtime>/runtime_protocol/server.py:_route` | 235 | 235 | 4700.0 | 76.06056201% |
| `<runtime>/runtime_protocol/server.py:_timeline_commit` | 235 | 235 | 4700.0 | 76.06056201% |
| `<runtime>/runtime_protocol/server.py:do_POST` | 235 | 235 | 4700.0 | 76.06056201% |
| `<stdlib>/server.py:handle` | 235 | 235 | 4700.0 | 76.06056201% |

Exact distinct per-sample frequencies are unavailable from this retained input because the sampler serialized only aggregate occurrences. The numeric cap is the safe corrected wall estimator; it is not relabeled as an exact frequency.

## Union and named operations

The `deepcopy`/`finite_json` union cap is 235/235 samples, 4700.0 ms, 76.06056201% of whole-request wall. It is capped once at the sample count; the two overlapping shares are not added.

| operation | calls | inclusive CPU (ms) | inclusive wall (ms) | self CPU (ms) | self wall (ms) | bytes |
|---|---:|---:|---:|---:|---:|---|
| `deepcopy` | 657 | 3674.464272 | 3966.175982 | 3674.464272 | 3966.175982 | EXACTMISSING |
| `finite_json` | 41 | 1390.964100 | 1501.569942 | 1390.964100 | 1501.569942 | EXACTMISSING |
| `RequestCommitPort._read` | 11 | 3911.438917 | 4226.860125 | 42.453340 | 53.702374 | EXACTMISSING |

Bytes are `EXACTMISSING` for all three operations. Captured request/document/history sizes are metadata only and are not substituted for operation bytes.

## Verdict

`NOAUTHOR`. No causal dominance or majority cost is proven. Inclusive samples/timers overlap; the named timers were recorded under diagnostic `sys.setprofile` hooks, so they are not uninstrumented production wall attribution. No source/product optimization or new measurement was performed.

The exact runtime/Agent heads and file hashes, JUnit identity, C0-shaped request/reply key checks, parser hash, and arithmetic invariants are in `D111adistribution.json`. Raw request/reply/auth/keys/private URLs/stacks are not exported.
