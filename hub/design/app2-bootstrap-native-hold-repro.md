# App2 bootstrap native opaque-inverse hold reproduction

Date: 2026-10-20 UTC  
Scope: peer prerequisite evidence only; no App, Runtime, browser, socket, or
repository-source change.

## Source and environment

- Agent source: `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`
- Agent tree: `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`
- Immutable extracted source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary`
- Python: `/home/user/work/venv-app2-native/bin/python` (Python 3.12.3)
- Requested test files match the Agent ref byte-for-byte:
  - `tests/editing_conformance/test_pristine_initialize.py`: SHA256 `67535a672d6749e2780c12858bb93a80a7274479e5c334edd3cab1a968ac09b0`
  - `tests/sdk/test_timeline_pristine_initialize_provider.py`: SHA256 `d26dc517e73123084ddd9d1d6099e2097575a77eff2c83cca154076087c1faea`
  - `tests/editing_conformance/fixtures/pristine_initialize.json`: SHA256 `214566e2a8ea7127ac5d27389ff4da5bedefd12b13155c89454b4719bda47b63`

The four held successes are the original inverse-preservation vectors for an
unrelated `parent.opaque` addition with values `null`, `false`, `[]`, and `{}`.
They were run from a temporary `/tmp` pytest probe with the strict xfail marker
and `--runxfail`; the Agent archive and its tests were not edited.

## Exact runs

Untouched requested native/provider lane:

```sh
ARCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ARCH" /home/user/work/venv-app2-native/bin/python -m pytest -q -c /dev/null -p no:cacheprovider --runxfail \
  "$ARCH/tests/editing_conformance/test_pristine_initialize.py" \
  "$ARCH/tests/sdk/test_timeline_pristine_initialize_provider.py"
```

Exact result:

```text
...........................                                              [100%]
27 passed in 1.18s
```

Forced original-positive hold repro:

```sh
ARCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ARCH" /home/user/work/venv-app2-native/bin/python -m pytest -q -c /dev/null -p no:cacheprovider --runxfail /tmp/ap2-m2-bootstrap-native-hold-repro-test.py
```

Exact final result:

```text
FFFF                                                                     [100%]
FAILED ...::test_inverse_preserves_unrelated_opaque_parent_fields[null]
FAILED ...::test_inverse_preserves_unrelated_opaque_parent_fields[false]
FAILED ...::test_inverse_preserves_unrelated_opaque_parent_fields[array]
FAILED ...::test_inverse_preserves_unrelated_opaque_parent_fields[object]
4 failed in 0.56s
```

The temporary probe reported the same details for every case:

```text
actual failure kind='inverse_dependency_changed' ref='parent' path=[]
```

The first temporary-probe collection attempt had an unused import in the probe
itself; it was removed before the reported run. No Agent or App source was
changed. The probe was deleted after testing.

## Interpretation

This is a real reproduction of the hold, not a refusal encoded as a passing
replacement. The current initializer records:

```text
parent []       present {'config': {'clips': [], 'tracks': []}, 'registry': {}, 'clips': []}
parent ['config', 'output'] absent
parent ['name'] absent
parent ['slug'] absent
parent ['registry', 'assets'] absent
```

`astrid/sdk/timeline/native_initialize.py:9` calls `ctx.read('parent')`, so the
whole raw parent is an inverse dependency. After the initializer and track
creates, the probe adds an unrelated `parent.opaque` field. Inverse validation
reaches `astrid/sdk/timeline/inverse.py:358-365` and rejects the changed whole
parent with `inverse_dependency_changed` before applying any reversal.

The intended property-guard behavior is narrower: initialization must still
refuse a non-pristine parent before writing (including a pre-existing opaque
field), and it must retain the four explicit absence guards for fields it
creates. An opaque field added later, outside the initializer write set, should
survive inverse/redo. The raw whole-parent read conflates pristine-entry
validation with the later inverse dependency set.

## Smallest Agent-owned correction

In `astrid/sdk/timeline/native_initialize.py`, retain the exact pristine-empty
inspection and `not_pristine` refusal, but perform that inspection without
recording `parent` as a whole-root `ctx.read`. Keep the existing narrow reads for
`config.output`, `name`, `slug`, and `registry.assets` (and their absence
checks). This keeps the safety guard against initializing over authored input
while allowing inverse validation to ignore a later unrelated opaque sibling.

Do not add a broad inverse bypass, App marker, Runtime field, or fixture
exception. The four original successes remain strict expected failures until
this Agent correction is implemented and the same tests pass normally.

Not run by design: App tests, Runtime tests, Runtime Door, localhost/live
sockets, browser/e2e, full suites, dependency installation, or central test
service. This evidence does not qualify App cutover, Runtime admission, or
writer retirement.
