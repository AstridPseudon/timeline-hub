# F D09 independent source/profile review and activation

## Verdict

**SOURCE: PASS. PROFILE: PASS. CENTRAL D09: PASS.**

The reviewed Agent worktree was `6562cde02c937d70b395718b8e2b71c4f01a1eb8`
(tree `71dd74353b451e380355f3aa0a8467ec26869cbd`), based on `ce1d1cca8`.
The exact current profile was `/home/user/work/runtimes/agent-remotion-v3-819acf-1110`.
The source/profile gate passed before the one authorized central activation.

## Independent source review

- Parsed the current D09 file and `git show ce1d1cca8:tests/integrations/test_d09_managed_scene_only.py`.
  The bodies of `test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle`
  and `test_public_checkout_check_uses_retained_managed_scene_result` are
  AST-identical. All original managed-scene, retained-result, live-child-origin,
  and isolated-child assertions remain present.
- The fixture's optional `ASTRID_REMOTION_PROJECT_DIR` binding resolves to the
  supplied profile, while the absent-variable default remains
  `/home/user/work/runtimes/agent-remotion-composition14-255b6856`.
  Import probes passed for both default and override paths.
- The source tree differs from `ce1d1cca8` only in the author fixture file;
  `git diff --check` passed. No product, validator, guard, pin, generated,
  package, or contract source was changed.
- The current worktree `remotion/` source files (76) are byte-identical to the
  corresponding profile files.

## Independent profile/custody review

- Profile package dependency resolves to
  `file:artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`.
- Lock SRI is
  `sha512-Ajl7lyCbJqbbOpHKEr2xlhFw85hWyirlTU1Dq63BNNUdHYfqgzLXljmudP359uKH6yBxSBMPTDoHLxgiDt65oQ==`.
- The archive is exactly 73,451 bytes with SHA-256
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` and
  80 regular members. All 80 installed Composition files match the archive
  member names and bytes exactly; the installed Composition tree has no symlinks.
- The profile has 21,534 regular files and zero writable regular files. Node is
  `v20.19.4`, Remotion is `4.0.509`, and the direct Composition import passed.
- The original f1012 installed custody remains intact: the recorded 182
  `RECORD` files pass their pre-existing hashes; the 164-pin inventory remains
  the recorded `478af081b0f27c1e90dac1ab4b0b645583f34787ecfe7b8079d1bb88ca034761`
  manifest; and Agent, Runtime, and Runtime-client wheel hashes match the
  previously qualified values. A real `python -I -B` child imported the Agent,
  Runtime, client, protocol, and schema namespaces from the private f1012
  site-packages root.
- The profile handoff's archived-source `npm run typecheck` failure remains
  disclosed: the archived source lacks generated registry files and two external
  `threejs-live-editor` modules. No workaround or source change was introduced;
  custody and the live D09 proof are independently qualified.

## Targeted evidence

Commands run directly in this worktree:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/integrations/test_d09_managed_scene_only.py
3 tests collected in 1.15s

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m ruff check tests/integrations/test_d09_managed_scene_only.py
All checks passed!

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m mypy --config-file pyproject.toml tests/integrations/test_d09_managed_scene_only.py
Success: no issues found in 1 source file

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider tests/test_installer_schema.py::test_remotion_lock_pins_the_immutable_composition_public_entry
1 passed in 0.67s
```

The test-service row passed `bash -n`, has exactly one D09 test node, has no
`PYTHONNOUSERSITE`, and is the only `d09-current-v3-1113` row. The only
orchestration change is that row in `ORCH/tests/suites.conf`; its bindings use
`env -i`, pinned Node in `PATH` and `ASTRID_NODE_EXECUTABLE`, f1012 Python,
`-P`, worktree `PYTHONPATH`, installed Runtime/schema paths, and the correctly
spelled `ASTRID_REMOTION_PROJECT_DIR`.

## One central activation

Requested exactly once:

```text
agt-F-D09-review-1113-d09-current-v3-1113-1023111556-14827
```

Exact central result: **pass, exit 0; 1 passed in 192.23s (0:03:12)**.
The executed node was only:

```text
tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result
```

No retry, full suite, HTTP/browser/native run, installer companion, daemon/Git
write, shared dependency mutation, or tool bypass was performed. The full v2
commit request/reply and metadata surfaces were untouched. No Agent/autoclassifier
denial occurred.

## Handoff

No blocker remains for this D09 review. The central result directory is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-F-D09-review-1113-d09-current-v3-1113-1023111556-14827/`

Recommended next step: preserve the exact profile and suite-row custody while
the manager records this PASS; do not substitute the stale Composition14
profile.
