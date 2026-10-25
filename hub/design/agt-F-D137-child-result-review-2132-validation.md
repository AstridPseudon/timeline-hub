# D137 custody review validation

Verdict: `PASS_EVIDENCE`.

The review is evidence-only. It did not import the child, replay controls, submit a body, run tests, or request another child.

## Checks

- `bash -n /home/user/work/wt/agt-pin-a4e016b6/tools/p4-d73-pinned-launch.sh`: PASS.
- Read-only AST parse of the launcher’s two embedded Python heredocs: PASS (`2` blocks).
- `python3 -m json.tool` on `cas-installation.json`, `cas-source-manifest.json`, and the registered `.bench-owner.json`: PASS.
- `preflight.json` is key/value text rather than JSON; `installed-child.json` and `service.json` are empty. These are recorded as exact source-packet gaps, not repaired or treated as service results.
- `git show cf80cfcb918ee9e311a294fb7291ad5e11c48d0b:ops-child-custody/make-child-venv | sha256sum`: `f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f`, matching the installed regular `0755` target.
- Protected helper hashes match the CAS receipt: `bench_store.py` `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2`; `verify_dependency_seed.py` `116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2`.
- Frozen Agent, Runtime, App, and Composition checkouts: clean, with recorded SHA/tree pairs matching the manifests.
- Review worktree: clean. No product, test, generated, pin, schema, kit, dependency, or configuration file was changed.

## Result classification

Normal child provisioning is supported by the passed provision report, registered key/owner record, source commits, lock identity, and actual module-origin record. The shared schema is absent from the registered child site-packages.

The corrected D73 manifest names the historical `/home/user/work/venv-agent/lib/python3.13/site-packages` schema path. The frozen launcher checks that path exists but then resets `PYTHONPATH` to only the Agent and Runtime checkouts at launcher lines 128–129 (and does the same for the body at lines 149–150). Its preflight imports `banodoco_timeline_schema` at embedded line 17 and fails with exit `1`, exactly as retained. This is a launcher/manifest binding failure, not evidence that normal child provisioning failed.

The positive path therefore has no command/body record, and the poison path has no request-id/runmanifest/preflight/body record because it is rejected at the SHA guard. No `agent-core-full` service or ship-grade core PASS exists. The shell preparation failure for the absent rehearsal stub is separately retained in the author log and is not conflated with either admission result.

No targeted tests were run, as required for this read-only proof-source review.
