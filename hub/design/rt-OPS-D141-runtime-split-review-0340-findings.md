# OPS D141h independent review — FAIL

## D141H-SEC-001 — terminal trace append is not no-follow or custody-safe

`privateops-d141-measured-floor/bin/d141-append-final.py:27-30` uses `Path.open("a")` on the trace path without rejecting symlinks, requiring a regular file, checking ownership, or opening with `O_NOFOLLOW`. `bin/test-run:64-80` calls this helper after terminating and reaping the sampler, and only then invokes `d141-validate-trace.py`.

An executing body or concurrent actor that can replace `tests/<FULLID>/disk-trace.tsv` in that interval can redirect the append to a symlink target, block the runner with a FIFO, or replace the sampler-owned inode before validation. The later validator's `lstat` check does not protect the earlier append and also has a check/read race (`d141-validate-trace.py:30-35`). This breaks the required durable KEEP trace custody and can turn terminal admission into a denial-of-service or false trace result.

Remediation required before PASS: make the terminal append operate on a securely opened descriptor (`O_WRONLY|O_APPEND|O_CLOEXEC|O_NOFOLLOW`), verify regular-file ownership/mode and the expected parent components, and preserve/bind the sampler-created inode (or equivalent immutable identity) through finalization. Validate through a descriptor or otherwise close the validation TOCTOU. Add a poison control that swaps the trace path between sampler reaping and final append and asserts refusal with no redirected write/block.

No candidate source was modified because this assignment is source/security review only.

## Non-findings / qualified controls

- Manifest has exactly the intended five direct `bin/` production files; the live normal `bin/test-run` preimage is exactly `0be17b74ad1e324bc84e50e61e50e3e07390b262b7abe17a37ad22b9bd10d0fe`; all four new helper preimages are absent.
- Exact P5 `runtime-d141-p5-cut-1026013331-6934` binds only to `runtime/d141-p5-cut`; target15 binds to `runtime/full-d141-pristine-targeted15`; 8912, 19479, bare/suffix/wrong P5 IDs refuse before launch artifacts.
- App D141g is fail-closed with `paired kit pending`; no App release is qualified.
- Receipt trust, witness, job/source/command identity, floor arithmetic, default floors, 4GB stop, one-heavy guard, source/snapshot/cache/lease paths, and the C0 v2 contract references remained unchanged in this private split.
