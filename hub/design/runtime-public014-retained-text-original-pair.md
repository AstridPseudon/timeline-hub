# Published014 original retained-text compatibility pair

Status: **Central execution attempted; failed before collection**. The exact
public two-node `--runxfail` lane was added to the supported test-service
allow-list and submitted once. The service snapshots the requested tree into
a synthetic commit before running the command, so the suite's first guard
(`git rev-parse HEAD == afe379…`) failed even though the captured Agent tree
was the exact public tree `f2cedd08…`. No private017/c964 source, old7d
Runtime, or alternate text/native control was used.

## Exact qualification tuple

| role | commit | tree / artifact |
| --- | --- | --- |
| Agent current PUBLIC014 source | `afe37906433773a29b5928b35abd8075be8a7ecf` | `f2cedd08a01b1a360df79046e4b9c2a5cb101dd5` |
| Runtime server | `b92d3e7a05eec65c142294ef4873edd059e9b31d` | `6abc2f117391de8e7e35c0283f575a002199894d` |
| published Runtime/client producer | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` | `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| generated client | `0.2.14` | schema `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816` |
| published artifact set | `76/76` | version `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac` |
| Agent ordinary command schema | `55 definitions / 29 operations` | `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |

The Agent lock points to the published producer commit and artifact version.
The Runtime checkout at `/home/user/work/runtime` was clean and imported from
the exact b92/tree6abc server path. The generated client imported from this
worker's Agent tree; no installed/private consumer artifact was substituted.

## Preflight evidence

Exact offline preflight command:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=$PWD ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -P -c '<tuple/import/lock/client/artifact/schema/fixture/private-temp assertions>'
```

Result: **PREFLIGHT PASS**. It verified clean source trees, the exact Agent and
Runtime SHAs/trees above, actual Agent client and Runtime imports, client
0.2.14/schema7d4, published95 lock, Runtime all76 manifest/artifact version,
ordinary6ba, the normal fixture at
`/home/user/work/runtime/tests/timeline_commit_film_fixture.py`, and a private
temporary storage write/read under `/tmp`. No renderer was imported or run.
Shared dependency realpaths were unchanged (`/home/user/work/venv-agent`,
`/home/user/work/venv-runtime`, `/home/user/work/app/node_modules`); disk had
10,622,816 KiB available at preflight.

Exact collection command:

```text
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration --runxfail --collect-only tests/editing_conformance/test_commit_runtime_text_binding.py::test_rebind_existing_main_descriptor_undo_is_exact tests/editing_conformance/test_commit_runtime_text_binding.py::test_clear_existing_main_descriptor_and_inverse_are_exact
```

Result: **2 tests collected**, exit 0. The module retains
`pytestmark = pytest.mark.integration`; both original bodies and assertions
remain unchanged. The bodies retain legacy `text/plain` checks, exact byte
size and CAS-byte checks, custody/selection checks, restart and idempotent
retry, canonical-document equality, absence/NotFound clear behavior, exact
inverse/redo, and zero-selection-on-clear assertions.

## Central request disposition

One central request was submitted, and no retry was made:

```text
request-test rt-m2-public014-text-pair-execute-0903 public014-retained-text-original-pair-integration
wait-test rt-m2-public014-text-pair-execute-0903-public014-retained-text-original-pair-integration-1021090309-19713
```

Result: **FAIL exit 1 before pytest collection**, test-service result
`.../tests/rt-m2-public014-text-pair-execute-0903-public014-retained-text-original-pair-integration-1021090309-19713/`.
The service captured Agent tree `f2cedd08a01b1a360df79046e4b9c2a5cb101dd5`,
but `test-run` creates a synthetic commit from that tree before executing the
suite. Therefore the first chained assertion, the Agent commit equality
`git rev-parse HEAD == afe37906433773a29b5928b35abd8075be8a7ecf`, failed.
The Runtime/client/artifact guards were not reached in the central process;
the central log has no collection count and no test bodies executed. The
offline preflight independently passed every guard against Agent
`afe379…`/`f2cedd…` and Runtime `b92d…`/`6abc2f…`, including actual imports,
schema7d4, published95 lock, all76 artifacts, fixture, dependencies, and
private temp storage.

