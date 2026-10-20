# App private392 native consumer/session gate

## Result

PASS for the bounded native App consumer/session qualification on the isolated
private392 candidate. The central runner tested the generic port/session/client
path, not a mounted UI gesture. No App product source was changed in this
worker; the candidate was already at `cb45dbb1d02b007938a0ec8fd379aaaba941fc55`
(`tl/ap2-m2-private392-current-consumer-gate-source`).

## Exact matched identities

- Runtime producer commit: `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`
- Runtime producer tree: `8be43e13acb436120f8a63b1a178d64c49422461`
- Runtime health/schema: `sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042`
- Runtime raw timeline bundle: `sha256:fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3`
- Runtime artifact manifest: `sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d` (75 artifacts)
- Agent normal private pin: `1303ce6be32e7bd96ed5c6b35afcb15819e81b50`
- Agent normal private tree: `2f2685d85c3f65b458795100a8045371eb19ee06`
- Agent source contract: `e010e6a3868e963471244491bb6672c3e4a5135e`
- Agent schema: `sha256:39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`

The existing Agent native/Door `10824` PASS2 is retained as prior evidence and
was not rerun. No `a0`, `952`, public013, future mute/remove/overlay, or other
cohort was used.

## Central evidence

Command queued centrally against the exact required target:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-private392-current-consumer-gate-source targeted --files "src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts" --no-cache
```

Result `ap2-m2-private392-current-consumer-gate-source-targeted-1020222004-8385`:

```text
3 test files passed; 30 tests passed; exit 0; 4.89s test time
snapshot tree feea92d859c05c4560b6101713f63caa97f19af0
```

Evidence is retained at:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-private392-current-consumer-gate-source-targeted-1020222004-8385/`.

The native consumer test exercises declared merge and replace lowering,
original namespace/leaf guards, stale same-leaf zero-write refusal, disjoint
rebase, lost acknowledgement, dispose/reload, persisted outbox recovery,
exact retry identity, guarded undo, opaque `null`/`false` data preservation,
and zero non-handshake POSTs outside `/commit`.

The source candidate's prior checks remain: 30 focused Vitest tests, producer-
backed runtime lock check, ESLint, TypeScript no-emit, and `git diff --check`.

## Decision and limits

The central allow-list had no private392-specific App suite entry. I used its
central App `targeted` runner with exactly the three reviewed files rather than
inventing a suite or running an unrelated normal014/public/full/browser path.
This is the requested one bounded App consumer/session result. No local
HTTP/provider/Door/socket/full run was made. No public or integration pin,
adoption, or mounted gesture qualification is claimed.

No blockers remain for this bounded result. Broader release, public adoption,
and mounted-gesture evidence remain separate gates.
