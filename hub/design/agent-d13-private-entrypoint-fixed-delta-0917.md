# APPROVE — Agent D13 private entrypoint fixed delta 0917

Review target: the corrected 0908 profile, not the 0851 profile:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b`

Selected interpreter:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/bin/python`

## Decision

**APPROVE.** The two concrete 0901 REQUESTCHANGES findings are closed. The corrected profile is a private, internally coherent installed set for the stated custody boundary. No product source, wheel payload, dependency constraint, version, or approved source identity changed.

## Exact identity and hash inventory

- Agent source ref `f4edcb4bce531be3ea8c6389069429175b048c2a`, source tree `1cbd18011b56c41a5ef31f155c15bd373c1208e`; `astrid==0.1.0`; wheel SHA-256 `7455220aa1d3f8c67c7c9cee0f7a6571fb4f51882eca2543ead25943eebd185a`.
- Runtime source ref `b92d3e7a05eec65c142294ef4873edd059e9b31d`, source tree `6abc2f117391de8e7e35c0283f575a002199894d`; `astrid-runtime==0.1.0`; wheel SHA-256 `12df54644e1acac46b9c396135ef345808a98515965f1f12f479f32adf3c9b0a`.
- Runtime client source ref `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`, source tree `d3a290b407fa61e6ab2d476f50c068073f70df00`; `astrid-runtime-client==0.2.14`; wheel SHA-256 `567605b13254f88ddeddad7b570553a2c50b5092908e6c4153553f9867e37254`.
- Dependency constraints: 164 entries; SHA-256 `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`.
- Selected additional versions: `banodoco-timeline-schema==0.0.2`, `numpy==2.5.2`, `opencv-python-headless==5.0.0.93`, `pillow==12.3.0`, `pyyaml==6.0.3`.
- `venv/pyvenv.cfg` SHA-256 `b66e1f96f9e5e9e089e1a5adc4e5eab65b6340d1ea1b1f849ad2a182f284aed0`.
- `profile/astrid.json` SHA-256 `570eb14172a416765d256d783a84826ce68a3f53dc8819e42bba066ca3866d17`.
- Corrected `metadata/wheels.sha256` SHA-256 `ec1c8806ca86ba7d364d46c23eae7be4a361ea5b20911a12e1dbae5afbec211e`; its three lines match the wheel hashes above. The metadata hash changed only because the absolute wheel paths and Agent digest were corrected from the stale 0851 staging record.

## 0908 delta audit

- The repaired root is independent: zero symlinks and zero files with link count greater than one. The three interpreter files are regular copies and resolve inside the selected 0908 `venv`.
- `venv/pyvenv.cfg` now records the actual 0908 private venv and `/usr/bin/python3.13`; it no longer records `profile-staging`.
- All 58 changed executable entrypoints now contain the selected private interpreter. The changed set is: `agent-detector`, `astrid`, `astrid-credential`, `astrid-runtime`, `astrid-runtime-protocol`, `astrid-tools`, `astrid-upgrade`, `astrid-with-credential`, `cffi-gen-src`, `coverage`, `coverage-3.13`, `coverage3`, `cpuinfo`, `detect-installer-test`, `distro`, `dmypy`, `dotenv`, `email_validator`, `f2py`, `fastapi`, `fonttools`, `httpx`, `httpx2`, `idna`, `inv`, `invoke`, `jp.py`, `jsonschema`, `keyring`, `manual-tests`, `markdown-it`, `mypy`, `mypyc`, `normalizer`, `numpy-config`, `pip`, `pip3`, `pip3.13`, `py.test`, `pyftmerge`, `pyftsubset`, `pygmentize`, `pyproject-build`, `pytest`, `runpod`, `runpod-lifecycle`, `scenedetect`, `slowest-tests`, `stubgen`, `stubtest`, `tqdm`, `ttx`, `typer`, `uvicorn`, `watchfiles`, `watchmedo`, `websockets`, `wheel`.
- `activate`, `activate.csh`, and `activate.fish` now select the 0908 private root. `profile/astrid.json` selects the private site-packages for both checkout fields and the private venv for `runtime_environment`.
- The installed entrypoint/config/import surfaces contain zero `profile-staging`, 0851/0901, shared venv, Agent checkout, or Runtime checkout references. Source test fixtures retain their pre-existing ordinary `/home/user/work/...` literals, but those are not installed authority and are absent from the installed package/entrypoint/config scan.
- Agent RECORD changed only for its five generated console-script rows plus its installation `direct_url` row. Runtime RECORD changed only for its two generated console-script rows plus its installation `direct_url` row. The client `direct_url` row changed to the new profile wheel path. No product package RECORD hash changed.

## Byte, RECORD, version, and origin evidence

- Old/new source trees compare cleanly after excluding only generated build/cache paths: 3,268 source files on each side and identical aggregate hash `e3af879e551f51f1ae5c26593e9ad29765b6bebf05292204ad60d4cb90cb8289`.
- Old/new Agent, Runtime, and client wheel files are byte-identical to the three hashes above. Wheel member sets are unchanged; installed comparisons covered 1,391 Agent, 80 Runtime, and 7 client non-RECORD wheel members with zero mismatches.
- Full direct installed RECORD read audit: 166 RECORD files, 16,139 rows, zero missing files, zero size mismatches, zero digest mismatches, and zero paths outside the venv root. The 16 nested setuptools-vendor RECORD files are outside this direct 166-distribution inventory and were not counted as additional installed distributions.
- Neutral isolated import probe was run from `/tmp` with `env -u PYTHONPATH -u PYTHONHOME <private-python> -I -B`. Seven imported origins (Agent child/host/SDK, Runtime, Runtime protocol and platform, and client) all resolved under the 0908 private site-packages; `sys.path` contained only Python stdlib entries plus that private site-packages directory. The approved eighth rendering action origin was checked by filesystem resolution without importing its guarded executable body.
- The selected installed versions and the three `direct_url.json` records agree with the wheel hashes. The existing coherent installed-set/controller assumption is retained; this review adds no attestation or packaging rule.

## Commands and results

- `diff -qr <0851>/source/agent <0908>/source/agent -x build -x __pycache__ -x '*.pyc' -x '*.egg-info'`: exit 0; source trees identical.
- `sha256sum <0908>/wheelhouse/*.whl`: matched `7455220a`, `12df5464`, and `567605b1` inventories.
- Independent Python wheel/member/installed-byte comparison: all three wheel member sets unchanged; 1,478 installed product members checked; zero mismatches.
- Independent Python direct-RECORD parser: `record_files=166 record_rows=16139 bad=0 outside=0`.
- Independent link scan: `symlinks=0 hardlinked_files=0`.
- `env -u PYTHONPATH -u PYTHONHOME <0908-private-python> -I -B -` neutral import probe: all seven executable imports succeeded and resolved privately; rendering action path resolved privately without executing its guard/body.
- No Agent product tests, launcher execution, daemon, native, HTTP, browser, renderer, install, or full suite was run, as required by the brief.

## Native-proof boundary and next step

This APPROVE is only for the corrected private profile's custody, entrypoint, config, installed-byte, RECORD, version, and neutral-origin boundary. It does **not** claim native dependency readiness, Runtime daemon readiness, launcher behavior, HTTP behavior, browser/render behavior, or product/full-suite qualification. Those remain downstream prerequisites for the separately controlled native proof.