The prior `text-native-private-pair-integration` command still points to the
rejected PRIVATE017/c964 worker and was not used. The generic
`rt-wc8-current14-integration` command was not reused because it runs the
whole integration lane and lacks the exact public95/b92 guards and
`--runxfail`. No old7d lane was used.

Exact one-line suite proposal, if the orchestrator chooses to allowlist a new
public lane:

```text
agent public014-retained-text-original-pair-integration env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_CHECKOUT=$PWD PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -P -c 'import json,pathlib,subprocess,astrid_runtime_client,runtime_protocol; a=pathlib.Path.cwd().resolve(); r=pathlib.Path("/home/user/work/runtime").resolve(); g=lambda p,*x:subprocess.check_output(["git","-C",str(p),*x],text=True).strip(); assert g(a,"rev-parse","HEAD")=="afe37906433773a29b5928b35abd8075be8a7ecf" and g(a,"rev-parse","HEAD^{tree}")=="f2cedd08a01b1a360df79046e4b9c2a5cb101dd5" and g(r,"rev-parse","HEAD")=="b92d3e7a05eec65c142294ef4873edd059e9b31d" and g(r,"rev-parse","HEAD^{tree}")=="6abc2f117391de8e7e35c0283f575a002199894d" and astrid_runtime_client.contract_metadata.SCHEMA_DIGEST=="sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816" and json.loads((a/"runtime.lock.json").read_text())["source_commit"]=="95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c" and len(json.loads((r/"contract/artifacts.json").read_text())["artifacts"])==76 and pathlib.Path(runtime_protocol.__file__).resolve()==r/"runtime_protocol/__init__.py"; raise SystemExit(__import__("pytest").main(["-q","-o","addopts=","-p","no:cacheprovider","-m","integration","--runxfail","tests/editing_conformance/test_commit_runtime_text_binding.py::test_rebind_existing_main_descriptor_undo_is_exact","tests/editing_conformance/test_commit_runtime_text_binding.py::test_clear_existing_main_descriptor_and_inverse_are_exact"]))'
```

## Remaining boundary

This is not a qualification result and does not close O6, authorize legacy
consumer migration, retire a route/writer, or claim whole text-binding
completion. Authenticated retained legacy `text/plain` descriptors remain live;
new selections still require `text/plain; charset=utf-8`. Agent owns the later
marker/consumer migration and must preserve the existing legacy consumers and
positives through an explicit recorded migration.

## Execution worker evidence

Fresh preflight: **PASS**. Agent source was clean at
`afe37906433773a29b5928b35abd8075be8a7ecf` / tree
`f2cedd08a01b1a360df79046e4b9c2a5cb101dd5`; Runtime was clean at
`b92d3e7a05eec65c142294ef4873edd059e9b31d` / tree
`6abc2f117391de8e7e35c0283f575a002199894d`; actual imports came from this
Agent worktree and `/home/user/work/runtime`; schema digest was
`sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`;
the lock pointed to published producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`;
the Runtime manifest contained 76 artifacts at version
`sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`;
the normal fixture was present; shared dependency realpaths were unchanged;
and private `/tmp` storage write/read passed. No renderer was imported.

Corrected exact collection command: **2 tests collected**, exit 0. The first
local collection attempt omitted the Runtime checkout from that command's
`PYTHONPATH` and failed to import `runtime_protocol`; no test body ran. The
corrected command used the suite environment and passed:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=$PWD ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration --runxfail --collect-only tests/editing_conformance/test_commit_runtime_text_binding.py::test_rebind_existing_main_descriptor_undo_is_exact tests/editing_conformance/test_commit_runtime_text_binding.py::test_clear_existing_main_descriptor_and_inverse_are_exact
```
