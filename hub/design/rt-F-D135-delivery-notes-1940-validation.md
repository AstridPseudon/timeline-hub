# D135 delivery prose validation

## Installation

The two existing builder inputs were read at predecessor hashes, mode-checked as regular `0644` files, and installed with same-directory fsynced candidates plus predecessor-hash CAS and atomic replacement. UTC predecessor backups are retained. The installed candidates are exact predecessor-plus-one-paragraph transformations; all outside bytes are equal and each D135 paragraph occurs exactly once.

- README predecessor: `a5ba95670b7e897bf5f1002cf7e68250a6498713317da34d14f2bc90caa6b331`
- README candidate/installed: `df9b4a622fddcb570a6919f4ff1dfd793f2929f0db87bb9aa55f3b529eba79b9`
- Gate predecessor: `2b1af9924445e5f991937f06bcc34451d9168d118ad5f269485862f06daac01e`
- Gate candidate/installed: `5661b6b698620bb6a486fad9677d2dad7117646a2723845f389a73dd40b63b8e`
- Installed mode: `0644` for both files
- Stale Agent proof pin `547e1045…` is explicitly rejected; Agent is sourced from the exact D59 cut tuple (checkpoint `a30e…`).

## Checks

- `pgrep -af '[d]elivery-build'` before and after installation — PASS; no builder active.
- `python3` predecessor/candidate/backup hash, mode, exact insertion, duplicate, outside-byte, and temporary-candidate assertions — PASS.
- Exact predecessor-plus-insertion reconstruction after removing the D135 paragraph — PASS; this preserves the full existing C0 request/reply prose and all deferred/known-state prose byte-for-byte.
- `bin/delivery-build.render_readme` via the installed `render_readme` with the same controlled four-repository stub shape used by the prior prose installers — PASS; zero unresolved placeholders, all four repository sections, D135 rendered twice (template plus gate input), existing pending status, D65, D72, and Gate3-deferred text present.
- `git diff --no-index --check evidence/predecessor-README.md delivery/README.template.md` — PASS diagnostics; expected exit 1 because the approved insertion differs.
- `git diff --no-index --check evidence/predecessor-gates.md delivery/gate-results.md` — PASS diagnostics; expected exit 1 because the approved insertion differs.
- Worktree `git diff --check` — PASS; Composition worktree remains clean.

The paragraph states that each patch base is current upstream `main` at the D59 cut after merge-forward into each integration, requires the exact D59 tuple, names the Agent tuple source, refuses unmerged/upstream-behind trees, and records that no cut/build/ZIP has occurred. D65/D67/D62/D72/D87/D126/D133 prose, all known failures and pending states, and the full C0 request/reply shape remain unchanged outside the insertion.

No product, generated, test, pin, kit, permission, Git-ref, network, clone, wheel, provider, core, native, E2E, P4, actual build, or ZIP operation was run. No additional independent prose review was required under D56; the production caller remains the installed real builder template route.
