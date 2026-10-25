## D128/F report

- Independent final binding: **PASS**. Wrapper SHA `564716…7fa3f`; suite row SHA `fcfd28…0fd8f`; source1747, maker, support, parent, helpers, Python, wheels, disk, isolation, and source hashes verified.
- Submitted exactly one authorized service: `agt-OPS-inventory-E2E-final-receive-1822-inventory-whole-maker-1025182407-27653`.
- Service reached two fixture Git commits and two private Stores, then failed at the first parent-maker check: exit `2` instead of expected inventory refusal. No candidate GREEN, registration, adversarial checks, retry, or fake result.
- No safety, classifier, or permission refusal occurred.

Tests:

- Wrapper preflight: **PASS**
- `bash -n`: **PASS**
- Evidence JSON parse: **PASS**
- `git diff --check`: **PASS**
- Full suite: not run.

Evidence is in [`evidence/`]( /home/user/work/wt/agt-OPS-inventory-E2E-final-receive-1822/evidence). Runtime owns the independent failure review and any follow-up CAS/install. `BLOCKED` and the conventional commit message were written; no product code changed.