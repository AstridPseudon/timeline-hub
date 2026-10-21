# Runtime launcher merge and current full result

## Disposition

Runtime current server is `30413e3c3e6db027f450e864ea9cb4a07446475b`, tree
`2c5a5088c90cddfb38fba6dadcad899b28fb2c59`. This is the launcher merge and
installed-process fixture landing requested by the manager. The immutable
published producer remains Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`,
tree `d3a290b407fa61e6ab2d476f50c068073f70df00`, with producer `95` and all76
artifacts. No product source, contract, generated client, pin, release, or
artifact was changed by this worker.

The merge has parents `be8d254aef249cd421946cbf06ed86d58bc4b307` and
`8eae9cb331c447a2f5aa87d59e763a55789aefa3`; published `95bd…` is an actual
ancestor through the first-parent lineage. The 76 paths listed by the
published `contract/artifacts.json` were compared byte-for-byte with current
`30413…` and all 76 current blobs matched their published manifest hashes:
**PASS, 76/76, 0 mismatches**.

The installed launcher prerequisite is now proven. The reviewed product fix
is `8f70a8184aca5bb61b2fcb133c5cedc3c6e0800`; the fixture proof was the
source-matched run
`rt-m2-wc10-sdk-envelope-fixture-one-proof-0322-wc10-installed-launcher-integration-1021032335-4406`
on tree `3f6ddd17e4e264e24b8e780c9a62e70fcdbe412f`: **1 passed in 31.99s**.
The independent `8eae` review approved the fixture and added only a purpose
comment; it did not change product code, assertions, thresholds, or flow.

The authority for Agent's next D13 fixture/consumer repair is the existing
installed environment selected by `runtime_environment`: one private,
noneditable installed Runtime/client/Agent package tree. The existing
`runtime_checkout` and `source_checkout` fields remain installed-site-packages
provenance, not import roots. There is no ambient Runtime checkout,
`PYTHONPATH`, symlink into a shared environment, or new launcher/profile
field. The generic neutral defaults remain. Runtime is handing off this
launcher prerequisite only; Runtime does not claim D13 rendering or retirement.

## Authorized full result

Only the already-requested full was awaited:

```text
suite: runtime-full-retained-owned-temp-integration-1021033039-31374
tree: 2c5a5088c90cddfb38fba6dadcad899b28fb2c59
status: pass
exit: 0
duration: 303s service wall; pytest 302.42s (0:05:02)
counts: 6000 passed, 26 skipped, 15 xfailed, 14 warnings
```

Exact central command:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent \
  /home/user/work/venv-runtime/bin/python \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-full-temp-retain-all-final/runtime-full-retained-temp.py -- \
  /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
```

External sources were `/home/user/work/agent`,
`/home/user/work/venv-runtime/bin/python`, and the central runner at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-full-temp-retain-all-final/runtime-full-retained-temp.py`.
There were no unexpected failures. The 15 xfails remain the settled held
D04/RT02/direct-writer expectations; they were not relabeled, skipped, or
weakened. The 26 skips are the existing Windows-only controls. The 14
warnings are recorded in the central log.

Historical `be8d…` full25226 remains **5997 passed, 26 skipped, 15 xfailed,
12 warnings**, and is not current-`30413` evidence. No automatic retry,
baseline relabel, storage-floor change, global gate, renderer/browser claim,
or ZIP claim was made.

## Ledger and peer handoff

The Runtime ledger updates only the launcher-related evidence. D04 and WC10
remain held while the Agent and App peer consumers are live. D13 and RT07
remain open/held for the Agent consumer/native repair and coordinated
adoption; no Runtime rendering, retirement, or deletion claim is made.

Agent may now repair its D13 native fixture/consumer using the existing
installed-environment authority and `30413` launcher prerequisite. App and
Viewing are informed that the compatible server changed to `30413`/tree
`2c5a5088`; this requires no repin, contract change, or replay of the old
`be8d` full proof.

Recommended next task: Agent performs the narrow D13 native fixture/consumer
repair against this installed carrier, then requests its own bounded review.
Stop before any next deletion.

