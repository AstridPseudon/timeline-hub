# D139a source/security review

Verdict: `PASS_SOURCE`.

No source-security findings were found in the two private files. The candidate
serializes each schema flag exactly once, validates the pair before writing the
pending row, rejects duplicate/partial/empty/unsafe/missing/physical-path and
Farm-conflict inputs, skips legacy bench matching when the explicit schema
route is selected, and preserves the authenticated wrapper’s old source,
client, Runtime, seed, Farm, retention, and no-schema behavior.

The real dispatcher was inspected read-only. Its CHILDVENV branch uses
`args=$(sed ...)` followed by ordinary shell word splitting and invokes
`$ORCH/bin/make-child-venv`; the candidate’s path grammar excludes whitespace,
quotes, glob metacharacters, and option injection. The joined `fd83c9…` maker
has the exact two schema parser branches and passes the pair into the existing
schema identity / Store-key path. A private probe reached the joined maker’s
normal source-path refusal, not an unknown-option refusal.

Separate receiving readiness: `NOT_READY`. The authenticated live maker at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv`
is `f07b809…` and has no schema-option parser branches; a private no-body probe
returned `REFUSED: unknown child venv option`. No installation or live request
was attempted. The manager must receive and independently verify the joined
`fd83c9…` maker before this carrier is operationally ready.

All findings are listed here; the readiness mismatch is not reclassified as a
private source defect.
