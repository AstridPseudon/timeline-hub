# Runtime RT08 carrier/private-version pair

## Result

Composed the reviewed Runtime carrier and secondary-ID fix onto current Runtime
integration safety (`388eff4`, tree
`708df14c75ef739a2c6130ca39f9e67b2758a571`) in worker source
`/home/user/work/wt/rt-m2-carrier-private-version-pair`.

Preserved the carrier port/materialization path and opaque secondary IDs. The
composition also retains the current fresh-bootstrap preflight, strict JSON
scope reader, and empty-shell adoption guards. No DTO, version field, inline
authority, or guard relaxation was added.

The private Agent source is exact commit `3730d0bd51686a1692450359482205df64dcc839`,
tree `3892a10bcffa9bf520b4c79591637cf3259d6724`, with schema SHA-256
`f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f` (48
definitions). The generated private Runtime resource/client metadata bundle
matches that schema:

| Artifact | SHA-256 |
| --- | --- |
| `runtime_protocol/timeline_commit_port.py` | `28968f683c064af54da4b767618880781a6ec66e80586d462b8b7e2b1f96ee86` |
| `runtime_protocol/timeline_commit_store.py` | `11252cf2cb3dc5c8fc83cb447d238cd3f7b64a4051ecd1b6086444555fa278a2` |
| `runtime_protocol/timeline_materialization.py` | `92ec9b7f105d5e0fd1c5f9e9f2a4602ee3dd005365a570e7ba91a573bb8b31fb` |
| `runtime_protocol/service.py` | `e006d1d2096bda9eac6a32ad099113dfe3e9e0ca75b76d69e9407ebdb7c6c1f3` |
| private command schema | `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f` |
| `runtime_protocol/schemas/timeline-commit-bundle.json` | `3b17151af11c35460aa54d9732f3235bd136dfa7622b795a68a9da622dfb4425` |
| `contract/artifacts.json` | `9e5915b912b4fb49ff7cca2bc4d43c25473a55a9a5198b562f5276058032dc62` |

The public Agent fixture remains unchanged at SHA-256
`a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-m2-carrier-private-pair-final-focused-2 tests/test_timeline_materialization_join.py tests/test_timeline_materialization_authority_review.py tests/test_timeline_projection_ownership.py tests/test_timeline_projection_occupancy.py`
  — **210 passed, 3 deselected, 1 strict xfailed** in 52.39s. The xfail is
  the public-013 typed-item-claim refusal control, retained until public
  adoption.
- Central named integration request
  `rt-m2-carrier-private-version-pair-occupancy-integration-1020140550-12817`,
  explicit files `tests/test_timeline_materialization_continuation.py
  tests/test_timeline_projection_occupancy.py` — **18 passed, 17 deselected**
  in 21.62s. This covered bounded real-provider continuation/restart/ACK and
  own-slot/global-item occupancy controls using the current Agent integration.
- `.../python -B scripts/artifact_manifest.py --check` — passed.
- Private bundle equality check — passed: the packaged edit-command resource is
  byte-equal as JSON to the exact private schema.
- Compatibility checks against Runtime 0.2.3, Runtime 0.2.10, Agent S1, and
  public Agent S2 — zero errors.
- The unchanged generator guard reports five explicit errors against the
  ancient Runtime 0.2.2 floor (`AnchorIdentity`, `EntityRef`, `ScopedId`,
  `TargetKey` patterns and the `track.set` union). The guard was not changed;
  the three corresponding checks are strict xfails in the private candidate.
  This is the exact floor limitation, not a weakened check.
- `git diff --check` passed. Repository-wide Ruff was not clean because the
  touched Runtime/test files already contain broad pre-existing lint findings;
  no formatter rewrite was applied.

## Review and limits

A PEER REQUEST with the exact source/tree/digests was appended to the Agent
INBOX and `design/runtime-coordination.md` at 2026-10-20 13:54Z. No Agent
counterpart review response was present at final readback. Therefore exact
paired native qualification remains held. The central occupancy run used
`/home/user/work/agent` current integration, not the frozen Agent3730 archive;
the exact private schema/resource checks were local. No full suite, browser,
release, pin, freeze, activation, merge, or public adoption was performed.

Next step: obtain the Agent review ACK for this composed Runtime counterpart,
then rerun the bounded native pair against the exact Agent3730 source before
any adoption decision.
