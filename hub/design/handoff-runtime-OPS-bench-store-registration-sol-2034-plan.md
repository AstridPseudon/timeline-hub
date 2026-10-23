# OPS-bench-store registration source/cutover plan

Source only; live exact-seven operation remains STOPPED.

API: Store.unregister(request), CLI `bench_store.py --root ROOT --tests-dir TESTS unregister --request JSON`. Request is `{names: {exact_name: {suite_sha256, env_sha256}}, suites_sha256}`. All seven original identities must match the 1841 evidence. No path/key adoption, eviction or legacy directory access. Journal uses existing pending.json with unregistration kind; recovery rolls forward the exact projections, with no payload victims.

Cutover: a newly initialized store may establish a stable registration flock only while all seven suite/env identities are absent. Its inode is retained in the existing index. The test-run suite lease takes that shared flock before launching a target suite; unregistration/recovery require its exclusive nonblocking acquisition under the store mutex. Missing birth custody on an existing store is UNKNOWN and refuses. There is no stamp-idle flag, retroactive bootstrap, /proc scan, or new ledger. The private fixture creates its own exact seven inputs after this controlled boundary and exercises real inherited descriptors.

Remaining live seam: installed core6d9368 has no registration birth custody, and test-run f599 never leased these unmanaged names. The patched caller supplies prospective preleases only; a separately reviewed owner/supervisor cutover must account for all pre-existing unleased runs before any migration of existing-store custody can be designed. This packet intentionally supplies no migration or live cleanup command. Unknown stays refused.

Validation: finite stdlib fixture for exact7, protected/outside bytes, legacy directories, lease/unknown/stale/ref/race/symlink/crash/recovery/shared-key; normal and env-i private CLI/caller shape, ruff/compile/bash syntax, private patch replay/cmp, installed six hashes and clean Runtime. No broad/full suite. Independent Luna review, then separately reviewed install/caller-smoke gate. C0v2 and frozen34e untouched.
