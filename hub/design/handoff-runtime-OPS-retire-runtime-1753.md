# Runtime handoff: OPS-retire-runtime-1753 — PASS

Private evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-runtime-1753`.

The reviewed route is:

```text
request-retire-venv agent-remotion-<lowercase-suffix>
  -> queue/pending/retire-venv-agent-remotion-<...>
  -> RETIREVENV agent-remotion-<...>
  -> retire-child-venv <...>
```

The maker grammar is `agent-remotion-[0-9a-z][0-9a-z-]*`; `agent-remotion-current` is protected. A target must be an unreferenced, non-live, older-than-one-hour, canonical direct child of `$WORK_ROOT/runtimes`. Associated `.partial.XXXXXXXX` components are exact-prefix/8-character matches only and receive the same reference, process, shape, age, fingerprint, and race checks. Runtime package/lock files and the four immutable markers are validated when present; malformed/incomplete marker sets refuse. Existing v2 child-venv/source semantics remain intact, including the empty-cmdline/unreadable-exe non-user case and fail-closed unreadable observations.

Fresh independent evidence: syntax exit 0; runtime controls 13/13; v2 controls 17/17; adapted controls 37/37 and 7/7; malformed-name controls 8/8; private runtime associated-candidate probe 13/13; request→exact dispatcher branch→handler FIFO smoke 5/5 under normal and `env -i`. Runtime worktree is clean and `git diff --check` exits 0. The old synthetic unadapted `...-running` 37-case control intentionally exits 1; it is not acceptance evidence because it is outside the actual maker grammar.

Flat exports in this directory:

- `handoff-runtime-OPS-retire-runtime-1753-retire-child-venv.sh`
- `handoff-runtime-OPS-retire-runtime-1753-request-retire-venv.sh`
- `handoff-runtime-OPS-retire-runtime-1753-hashmanifest.txt`
- `handoff-runtime-OPS-retire-runtime-1753-cmp.txt`
- installed diffs and v2 layer diffs for both scripts (`*.patch`)

The staged handler/request hashes are `954d5d87…` / `21f61833…`; installed v2 hashes are `48cac6c7…` / `4713b456…`; qualified v2 hashes are `a500d2a1…` / `44c61283…`. Dispatcher staged, installed, and v2 are byte-identical at `f18bc20b…`.

HOST-only publication, after an idle/process/reference preflight:

1. Preserve each current `$ORCH/bin/{retire-child-venv,request-retire-venv}` as `{script}.<UTC>.bak`.
2. Install the corresponding flat export to a same-filesystem `{script}.new` with mode 0755, verify its SHA-256, then atomically `mv` the `.new` over the script. Do not touch `dispatcher-daemon`.
3. Confirm the installed hashes and run a real, non-worker smoke using the existing caller: `request-retire-venv agent-remotion-<name>`. Observe the normal `RETIREVENV` done/refused receipt and exact target/path/disposition log. Do not manually delete, retry, chmod, or remove markers.
4. Publish the normal route only after the lead confirms host idle, `/proc` cmdline/exe/cwd/fd visibility, suite/env/pending/running-worker references, and UTC backup/atomic-install checks. The worker did not install scripts or delete any host runtime.

No Runtime source/tests/schema/generated files/pins, installed scripts, host runtime, production data, branches, or refs were changed. No v2 request API, receipt/history/error-path contract, or frozen `34eac` invariant was touched.
