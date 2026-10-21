# Producer 1209 after-control reverse-translation first-byte diagnosis

## Verdict

The first new failure is a sidecar fixture-translation identity failure, before
the `after` case dispatches. It is in
`outer-controls-run.phase-corrected-1150.py:83`, for
`producer-startup-only-gate-0717-owned.sh`. The source/artifacts, producer
guards, positive assertions, hashes, profiles, and graph are not implicated.

The 1209 stage counts remain: preflight `11/11` plus the TSX module-format
probe passed; `before` completed and passed; `after` failed during fixture
construction before dispatch; `absent-output`, `copy-failure`, and `success`
were unreached (`1/5` complete, `4/5` unreached). No rerun or code fix was
made.

## Exact byte witness

Inputs were the retained `P/artifacts` eight-file set from:

```text
P=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-complete-execution-prereqs-diagnosis-1132
```

The failing source artifact is:

```text
P/artifacts/producer-startup-only-gate-0717-owned.sh
```

Original identity: `4910` bytes, SHA-256
`4ce9e7f4fc0eb6c6a7b32b784cd3ea64f598b4169fa49ba2a99126237dc4a5df`.

I reconstructed only the existing `after` translation in one ephemeral
`TemporaryDirectory`, using the sidecar's exact mapping and hash-replacement
order. The reconstructed translated artifact had SHA-256
`5fb7649155e112bd6e1736343e193d9f982f61a91ebeaab6983c8f5b22a3e486`; after
the sidecar's reverse operation, the result had SHA-256
`adc74649d5ff5702b98e0af02652e07371503b7b27343cd71ff3a856fb7d9e42`.
The temporary copy was automatically cleaned. These translated/reversal hashes
are witness-specific because the fixture directory name is temporary; the
byte mismatch and cause are path-independent.

The first differing byte in the reversed result is offset **47**, zero-based
(line 4, column 28):

```text
expected: KEEPER=/home/user/work/wt/app-pin-5863411a
actual:   KEEPER=/home/user/work/wt/ap2-m2-producer-helper-expect-import-0717
```

Exact byte snippets, including the following newline:

```text
expected b'KEEPER=/home/user/work/wt/app-pin-5863411a\\n'
actual   b'KEEPER=/home/user/work/wt/ap2-m2-producer-helper-expect-import-0717\\n'
```

The translated bytes contain the temporary canonical path
`.../launch-*/keeper`; the reverse result is wrong at the first path byte. No
guard, shell body, command argument, or producer operation is reached.

## Root cause: replacement order and collisions

At sidecar lines 67–83, all path mappings are applied forward to each artifact,
then all hash substitutions are applied in `ORDER`, and reverse translation
applies hash substitutions in reverse followed by **all path mappings in reverse**.

The canonical temporary keeper target is many-to-one. These three distinct
source paths all map to the same target:

```text
/home/user/work/wt/app-pin-09171792
/home/user/work/wt/app-pin-5863411a
/home/user/work/wt/ap2-m2-producer-helper-expect-import-0717
    -> <temporary fixture>/keeper
```

The forward mapping order is `app-pin-09171792`, `app-pin-5863411a`, then the
helper worktree. Reversal walks the mapping list backwards, so the helper
worktree mapping is the first applicable replacement from `<fixture>/keeper`
back to a source string. Therefore the original `KEEPER=...app-pin-5863411a`
cannot be recovered by global string replacement.

There is a second many-to-one target collision for the `KEEP` marker: four
source spellings map to the same temporary `KEEP` path, with the duplicated
helper marker mapping last. It is not the first differing byte, but confirms
the collision is systemic in the map shape.

The five dependent hash substitutions are computed after path translation in
this stable order:

```text
producer-public13-runner-0717-owned.sh
producer-runner-0717-owned.sh
producer-physical-keeper-gate-0717-owned.sh
producer-startup-only-gate-0717-owned.sh
producer-startup-custody-gate-0717-owned.sh
```

Reverse hash order is the exact inverse. The five old/new hash tokens are
distinct: no old hash equals or occurs inside another new hash, and no new hash
equals or occurs inside another new hash in the witness. Thus there is no hash
collision causing this assertion; the first mismatch is entirely the
many-to-one path collision at offset 47.

## Minimum fix proposal — UNAPPLIED

Preferred data-only fixture mapping: make every source alias target distinct,
then point the distinct temporary aliases at the same canonical fixture
directory (and do the same for the distinct `KEEP` marker aliases). For
example, the three keeper spellings must map to three unique temporary alias
paths rather than one `<fixture>/keeper`. The fixture remains semantically the
same, hashes are recomputed from the translated bytes as today, and the
reverse proof remains exact. Reordering the existing many-to-one map cannot
fix it.

If the sidecar cannot materialize unique aliases, the exact harness-logic
alternative is to retain per-file/provenance-aware path mappings (or map only
the source path tokens present in each file) so reverse translation is
bijective for each artifact. Do not use a broad string rewrite, fake the
matched boolean, remove the reverse proof, or weaken any guard/assertion.

An independent review is required before applying either mapping repair,
followed by the separately authorized single control run. This report applies
neither repair.

## Evidence and boundary

- Preflight: PASS; public13 resolver and all 11 preflight checks passed; TSX
  module-format probe passed.
- Controls: `before` PASS; `after` stopped at reverse proof before dispatch;
  remaining four unreached.
- No source/spec/helper/operation/pin/graph/profile/hash change.
- No build, browser, socket, service, install, actual producer run, or control
  rerun was performed.
- Assigned App worktree is unchanged and clean; the original 1209 failure
  packet and retained inputs were not modified.
