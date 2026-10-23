# OPS-D21b Remotion reuse review (1836)

Status: **PASS — evidence-only review; no installation, merge, or product qualification.**

## Scope and findings

Reviewed the settled PLAN, COMMON/header kit rules, Sol1824 packet, and the
1818/1802 failure reports. The repaired flat scripts restore the installed
defaults (`ORCH` under the harness ORCH root; `W=/home/user/work`; Agent
checkout `/home/user/work/agent`) while preserving private overrides. The
production caller remains the existing `request-runtime -> RUNTIME ->
make-runtime` path; the dispatcher branch is the literal `RUNTIME` branch and
invokes `make-runtime $(sed 's/^RUNTIME //' "$f")`.

The exact private matrix verifies:

- default, unset, empty, and private-root selection without invoking a real
  shared requester or daemon;
- exact queued 2-, 3-, and 7-argument payloads and the extracted dispatcher
  branch;
- legacy 2/3 forms refuse missing explicit Runtime identity with exit 2;
- explicit 7-argument forms reuse with exit 0, including a second request with
  different requested Agent/Runtime commits against the same authenticated
  Remotion tree and physical graph;
- Node 20.19.4/npm 10.8.2 validation precedes reuse; authentic build-origin
  commit/tree/package/lock/component/installed-byte facts and registration
  tuple are checked;
- artifact, readonly, partial, ambiguity, source/profile/template, engine,
  marker, modified-env/row, and changed-tree negatives refuse as expected;
- unmarked legacy-layout graphs remain build-required/unqualified;
- private version-only Node/npm mocks record 54 version checks, with zero
  installer calls and zero network calls.

Authenticated source facts exercised by the matrix:

`Agent=78738040d72ce74c42ddf7731221aecb06f9246d`, alternate requested Agent
`33fc387968c0b1bd4a78e828c34677d6f9cadd21`, Remotion tree
`b01dca9b3b24f54093c20b7c5657316f997725db`, Runtime
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, alternate Runtime
`31c7ac3a00f7a205f507bf5bd4d4625628d429bd`.

## Exact checks

All commands were read-only apart from private `/tmp` fixtures and packet
export files. The first verifier/matrix attempt found the prior worker's
scratch target absent; creating that private directory was required by the
fixture's hard-coded assertion. The exact commands then passed:

```sh
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-D21b-remotion-reuse-sol-1824-request-runtime.sh
# exit 0
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-D21b-remotion-reuse-sol-1824-make-runtime.sh
# exit 0
python3 -m py_compile <sol1824 evidence>/verify_packet.py <sol1824 evidence>/test_reuse.py
# exit 0
python3 <sol1824 evidence>/verify_packet.py
# exit 0; 15 manifest entries OK; patch/cmp/compile/diff/status checks PASS
python3 <sol1824 evidence>/test_reuse.py
# exit 0; D21b private reuse/source-custody/toolchain/registration/caller/refusal matrix PASS
```

Runtime remained clean at `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.
The packet hash manifest and flat exports are present in `ORCH/design`.
Installed snapshots are maker
`9fc7f72a7d03fcb4618310ad57f5c9cf111b78a59b2c02caa702073d0951fd09` and
requester `15b07daf4cd46a225ecc020c11e3ec8f3a62368c73d9ba6940ad3ce4ea8191ff`.

## Limits and handoff

This is not a real host call, daemon run, npm/build, graph publication, or
product test. C0v2 request/reply and frozen34e remain unverified here. No
universal reuse or migration claim is made; existing unmarked graphs remain
future-only.

If the lead proceeds, first recheck those installed snapshot hashes and host
idle state. Apply only the exact reviewed flat patches, preserving each
predecessor as `<script>.<UTC>.bak`; install through `.new` then atomic `mv`,
never while the dispatcher script is running. Perform the authorized idle and
real-call-shape qualification separately, record the Runtime board KIT CHANGE
line, and retain the rollback `.bak`. No worker installation is authorized by
this review.
