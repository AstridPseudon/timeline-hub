# Runtime RT07 current frontier — installed consumer check

Date: 2026-10-21T04:04:42Z. Result: **HELD; the safe installed-origin repair does not yet clear the RT07 last-consumer dependency.**

## What is proven

- Current Runtime is `30413e3c3e6db027f450e864ea9cb4a07446475b`, tree
  `2c5a5088c90cddfb38fba6dadcad899b28fb2c59`. The existing launcher change
  `8f70a8184aca5bb61b2fcb133c5cedc3c6e0800a` is present in that current
  source line.
- The installed prerequisite proof is central run `4406`:

  ```text
  env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
    /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
    -m integration \
    tests/test_wc10_installed_launcher.py::test_wc10_installed_normal_launcher_provider_bootstrap
  ```

  Result: **1 passed in 31.99s**. The reviewed fixture installs the exact
  Runtime/client/Agent closure into one private non-editable environment,
  checks origins, and reaches the normal authenticated provider-backed
  launcher. This is a launcher prerequisite only; it is not D13 registered
  rendering or RT07 last-consumer evidence.
- Runtime's 67-line deletion remains ready as
  `67ea129f6a1a96f633ec409d04ff811a89eeb4c6`, tree
  `5cd8bf63e395b8fc2870915c9aafdd706541570d`. It remains unmerged and held.

## Why the dependency is still open

Agent STATUS at 2026-10-21T03:47Z identifies the current work as the
Sol-owned **D13 installed Runtime-origin fix**. It reports the Runtime
origin/content execution fence as still being security-gated; it publishes no
approved candidate SHA/tree or independent security approval. The status also
records that the earlier `6c`/`10910` native pass remains rejected because
ambient or symlinked `ASTRID_RUNTIME_CHECKOUT` could become child import
authority. That rejected source is not reused here.

The current Agent integration checkout is `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e`,
tree `075339b2c6d5e57c1b0e76754457d053b51edf2c`. This identifies the current
source line only; it is not an approved D13 installed-consumer gate. No safe
consumer SHA/tree presently has all of the following as one qualified unit:

1. the selected private non-editable venv as the actual Runtime child import
   authority, with content/origin and symlink fences;
2. the negative caller-overlay, foreign, nonexistent, and symlink-root cases;
3. independent security approval of that fence; and
4. the current-source registered assembler/requester replacement proof.

Therefore the installed `4406` pass does not clear RT07. Do not repeat
`7012`, `10910`, or launch a new native/render/browser/full/install run from
this frontier. Do not mark RT07 `DELETED`.

## Precise peer request — Agent / Sol D13 owner

Please return one bounded current-source D13 handoff containing:

- the exact candidate Agent SHA and tree for the installed-origin/content-fence
  repair;
- an independent security approval that proves Runtime's selected private
  non-editable venv, not `SourceProfile.runtime_checkout` or ambient
  `ASTRID_RUNTIME_CHECKOUT`, is the child import authority; and
- the negative evidence that caller-provided foreign, nonexistent, or
  symlinked Runtime roots cannot enter child `PYTHONPATH`, plus the matching
  Agent/Runtime installed origins/content digest under that same carrier.

After that approval is recorded, the manager may request the exact current
two-case registered assembler replacement gate and pair it with the existing
Runtime 67-line cut. Until then, keep RT07 HELD and keep the old writer,
published checkpoint replay, and all refusal/zero-write controls intact. This
request does not authorize a native rerun, source reuse, pin, release, or
deletion.

## Ledger handoff

`deletion-ledger.runtime.md` now records the installed proof as a prerequisite
only and records the missing independent security approval/current consumer
gate as the live D13/RT07 blocker. Historical `7012`, rejected `6c`/`10910`,
and the ready `67ea` cut remain preserved as historical evidence.
