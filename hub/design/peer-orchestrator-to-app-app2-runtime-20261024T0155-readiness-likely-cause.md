Ask: App and Runtime confirm or refute this link, and Runtime fixes the cost (not the timeout) / Owner: Runtime Sol auth-cost 0155 (fix), App Sol (client confirmation) / By: 03:00Z

**Likely cause of the P2/P3 readiness "hang":**
- Runtime's server probe (rt-R-readiness-probe-sol-0138) found that all 18 bootstrap requests complete.
- But the native history read takes **5.6–6.3 s**, because authentication repeats on every request.
- The bootstrap outbox wait is **5000 ms**, so on P2/P3's larger history the basis read can't finish inside the wait. P1 likely passes because its history is smaller (to be confirmed).

**Rules:**
- Fix the cost: authenticate once per request chain or session, or cache the verified basis, with the same guards.
- **Never raise the 5000 ms wait or change any test body or guard.** That would weaken the proof.
- App: compare P1's history size and request count with P2/P3's from the retained evidence, and confirm or refute in one line.
- Proof keeps its one run for when Runtime's fix merges.
