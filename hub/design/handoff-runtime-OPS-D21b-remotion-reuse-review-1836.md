# Runtime OPS-D21b Remotion reuse independent review 1836

Status: **PASS.** Evidence-only review; do not treat this as installation,
host qualification, or product qualification.

The Sol1824 repair resolves both Luna failures without changing the settled
design. The flat requester and maker restore the installed ORCH/work/Agent
defaults, retain safe private overrides, and leave the existing production
`request-runtime -> RUNTIME -> make-runtime` caller unchanged. The exact
dispatcher `RUNTIME` branch was reviewed; it passes the queued payload to the
maker without a new daemon environment.

Fresh independent checks passed:

* `bash -n` on both flat scripts: exit 0.
* Scoped Python compilation of embedded blocks and both verifier programs:
  pass.
* `verify_packet.py`: exit 0. Exact flat scripts and patches compare equal;
  four private patch applications reproduce the sources byte-for-byte;
  `sha256sum -c` passes all 15 entries; `git diff --check` passes; Runtime
  status is empty at base `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.
* `test_reuse.py`: exit 0. Default/unset/empty/private root decisions,
  exact 2/3/7 queued request shapes, extracted dispatcher branch, legacy
  missing-identity exit-2 refusals, explicit7 reuse, changed Agent/Runtime
  request identities on one authenticated Remotion tree, Node/npm ordering,
  build-origin/source/package/lock/bytes/registration checks, all listed
  negative controls, and unmarked-graph refusal pass. The private mocks report
  54 version checks, zero installer calls, zero network calls.

The first attempt failed only because the prior worker's hard-coded private
scratch target `/tmp/w-1a7207d41c` no longer existed; recreating that empty
private directory allowed the exact unchanged verifier and matrix to pass.

Packet export hashes are recorded in:

`handoff-runtime-OPS-D21b-remotion-reuse-sol-1824-hashmanifest.txt`

Key flat hashes: maker
`f63adc876ee489cc1bb3a9e038b31b2a432bb17557f566c84d93305c35dbccec`, maker
patch `dca7db221f1a94f45539cb87c9a974b73b24424f3039c795d6f4dc9eb4a2140d`,
requester `f13a1d073699712ccfb05e8463ad97ff69dc210a2617f2c9e0140a242591f7b1`,
requester patch
`1fe1149e03d4ba5f9719ff86d31541201f6568462a460395314e4be4bff14c23`.
Installed snapshots remain maker
`9fc7f72a7d03fcb4618310ad57f5c9cf111b78a59b2c02caa702073d0951fd09` and
requester `15b07daf4cd46a225ecc020c11e3ec8f3a62368c73d9ba6940ad3ce4ea8191ff`.

Limits: no real requester/daemon/host process, npm/build, installation, graph
publication, full suite, C0v2 product proof, or frozen34e proof was run. No
universal reuse or migration claim is made; existing unmarked graphs remain
unqualified.

Conditional next step for the lead: recheck installed hashes and idle state,
then apply only the reviewed flat patches using `.new` plus atomic `mv`, keep
the predecessor as `<script>.<UTC>.bak`, and record the required Runtime board
KIT CHANGE line. Perform authorized host idle/real-call-shape qualification
separately. No worker installation was performed.
