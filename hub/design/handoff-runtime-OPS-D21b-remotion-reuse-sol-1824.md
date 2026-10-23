# OPS-D21b Remotion reuse: bounded root compatibility repair

Status: **private staged checks PASS; independent review and HOST publication pending. Evidence only; NEVER MERGE; NOT INSTALLED.** Completed 2026-10-23T18:32Z.

## Finding and repair

Read PLAN, COMMON, BOARD-HEADER (kit rules and D21b), failed independent 1802/1818 handoffs, and staged author1811 scripts/fixtures. The exact 1811 prologues made `RUNTIME_ORCH_ROOT` mandatory in both scripts and `RUNTIME_WORK_ROOT` mandatory in the maker; `RUNTIME_AGENT_CHECKOUT` also lost its installed default. The unchanged production daemon calls only `$O/bin/make-runtime $(sed 's/^RUNTIME //' "$f")`. No new daemon environment is justified.

Restored the installed assignments verbatim:

- `O=${RUNTIME_ORCH_ROOT:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}` in both scripts.
- `W=${RUNTIME_WORK_ROOT:-/home/user/work}` in the maker.
- `A=${RUNTIME_AGENT_CHECKOUT:-/home/user/work/agent}` in the maker.

Private optional overrides remain available and validated. The request comment now accurately puts toolchain validation before reuse; its queue diagnostic no longer incorrectly calls the installed queue private. No dispatcher change. **The entire maker from `NODE_BIN` onward is byte-for-byte identical to the reviewed1811 source.** The only maker difference is the root-selection repair.

## Fresh private proof

