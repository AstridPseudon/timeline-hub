# Runtime raw-audio port final review

## Decision

**REJECT** for merge at candidate `ab4c26d12f1f71e3540d3e118fdff7771bd2c73d`.

The closure, project/managed-object authorization, CAS hash/size check,
unsupported-WAV omission, request memo, acceptance recheck, and ledger-first
retry ordering are directionally correct. The candidate still has a
merge-blocking read-TOCTOU in the metadata reader.

## Finding

`runtime_protocol/timeline_commit_port.py:892-905` calls
`_verify_child_object_bytes`, which hashes and fstats one descriptor, then
opens the CAS pathname again with `self.cas.open` for `wave.open`. A pathname
replacement between those operations lets WAV metadata come from bytes that
were never hashed. I reproduced this without changing the recorded object
row: after the verification callback returned, changing only the WAV data
chunk length made `media_info` return `duration_seconds: 2.0` for the original
1.0-second object. The reproduction used a private temporary realm and
restored no worktree files.

The later memo recheck at `:428-430` usually refuses a tampered object that
remains changed, so the existing acceptance test catches the persistent case.
That does not make the initial read safe: the proposal requires inspection of
the verified bytes, and a provider can observe/record the unverified result
before acceptance. Fix by verifying and parsing through the same already-open
descriptor (including stable identity/size/hash checks), or by an equivalent
single-read verified-byte path; retain the acceptance recheck.

## What passed

- `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_raw_audio_port.py tests/test_timeline_commit_port.py tests/test_timeline_commit_contract.py` — **69 passed in 39.85s**.
- `/home/user/work/venv-runtime/bin/python -m py_compile runtime_protocol/timeline_commit.py runtime_protocol/timeline_commit_port.py tests/test_timeline_raw_audio_port.py` — passed.
- `git diff --check HEAD^ HEAD` — source diff is clean except the known accidental trailing blank line in `design/runtime-raw-audio-port.md`; that documentation hygiene issue is separate and should be cleaned before merge.

The focused suite covers exact-base closure refusal, foreign-project refusal,
unsupported WAV omission, persistent tamper refusal, and accepted-retry
ledger-first behavior. No full/live/browser suite was run, as directed.

## Compatibility and scope checks

`contract/manifest.json`, `contract/artifacts.json`, generated clients,
`SCHEMA_DIGEST`, and `runtime_protocol/timeline_commit_provider.py`'s fixed
`astrid-v1`/interface-version-1 provider startup checks do not include this
private port method. The Runtime package `__init__` and Agent timeline public
`__all__` exports do not expose it. No public route, DTO, generated schema,
generation/variant adoption, inline duration, whole-film read, or new ledger
was added. The accepted-retry lookup occurs before `port_factory`, so it does
not reread raw media.

## Limitations / next steps

This is a source-level Runtime review only. The native legacy trim positive is
still **OPEN** pending the paired Agent adapter and an integrated proof; this
review does not certify it. Correct the single-descriptor read race, rerun the
focused Runtime tests, and obtain the paired Agent/Runtime evidence before
reconsidering approval.
