# OPS finite pin headroom — manager flat

- Result: `eligible_pins=[]`; no pin is cleared for recycling.
- Snapshot: 2026-10-25T14:54:54Z; source-only Composition head `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`.
- Scope: exactly `agt-pin-16bbd56d`, `agt-pin-82b6d00d`, `app-pin-0b6cee26`, `rt-pin-1daca2a3`, and `rt-pin-d4f496ec`; read-only metadata and target-path process guards only.

## Measured bytes

| Pin | Bytes | HEAD/tree exact | Clean | Current integration? | KEEP |
|---|---:|---|---|---|---|
| `agt-pin-16bbd56d` | 116,984,543 | yes / `70fcd38844e7d93cdf97e4aebaf248d3736a312a` | yes | no | yes |
| `agt-pin-82b6d00d` | 120,070,782 | yes / `019ae9944d5f445776bd19c7d0c441190955c1a3` | yes | no | yes |
| `app-pin-0b6cee26` | 150,195,681 | yes / `9456c9edf3229ddcfd824b0f626516f2c602ccfa` | yes | no | yes |
| `rt-pin-1daca2a3` | 22,821,041 | yes / `a522511414947e48e317a5e5c2103483b121a750` | yes | no | yes |
| `rt-pin-d4f496ec` | 6,655,855 | yes / `1d3e06f4d59ed6d459646d24ab185c36eb5be075` | yes | no | yes |
| **Total** | **416,727,902** | | | | |

Filesystem availability was 4,841,418,752 bytes, below the 5,000,000,000-byte light-admission threshold.

## Guard result

- `/proc` target-path checks across `cmdline`, `cwd`, `environ`, and file descriptors: external matches 0; unreadable fields 0; host scope certified.
- Pending/running queue refs: 0. Running test services: 0. Lease/ACTIVE target refs: 0.
- One historical `tests/suites.conf` registration references `rt-pin-d4f496ec` at line 156; no running service uses it.
- Active external worker: unrelated `rt-OPS-Farm-ownership-census-1457`, with no target ref. This audit worker’s own marker was explicitly excluded.
- Manager STATUS refs are historical abbreviated SHA citations only; no current physical-path refs.

All five `KEEP` markers have explicit purposes (D124/D115/D73/D86/D118). The manager must decide completion and remove `KEEP` only after all guards clear, then use the normal recycle route. No mutation, retirement, sweep, acquisition, or retry was performed.
