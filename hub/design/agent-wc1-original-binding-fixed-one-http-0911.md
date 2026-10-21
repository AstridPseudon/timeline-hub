# WC1 original binding fixed HTTP proof

Date: 2026-10-21 UTC

## Source

- Agent commit/tree: `8cad2a95b705862e4d8c6578780cf92a5ed1cc2b` /
  `d0d0edc5e72a081ef5dc4676ad8130c470b98ccc`
- Runtime: `b92d3e7a05eec65c142294ef4873edd059e9b31d` /
  `6abc2f117391de8e7e35c0283f575a002199894d`, clean
- normal95 client: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` /
  `d3a290b407fa61e6ab2d476f50c068073f70df00`, clean
- Central result: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-wc1-original-binding-fixed-one-http-0911-wc1-selected-media-http-b92-normal95-integration-1021091314-15223`

## Preflight

The complete read-only preflight passed:

- Agent/runtime/normal95 identity and clean shared Runtime checks.
- `runtime.lock.json` source `95bd3c5f`; lock SHA256
  `920f4a3e...65be8e7`; authored/runtime schema SHA256
  `6ba7b51e...9768f2d`; Runtime artifacts SHA256
  `a902387c...3a532d`; artifact count **76**.
- C13/post-schema client origins, contract version `0.2.14`, contract digest,
  Node executable, runtime module, shared-schema module, and `timeline_commit_film_fixture`
  origins all matched. The b92 helper has no `_binding_descriptor`.
- Environment, disk, required auth-scope source guards, and client-data outbox
  guard passed.
- The occurrence fixture file is byte-identical to the approved `ff332817a`
  and `7dedde2a4` blocks; the parent proof is unchanged from `c4a24ae81`.
  The restored block keeps genuine old/new five-field selections, old alias,
  generation/variant identity in both authored planes, mirrored old-asset
  clips, and empty text bindings. No `oldclientshadow` or `fakeauthority`
  source was introduced, and the delta adds no assertions.
- Exact collection command:

  ```text
  env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_PARENT_MEDIA_SEED_RUNTIME=/home/user/work/runtime ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/venv-agent/bin/python -B -m pytest --collect-only -q -o addopts= -p no:cacheprovider -m integration tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_selected_swap_over_authenticated_http_preserves_flight_and_guarded_undo
  ```

  Result: exactly **2** cases, `parent` and `occurrence:occ-a`.

- The same target with `--setup-only` passed setup/teardown for both owners
  without running the body. A direct no-network public-API fixture probe also
  produced real five-field old/new selections for both owners and zero commit
  candidates.

## One allowed HTTP run

Requested exactly once:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-m2-wc1-original-binding-fixed-one-http-0911 wc1-selected-media-http-b92-normal95-integration) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: **2 failed in 7.13s**, both parametrizations. Both cases reached and
passed the assertions for authenticated initial commit, durable acceptance,
lost-ACK transport error, persisted request/key/body/base/guards/media,
fresh-session/restart exact retry using the original flight identity despite a
different caller key, reload, and guarded inverse/receipt restoration.

First failure in each case:

```text
tests/editing_conformance/test_commit_runtime_parent_media_swap.py:422
assert not any('composition' in path or 'publish' in path for path in paths)
```

The run therefore does not qualify as green: the final no-legacy-publication
route assertion observed a matching path. No retry or diagnostic HTTP rerun
was made. The complete log is in the result directory above.

Prior 0806/preflight0844 failures and rejected 0900 proof remain historical;
the 0900 proof was not run or retargeted.

## Changes and next step

No product, test, assertion, fixture, schema, pin, or generated file was
changed in this worker. The worktree is clean. The remaining action is to
inspect the captured legacy-route path causing line 422, then obtain a fresh
orchestrator-authorized proof only after that assertion is explained; do not
silently weaken or remove it.
