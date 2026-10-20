# RT-M2 original native authoring seam report

## Result

No current Agent command can author the accepted RT03 carrier. The one
concrete missing boundary is a closed, occurrence-owned extension to an
existing native media/placement command and the existing recorder so it can
write `provenance.astrid.timeline_reference` with the already-agreed v1
vocabulary. Runtime already preserves occurrence provenance, but cannot derive
the original `timeline_references` projection without that native authored
carrier.

Peer request: [PEER-REQUEST-agent.md](PEER-REQUEST-agent.md).

## Evidence trace

- Contract read: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-rt03-film-reference-role-carrier-contract.md`.
  It fixes `version: 1`, exact `reference_id`, `role: "source"`, and an
  existing occurrence-local internal registry `asset` alias; Runtime derives
  object custody from the accepted dependency/selection closure.
- Agent registry: `/home/user/work/agent/astrid/sdk/timeline/commands.py`.
  `operations()` has 20 native operations and none named or targeted for
  reference/provenance authoring.
- Agent capture paths: `native_occurrence_media_commands.py` only creates or
  swaps occurrence-owned clips and registry media bindings; `native_placement_commands.py`
  creates/unplaces media expressions; `_shot_commands.py::shot_set` only writes
  shot name/settings; `_clip_scalar_commands.py::clip_set` only targets a
  parent/occurrence clip. None writes occurrence `provenance`.
- Runtime custody: `runtime_protocol/service.py::_normalize_occurrence`
  validates and retains an opaque provenance object; `runtime_protocol/timeline_commit_store.py`
  verifies and persists that occurrence field. This is retention/acceptance
  custody, not an Agent authoring seam or a timeline-reference projection.
- Original positive remains strict/open at
  `tests/test_runtime_exact_idempotency.py:81-122`, marked
  `xfail(strict=True)`. Its direct legacy writer asserts durable creation,
  restart retry, changed-payload conflict, different-key overwrite refusal,
  and durable `role == "source"`.
- Separate direct-writer refusal controls are in
  `tests/test_timeline_reference_authority.py`; catalog CRUD controls in the
  same file are intentionally not treated as this positive.

## Tests and probes

- Pass — read-only Agent registry probe:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-agent/bin/python - <<'PY' ... operations() ... PY`
  Output listed all 20 operations and `occurrence provenance candidates: []`.
- Pass — direct service refusal controls:
  `ASTRID_CHECKOUT=/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/tests:$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_reference_authority.py -k 'test_service_reference_writers_refuse_before_lookup_or_replay'`
  Result: `24 passed, 121 deselected`.
- Not qualified locally — original strict positive:
  `... pytest ... tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`
  could not reach its expected `ApiError` because this sandbox forbids the
  daemon socket (`PermissionError: [Errno 1] Operation not permitted`).
- Central targeted request was attempted for the two original files. The
  service lacked `ASTRID_CHECKOUT`, yielding `2 passed, 1 xfailed, 145 errors`;
  the `1 xfailed` preserves the open original positive, but the run is not a
  clean qualification result.
- No full suite, renderer, browser, release, product edit, source-contract
  generation, or implementation was run.

## Decisions / blockers

No product decision was changed and no implementation was attempted. The
boundary is blocked on Agent peer agreement for the existing-carrier recorder
extension described in the peer request. Do not substitute project catalog CRUD
or fabricate accepted history. After agreement, Agent should implement the
closed carrier and Runtime should add the actual-provider acceptance witness
while keeping the original positive and direct-writer refusal separate.
