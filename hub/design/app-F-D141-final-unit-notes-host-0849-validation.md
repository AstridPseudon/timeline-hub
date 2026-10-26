# D141 final App unit candidate validation

Scope: source-only private candidates. No App/Main installation, product import, delivery-build invocation, rehearsal, clone, patch, build, ZIP, service, package acquisition, registry action, or product test was run.

Authenticated SAFE inputs were read from the three exact `runtime-final-unit-notes-input-0849-*` design preimages and checked against `runtime-final-unit-notes-input-publication-0849.json`. The two candidate documents were generated as private evidence outputs only.

Checks:

- `README.template.md` and `gate-results.md` each contain the disclosure paragraph exactly once.
- The README candidate is the exact README source bytes plus the disclosure suffix; the gate candidate is the exact gate source bytes plus the disclosure and complete 32-ID table.
- Existing prior bytes are conserved byte-for-byte; no canonical delivery file changed.
- Both candidate documents have balanced triple-backtick fences.
- The gate candidate visibly carries all 32 current failure IDs, classified `OWN/N/A` (5 absent files, 27 absent exact titles/predicates).
- Exact `delivery-build.render_readme` was imported from the authenticated source and called **FUNCTION ONLY** with controlled `agent`, `runtime`, `app`, and `composition` result dictionaries. Rendered placeholders were replaced, the two-document disclosure occurred twice in the composed README (once from each source document), and the finite ID table occurred once.
- The same function was called with a nonexistent gate-results path; the existing `_Not recorded yet.` fallback remained active and no placeholder remained.
- The current `4de54...` measurements were not retargeted to the separate `82e9...` catch-up applicability source.

Rendered output hash: `4084e1c74bf1f47dce8447edb96840b113729144e7653cf11291ba589074a422` (scratch only; not a delivery artifact).
Fallback output hash: `3a3e162113f53562287bae234cce33eaaa89adc333bebf648d445fbfe94784a0` (scratch only).

`python3 -m py_compile` is required for the authenticated delivery-build Python source; its output is directed to the private scratch prefix, not the design directory. Types, lint, product tests, and full suites are N/A for this prose-only task.

Disk monitor: `df -B1 --output=avail /home/user` ran in retained session `74496`, with PID `2` as reported by that session. The final retained sample was `4725121024` bytes, above the `4000000000`-byte stop. The trace file retained one sample only; the live terminal emitted additional samples that were not durably retained. This persistence failure is disclosed and not backfilled. SIGINT stopped the session at 2026-10-26T09:05:16Z; the subsequent wait poll returned `Unknown process id 74496`, so exit, wait, and reap status are not independently observable.

The ordinary source admission floor was 4,600,000,000 bytes and no heavy path was used. The retained service receipts use five-second sampling and a 4,000,000,000-byte stop; no continuous-peak interpretation is claimed.
