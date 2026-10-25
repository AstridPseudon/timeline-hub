# D137 installer handoff

Review decision: source-security PASS; acceptance remains UNVERIFIED.

The fixture E2E gate is intentionally `WITHDRAWN`, its result is `NOTRUN`,
and `production_install=false`. The manager-only route must receive a fresh
decision JSON with these exact fields:

```json
{
  "authorization": "D137",
  "fixture_e2e_gate": "WITHDRAWN",
  "e2e_result": "NOTRUN",
  "e2e_pass": false,
  "install_route": "CAS_MANAGER_ONLY",
  "production_install": false,
  "candidate_sha256": "4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36",
  "candidate_bytes": 75503,
  "source_commit": "0c4170e42d2ff435ea855a54c940299619f6a285",
  "reviewed_installer": "installer1826",
  "decision_path": "/approved/gates/d137-decision.json"
}
```

Runnable manager command, only after manager acceptance and from the reviewed
Composition checkout:

```sh
ORCH=/approved/orch/root \
SOURCE_CHECKOUT=/approved/composition/checkout \
TMPDIR=/approved/private/tmp \
D137_DECISION=/approved/gates/d137-decision.json \
bash ops-child-custody/install-prep/apply-reviewed-maker.sh
```

Installer-required preimage: `0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`,
68,351 bytes, mode `0755`. Protected helper pins remain
`bench_store.py=123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2`
and
`verify_dependency_seed.py=116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2`.

The route must preserve physical owned paths, regular single-link mode-`0755`
target/preimage checks, no-follow/no-clobber backup creation, descriptor-bound
receiving lock, target identity CAS, atomic rename, protected-helper readback,
and `cmp` verification. Do not run a whole-make fixture, issue a child
request, acquire packages, or use an alternate installer.
