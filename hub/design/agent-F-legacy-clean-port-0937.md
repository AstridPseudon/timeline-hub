# Agent F legacy clean-port

PASS — exact source identity: current pre-port blob
`195839982f128753bd9bc06d59c43b51fd8912bb` matched donor parent
`ae3debdd3^`; current post-port blob
`8f48f8f7c3126df26ab5499f945b48e0c5e5f450` matched donor commit
`ae3debdd3`.

PASS — exact reviewed hunk only: `_renderer_selection` now tolerates a
minimal capability record without an adapter by returning no renderer
selection. Outside bytes are identical by whole-file blob identity. The only
changed path is `astrid/core/execution/generic_host.py` (`2 insertions, 1
deletion`). Donor reports were not imported.

PASS — acceptance `1 passed in 0.87s`; compile passed; Ruff `2149/2149`; mypy
`1912/1912`; `git diff --check` passed.

Limits: no full/browser/heavy/HTTP/native/daemon/process suite; no duplicate
review or implementation; harness commit remains pending.
