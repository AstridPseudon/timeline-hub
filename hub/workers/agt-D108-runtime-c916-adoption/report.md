Implemented D108 provenance adoption.

- Updated only `runtime.lock.json`: `source_commit` → `c91626f5e905f9336b51aae0486a071d83f0bac7`.
- Runtime checkout: HEAD `c91626f5e905f9336b51aae0486a071d83f0bac7`, tree `16264479ae18fbb05ec5356ce5b5ab6f69dea9aa`, clean.
- All 15 vendored artifact bytes unchanged.
- Lock SHA256: `44ccac649b50d8163ed1f60b49530b618cc3f8bb70973f5578436676d8d208bb`
- Manifest SHA256: `9bbce65e5b8dd4fd7ca1f24105ffb88d341e5d5beb10348e555dda79145c4dd3`

Commands/results:

- Direct old-lock check refused exactly: `producer commit: expected 1daca2a33f6d7b10053e07c539a54843e3984e19, got c91626f5e905f9336b51aae0486a071d83f0bac7`.
- Refresh tooling: succeeded.
- `vendor_lock.py check`: passed.
- Targeted pytest: `29 passed`.
- `git diff --check`: passed.

Agent current HEAD/tree: `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` / `6056414359ae9fce08d999d54cbef719fda33c3`. Harness successor commit is not yet materialized; prospective tree is `68df11fad2b082fa12d99ca20404e1e40e350cd7`.

Completion marker and commit message were written.