All execution targets were resolved and asserted beneath the harness-assigned private tmpdir `/tmp/w-1a7207d41c` (the worker's `tmpdir` is a text pointer, not a directory). Source checkouts and template facts were read only. Every whole-script invocation used explicit private ORCH/work roots; the exported production scripts were never rewritten for acceptance and were never invoked against a real queue. Fixtures retain scratch output; no cleanup or tracked deletion was performed.

Default-root proof executes only the extracted assignment-only production prefix under `env -i`, including unset, empty, and explicit private overrides. The expected ORCH/work/Agent assignments are checked against installed source. The prior exact root-guard fragments reproduce exit 2 without executing their queue bodies. All new default decisions exit 0 and return the exact installed paths. This is intentionally a static/extracted root-decision proof, not a whole default-root host invocation.

The full private path runs the exact staged requester, checks the exact `RUNTIME ...\n` payload, and executes the installed daemon's literal RUNTIME condition/invocation against a byte-identical private copy of the exact maker. Only that branch is extracted; no daemon loop or host dispatcher is run. Receipt routing covers successful/refused results. Under `env -i`, identity/template environment variables are absent; the maker receives only the queued positional arguments. The private work-root toolchain lookup supplies version-only Node/npm mocks without `RUNTIME_NODE_BIN` injection for these dispatcher flows.

- Old 2-argument request: requester exit 0, exact payload; maker exit 2 for missing explicit Runtime identity.
- Old 3-argument request: requester exit 0, exact payload; maker exit 2 for missing explicit Runtime identity.
- New 7-argument request: requester/maker exit 0, truthful reused receipt and env/row registration.
- Second new 7-argument request with different Agent/Runtime SHAs: exit 0, same physical synthetic graph, original build-origin SHA retained.

The old maker already requires explicit Runtime source declarations for legacy forms. That refusal is preserved; legacy maker success with missing identities is **not** claimed or fabricated. No identity environment was injected to replace absent queue payload fields.

Authentic read-only source identities in the final run:

- Agent build origin `78738040d72ce74c42ddf7731221aecb06f9246d`.
- Different requested Agent `33fc387968c0b1bd4a78e828c34677d6f9cadd21`.
- Shared committed Remotion tree `b01dca9b3b24f54093c20b7c5657316f997725db`.
- Runtime requests `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` and `31c7ac3a00f7a205f507bf5bd4d4625628d429bd`.

Synthetic graph package/lock bytes come from those actual Git commits; the graph is explicitly a fixture, never represented as an installed production graph. Env and suite assertions cover requested source identities, retained build origin, selected Node executable, physical graph path, checkout guards and retained pytest consumer. Different committed tree takes the normal bounded build branch, stopped with exit 3 / `installer=not-run` while an older different-tree graph is present. No physical requested-name graph is created by reuse.

Refusal controls PASS: nonexistent Node executable; wrong current Node/npm versions; artifact bytes/manifest; fabricated build origin; committed-tree marker; lock/package/component markers; installed lock/package provenance; missing marker; engine markers; writable graph; partial and ambiguous graphs; unapproved profile; modified env/template row; mismatched Runtime source; ambiguous positional/inherited identity; mocked dirty checkout. Unmarked old-layout fixtures remain unchanged and produce build-required, never reuse or an upgrade claim. Reviewed production old-layout graphs remain future-only; none was opened for mutation or newly qualified.

All Node/npm execution is private version-only mocks. Final log: 54 version checks, **zero installer calls, zero network calls**. A private build-stop is set before every maker invocation, with a curl blocker and version-only tool executables as additional bounds. No actual npm, provisioner, network build, toolchain installation or graph publication ran.

## Exact validation commands and results

Final targeted private matrix (exit 0):

```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-remotion-reuse-sol-1824/evidence/test_reuse.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-remotion-reuse-sol-1824/evidence/matrix.log 2>&1
```

Final packet exporter/validator (exit 0):

```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-remotion-reuse-sol-1824/evidence/verify_packet.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-remotion-reuse-sol-1824/evidence/verification.log 2>&1
```

The validator records each exact command in [checks.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-remotion-reuse-sol-1824/evidence/checks.log), including:

- Separate `bash -n` invocations for both exact `.sh` files: exit 0.
- In-memory scoped compilation: five embedded Python heredocs, three `python3 -c` snippets, both fixture/validation Python files: PASS.
- `cmp -s` of staged/flat scripts and patch pairs: exit 0.
- Four `patch --batch --output=<private-output> <private-baseline> <patch>` applications: exit 0; each output exactly matches the staged script. No installed target is patched.
- `sha256sum -c /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-D21b-remotion-reuse-sol-1824-hashmanifest.txt`: exit 0, all 15 entries OK; detailed output in `evidence/hashcheck.log`.
- `git diff --check`: exit 0. Added patch lines separately checked for trailing whitespace.
- `git status --porcelain`: exit 0, empty. Runtime HEAD remains `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.

No full suite requested. No product test, generated file, client, contract, pin, integration worktree, installed kit script, queue or actual graph was changed. The C0v2 full request/receipt/canonical/history/conflict/invalid/preview surface and frozen34e remain untouched and **unverified by this script-only packet**; no product qualification is claimed.

## Flat packet and next gate

Flat files in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/` with prefix `handoff-runtime-OPS-D21b-remotion-reuse-sol-1824`:

- `-make-runtime.sh`, `-request-runtime.sh`: exact staged scripts.
- `-make-runtime.patch`, `-request-runtime.patch`: complete diffs against read-only installed source snapshots.
- `-make-runtime.root-fix.patch`, `-request-runtime.root-fix.patch`: minimal compatibility diffs against author1811.
- `-hashmanifest.txt`, `-cmp.txt`: hashes and exact validation/cmp results.

Fixtures, source snapshots, logs and full commands remain in [worker evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-remotion-reuse-sol-1824/evidence). Installed snapshot SHA-256: maker `9fc7f72a7d03fcb4618310ad57f5c9cf111b78a59b2c02caa702073d0951fd09`, requester `15b07daf4cd46a225ecc020c11e3ec8f3a62368c73d9ba6940ad3ce4ea8191ff`.

No blocker for this bounded repair. Next: independent Luna review of these exact flat bytes and private proofs. Only after PASS, the lead may conditionally perform HOST idle/real-callshape qualification and UTC-backup/atomic publication under the existing kit rules. Recheck installed snapshot hashes before applying a patch. No install, merge, host smoke, actual-graph qualification, or approval waiver is authorized by this report.
