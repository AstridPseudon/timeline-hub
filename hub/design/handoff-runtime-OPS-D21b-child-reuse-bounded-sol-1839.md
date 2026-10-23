Continued the retained 1826 security candidate; ready for independent Luna review, **not installation or merge**. The maker and requester are byte-identical to 1826, with the exact installed-base and 1811 incremental patches exported beside this report. Runtime remains clean at `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.

Confirmed predecessor terminal before copying: `STOPPED`, `ended`, exit 0, no `running` marker. Its branch and this worktree have the same Runtime base. Copied only 11 small evidence files (95,038 bytes); left the previous worker's large `tmpdir-work` and fixture trees untouched. Initial report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-reuse-bounded-sol-1839/early-report.md`.

Replaced only the oversized evidence harness: tiny committed synthetic Agent/Runtime repositories, authentic package/distribution layout, SHA256 RECORD rows, noneditable PEP 610 directory provenance, one baseline plus one mutable installed bench. Synthetic commits use Git fast-import in disposable repositories; no real Git refs, indexes, or configuration changed. Disposable fixtures live only in `$TMPDIR=/tmp/w-2c40903018`. Every source/baseline/mutable/test group measures logical and allocated usage and refuses expansion above 100 MiB. Final-run peak: **661,280 logical bytes / 1,679,360 allocated bytes**; after each session release: 110,993 / 217,088 bytes. Earlier completed private synthetic sessions were released; no real data or predecessor fixture was cleaned or chmodded.

Fresh final results (all exit 0), executed from the assigned Runtime worktree:

```bash
P=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-D21b-child-reuse-bounded-sol-1839
python3 "${P}-test-child-reuse.py"
python3 "${P}-test-dispatcher.py"
python3 "${P}-validate-packet.py"
```

- Security: **97 controls passed**. Includes all decisive 1820 attacks; valid request/maker reuse; missing/wrong/dirty/racing Agent checkout and commit; Agent/Runtime metadata/version/direct URL/editability; missing and changed retained source files; malformed non-client and Agent RECORD rows, unsafe paths, duplicates, absent client ownership; canonical client, Agent and backend byte changes including re-signed RECORDs; writable roots/nested files/source, symlinks, partial benches, ambiguous distributions/benches; same-name maker refusal before provisioning and unchanged retained-target manifests.
- Caller: production defaults evaluate to the existing shared ORCH and `/home/user/work/{agent,runtime}`/work root. Private installed-layout request → exact CHILDVENV payload → extracted actual dispatcher branch → mock maker passes normal and `env -i`, with no CHILD_VENV environment variables supplied to the dispatcher/mock maker. Only hardcoded default fixture paths are substituted; all executed queue/work/source paths are private. Existing maker reuse also passes normal and minimal environments. Fourth argument remains the Remotion graph.
- Validator: `bash -n` on all three shell scripts; compile of four fixture/validator Python files, requester inline Python, three maker Python snippets and scoped Runtime files; four private patch applications (installed base and 1811 parent for both scripts) produce exact candidate bytes. `git diff --check`, empty `git status --porcelain --untracked-files=all`, and `git diff --exit-code 2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d --` pass.
- `cmp` of all 11 worker/flat sources and patches passes; both candidate scripts match retained 1826 bytes. Hash verification: **15/15 OK**, exit 0, using the exact command below from `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design`:

```bash
sha256sum -c handoff-runtime-OPS-D21b-child-reuse-bounded-sol-1839-hashmanifest.sha256
```

Exact scripts, both patch forms, `cmp.txt`, `hashmanifest.sha256`, and three successful final logs use this report's flat filename prefix. Packaging dry runs exposed a fixture launcher executable-path issue and an incremental patch path mismatch; corrected only the harness/private replay command before the successful final runs. Historical 1802/1811 observations are **oldcandidate evidence**, not fresh qualification of any real retained bench.

**Decision remains unresolved:** full maker installs and exercises the actual Runtime backend, so its backend SHA custody guard remains mandatory. The orchestrator still owns full-bench Agent+backend+client key versus a separately scoped client-only redesign. No speculative key choice or component change was made. Production caller remains `request-child-venv → CHILDVENV → make-child-venv`; C0v2 request/reply, frozen34e, actual dependency/package graphs, product/tests/generated/pins, installed scripts, real benches, queues and daemon are unchanged. No network, install, full suite, HTTP/browser run, or full-D21b claim. Real installed bench compatibility remains unverified; the fresh fixtures prove custody logic, not a real provisioning run.

Next: independent Luna security review of the exact hashed packet, then orchestrator key decision. Host installation requires both. Evidence-only; never merge this worker branch.
