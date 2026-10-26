# F D141z Main receiving independent findings

Verdict: **PASS** for the bounded Main receiving closure.

The accepted `61f91572495f4a5733058f1310055846730d3b9b` / tree
`28047a71b0d06f43d945ff92a935bfce2aa31e5e` caller and lifecycle helper are
byte-identical to the published exports. The candidate caller imports the
helper from its own artifact directory; the installer checks both hashes before
loading it, so a helper-only install or a sibling mismatch is refused.

The three exact candidate rows bind the caller path/hash. The installer also
checks the genuine core runner, inventory, D68 wrapper, and builder, then checks
the caller's corresponding path/hash pins. The genuine D68 source is regular
`0755`; its transport copy is `0644`, and the caller uses `sys.executable`.

The real Main registry is `tests/suites.conf`, SHA-256
`7b1ffdd7225ad9db6a21dd3f2ced1ae7aa3335249ae9994f529aec6d15fd98df`, mode
`0600`. The candidate validates the seven inherited Runtime rows, all four
current disjoint D141 rows (`full-d141-cut`, `full-d141-pristine`,
`d141-p5-cut`, and `full-d141-pristine-targeted15`), and exact candidate row
identities. Private replacement/readback proves all outside bytes are retained.

Independent private negative controls rejected source/hash/path/mode/symlink
drift, registry preimage drift, unknown outside-row drift, tuple markers, an
occupied backup, and an injected atomic-replace failure. The replace failure
left the private registry preimage and removed staged tuple/temp artifacts.

The PASS is source receiving only. No canonical registry write, final tuple or
gate tuple, live dispatcher admission, real builder/main/rehearsal, final build,
ZIP, full suite, browser, socket, or service body was run or claimed. The
candidate's `/tmp` evidence-root coordinates are prospective source artifacts;
durable canonical deployment remains a later gated action.
