# Candidate cause for readiness-after-bootstrap (P2/P3), from upstream Agent, 00:45Z

Upstream Agent main moved 74f3f7edb..90d469808 (15 commits). One of them, **f38e164cca** "Fix host bootstrap readiness marker, attempt_base, Linux census race", changes:
- astrid/core/execution/generic_host.py: receipt-mode activation now allocates attempts under the owner-observed output root;
- astrid/core/execution/process_group.py: a Linux ps/proc census race made children of an exited parent read as "unverified child of a missing parent";
- astrid/sdk/host_bootstrap.py.

This may be the cause of P2/P3's "owner/read-only readiness baseline UNKNOWN after bootstrap".

Actions:
1. **App (owner of readiness-after-bootstrap):** test this hypothesis first, against your retained P2 18800 and P3 458 evidence. Look for a census-race or attempt-root signature. Don't change any body, guard or timeout.
2. **Agent:** open row **U2c-readiness-draft** (Luna, Sol if hard). Port f38e164cca alone onto a branch from tl/integration, with its own tests plus the integrated Agent tests.
   - Don't merge it yet. Under the upstream rule, it may merge early only if App confirms it is the cause, and **only after the P1 18792 Proof verdict is recorded**: no merge while an exact-pin proof on Agent is pending.
   - The other 14 upstream commits (CI, lanes, tests) are deferred to the freeze.
3. **Proof:** no new P2/P3 run until App names the cause. Then run once.

Other upstream (deferred to the freeze): App 65c1771b7..b236cbfa3 (2 commits, render controls and the visual seam contract); Runtime aa6c5b0cb..795379a67 (managed-output export root default).
