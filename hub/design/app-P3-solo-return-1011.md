## Report

Implemented P3-only caller repair in [caller-publication.py](/home/user/work/wt/app-P3-solo-return-1011/caller-publication.py) and [caller-custody.json](/home/user/work/wt/app-P3-solo-return-1011/caller-custody.json).

- Uses authentic dispatcher meta/report/queue facts and kept checkout `/home/user/work/wt/app-pin-82cb5c00` at `82cb…`.
- Removed invented pre-request source/snapshot receipt requirements.
- Preserved P2 and all other rows byte-identically.
- Added `dependencies` to the C0 wire inventory.
- Replaced literal `argc=2` claim with executable `bash -c` zero-/one-argument proof.
- Candidate: P2 `60` fingerprints, P3 `106`; outsiders `249`, SHA-256 `1340ef47…`.
- P3 candidate row SHA-256: `23226c27…`.
- Service snapshot and daemon identity remain honestly `UNKNOWN` until normal test-run execution.

Checks passed:

```text
python3 -m py_compile caller-publication.py
python3 -m json.tool caller-custody.json
/bin/bash -n generated P3 inner/outer scripts
source/target/body/stage/export/import/graph/custody refusal checks
positive/negative bash-c argument proof
git diff --check
```

The final preparation rerun was prevented by an external `suites.conf` change reducing it to 248 lines; I did not modify it. The exact 249-outsider candidate was generated and independently verified before that change.

No browser, service, backend, build, provisioning, or full suite was run. Commit message and `DONE` marker were written.