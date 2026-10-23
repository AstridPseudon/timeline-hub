# Runtime OPS-bench-store install receipt

Conditional atomic installation completed at 2026-10-23T20:08:00Z after independent 1947 PASS of the exact 1941 source (`6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8`).

Installed live hashes:

```text
bench_store.py       6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8
test-run             f599c5ad7bf3cd61aeb01791d903ce6edfa87d5d04a39b3ebb630b3517b17ff4
make-child-venv      89d82618c6c67819e40cc73d32b6d1c372f95889761d5170bb1af3a83dc5fcff
make-runtime         99cca067330fd87e1f8c475045ab8282e944b2455e25d44d4c6072e77e9e4e28
request-child-venv   72cafb3a5ec343f648a0e41d59a51e7c803ee51b4d04a394dc2010df828bd731
request-runtime      f13a1d073699712ccfb05e8463ad97ff69dc210a2617f2c9e0140a242591f7b1 (unchanged)
```

All live files are regular root-owned `0755` nonsymlinks. Existing backups, UTC `20261023T200625Z`, were preserved for `test-run`, `make-child-venv`, `make-runtime`, and `request-child-venv`; the absent helper had no predecessor. Dispatcher `f18bc20b…`, retire handler `954d5d87…`, and retire requester `21f61833…` remained unchanged.

Idle proof passed before every replacement: two snapshots plus an immediate check, no non-hidden pending records, no pending operation types, no test `running`/`queued` state, no running markers. Final idle checks passed at 20:08:22Z and 20:08:27Z. The bounded private requester→exact dispatcher→maker smoke passed 4/4 (2 normal, 2 `env -i`), with no network/installer/daemon/real-store activity.

Runtime stayed clean at committed HEAD `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`. Read-only hub observation did not show a new publication within 60 seconds; manager must publish the KITCHANGE and obtain remote ACK. No direct hub/kit/Git action was taken. This receipt is not real-bench or freed-space proof.

Full details and exact backup hashes are in [worker report](../workers/rt-OPS-bench-store-install-2003/report.md).
