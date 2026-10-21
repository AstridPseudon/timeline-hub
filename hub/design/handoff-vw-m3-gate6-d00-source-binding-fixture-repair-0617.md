# d00 source-binding fixture correction handoff

The private successor of the 0417 wrapper is prepared at
`orch/workers/vw-m3-gate6-d00-source-binding-fixture-repair-0617/`.

The only diagnosed fixture correction is the existing prefixed member-hash
serialization result: `sha256:76694aa3...` for 5,902 members. The historical
`sha256:a2478c3c...` is the same frozen d00 source tuples with the per-member
`sha256:` prefix removed. The source remains App d00/tree a8bf, clean and
identical to the frozen git tree.

The exact four-file diff, checksums, and bare/prefixed frozen-object proof are
in the worker folder. The fresh private output namespace is
`gate6-20261021T0617`; it is empty. The complete offline preflight was
attempted with `--preflight` only and stopped at the existing Node child-process
Python-origin guard with sandbox `EPERM`; its stdout showed the expected import
origins. This is unverified custody evidence, not a product failure.

No grant, marker, issue script, physical mode, controller startup, helper,
browser, socket, central, or full suite was run. Remaining blockers are
independent custody review of the exact scripts and an offline preflight in an
environment that permits the existing child-process/localhost guards.
