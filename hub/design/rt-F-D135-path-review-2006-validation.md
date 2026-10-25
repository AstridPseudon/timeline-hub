# D135 independent path review

Verdict: **PASS_WITH_FINDINGS** for the exact D135-REV-1 implementation delta. The
original implementation finding is fixed: private delivery/work/template/gate/source-tuple
validation now runs inside the existing `argparse.error` boundary. Two non-code findings are
listed once in `findings.json`.

## Exact scope

- Reviewed `d45e07dfb` against `799cf268`; the production delta only moves the existing
  private-input/source-tuple validation into the structured refusal boundary. The focused test
  adds the caller subprocess matrix.
- Substantive independent review `1949` is reused for the unchanged D135/D59 ancestry,
  identity, private-root, extras, and verifier controls.
- The exact pinned Agent tuple remains `/home/user/peteromallet/astrid-agent`, SHA
  `a30e74e901a28b39c28facba3deb00d76f186e23`, tree
  `ece8e0887e48e45cb1fce85b1256c49a0f6126c0`; no stale local `work/agent` substitution is
  accepted.

## Checks

| Command or check | Result |
|---|---|
| `python3 -B -m unittest -v ops-delivery-d135/tests/test_delivery_build.py` | PASS — 8 tests |
| `ruff check ops-delivery-d135/delivery-build ops-delivery-d135/tests/test_delivery_build.py` | PASS |
| `python3 -m py_compile ops-delivery-d135/delivery-build` | PASS |
| `python3 -m compileall -q ops-delivery-d135/delivery-build ops-delivery-d135/tests/test_delivery_build.py` | PASS |
| `git diff --check 799cf268 d45e07dfb` | PASS |
| candidate script SHA/mode | PASS — `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`, `0755` |
| installed reference SHA/mode | PASS unchanged — `f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708`, `0755` |
| final reviewed tree | `92401b1abc84a0a6a23d5b0d9b9bfebeb41638a2` |
| D59 tuple SHA | PASS — `ce3d06b41014bcd5cd42454c62828c7d240d3beb0a570467be0375109b1c4338` |

## Refusal matrix

An independent direct subprocess matrix covered relative and symlink forms of delivery root,
work root, README template, gate-results, and source-tuple inputs: 10/10 returned exit 2,
contained no traceback, reported the structured label-specific error, and left the pre-existing
delivery and work directories empty. The existing focused test also preserves ancestry refusal
before any staging write and checks exact repository/base/tip reporting.

## Atomic installation readiness

No installation was performed. A manager-dispatched Codex installer may atomically install only
the candidate named above to the installed entrypoint after verifying SHA `ef9cd915…680fd9ca`
and mode `0755`, with `TIMELINE_DELIVERY_SCRIPT_SHA` set to that exact hash. The installer must
write a temporary file in the target directory, verify it, atomically replace the target, and
retain the predecessor until replacement verification. The successor D59 tuple must be supplied
and pass all-repository ancestry preflight before any positive delivery run.

## Not run

No install, positive build, ZIP, clone, network, body/production request, hub write, source-repo
write, branch/ref change, or full suite was run. The current committed tuple remains refusal-only
for production qualification where its Agent/Runtime/App tips are not current upstream
descendants.
