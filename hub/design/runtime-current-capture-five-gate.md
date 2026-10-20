# Runtime current capture-candidate five-function gate

Date: 2026-10-20

## Scope and source tuple

This is a test-only qualification report for the Runtime base requested by
`rt-m3-current-capture-candidate-five-gate`. No Runtime product, fixture,
test, xfail, DTO, or verifier changes were made.

The exact Runtime source used by the service was:

- commit `601d533d91e3726c4f7ae74723e8eff4adbe2f90`
- tree `a3f42fa9d8187b338e987fdedae50663bfd4e85f`
- `runtime_protocol/capture_validation.py` SHA256
  `572d4c8ec61e2705ce56aa3d5733b500c64ba06b9e5addca885bd457388f6b75`
- `tests/test_capture_candidate_actual.py` SHA256
  `f5a301bb7c691f0fed1977ea91c701e509bd413c88c919c7c177fb3a1e205990`

The current Agent integration checkout observed by the service at test
launch was:

- commit `a760ecca02111b0e0841510926f200e398f3b6cb`
- tree `a990e8da66572da4a91836b2e04e325a408d86d8`
- clean checkout at launch

The Agent checkout advanced from `490c10ac12d55f75d698213487353a7912d33067`
while this request waited in the central queue. The service result's
`external` record and the launch-time checkout identify `a760ecca` as the
qualification source; no frozen Agent substitution or provider override was
used.

The Runtime artifact and compatibility identities were:

- Runtime `contract/artifacts.json` SHA256
  `129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497`
- artifact producer version
  `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`
- Agent `runtime.lock.json` SHA256
  `c2ed617f38bc53e4f90dc082f082d38828d8f68a93e61776300ec7082ef23311`
- Agent lock producer version matches the Runtime artifact version above;
  lock source commit is `2c4ac180c2220bdad966bc01e95ad230e99ce26a`

The loaded Agent provider exposes `capture_candidate_inputs` and
`project_capture` from `astrid/sdk/timeline/commit.py` (lines 655 and 663).
The test's direct imports are:

```text
test_timeline_commit_acceptance.validate_prepared
test_timeline_native_inspection._publish
runtime_protocol.service.RuntimeService
runtime_protocol.snapshot_refs.snapshot_bytes, snapshot_digest
runtime_protocol.store.RealmStore
runtime_protocol.timeline_commit_provider.load_timeline_commit_provider
runtime_protocol.timeline_commit_store.TimelineCommitStore
runtime_protocol.util.canonical_json
tests.test_snapshot_authority_refusal.CAPABILITY, CAPABILITY_DIGEST,
  _assert_refused_without_writes, _digest, _state
```

## Exact service run

Result ID:
`rt-m3-current-capture-candidate-five-gate-marked-integration-1020190218-5523`

The existing Runtime `marked-integration` suite was used. Its command was:

```text
env ASTRID_CHECKOUT=/home/user/work/agent \
PYTHONPATH=$PWD:/home/user/work/agent \
/home/user/work/venv-agent/bin/python -m pytest -q -n 3 -m integration \
tests/test_capture_candidate_actual.py::test_actual_candidate_reaches_claim_and_host \
tests/test_capture_candidate_actual.py::test_original_working_copy_forgeries_refuse_before_writes \
tests/test_capture_candidate_actual.py::test_working_copy_without_candidate_is_admitted_uncertified \
tests/test_capture_candidate_actual.py::test_forged_working_copy_certificate_refuses_before_writes \
tests/test_capture_candidate_actual.py::test_explicit_cas_candidate_is_native_without_binding
```

Service result: **13 passed, 4 failed in 6.97s**, exit 1. The five selected
functions expanded to 17 parameterized nodes. The separate alias/outer
context 18-case matrix and mixed-result probe were not selected. An earlier
queued whole-module request was superseded and is not evidence; it briefly
ran as a separate result and is explicitly excluded from this report.

## What passed and what failed

The 13 passing nodes establish, against the startup-loaded current Agent
provider and Runtime source, that:

- forged working-copy config, registry, and shot-digest changes are refused
  before writes (six nodes);
- a working copy without its candidate is admitted as uncertified, with no
  candidate metadata carried into the claim (two nodes);
- forged working-copy candidate certificates are refused before writes (four
  nodes); and
- an explicit CAS candidate remains native/uncertified without a working-copy
  binding (one node).

The four failures are all the positive
`test_actual_candidate_reaches_claim_and_host` nodes (parent/child changes,
inline/ref forms). Every Runtime and host assertion before the final
`RenderRequest` construction passed: startup provider projection comparison,
candidate authority/binding checks, claim and materialization, immutable
snapshot bytes, dependency expansion, and materialized media bytes. Each
failure is at `tests/test_capture_candidate_actual.py:262`:

```text
AttributeError: 'RenderRequest' object has no attribute 'verified_source'
```

This is the known downstream caller/renderer propagation gap, not a Runtime
candidate-admission or authority failure. Smallest follow-up is for the
separate owner of the Agent rendering contracts/caller path to carry the
existing typed verified-source binding into `RenderRequest` and retain its
strict source checks, then rerun these same four positive nodes. Do not
weaken the Runtime authority comparison, certify from leftover metadata, or
replace the saved/real candidate inputs with a fake fixture.

## Boundaries

This gate does not prove physical frame/audio parity, renderer delivery,
Composition parity, browser behavior, transport, full Runtime health, or
Gate 1/6/7 completion. No full suite, broad capture matrix, browser,
pixel/audio, renderer job, or other capture file was run. Capture admission
remains startup Agent projector comparison plus saved/real working-candidate
authority; claims without that authority remain uncertified/refused.
