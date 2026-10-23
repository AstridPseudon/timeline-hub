# Handoff: ap2-P2-auto-proof-return-1030

## Source repair

P2 ported only `tests/e2e/local/auto-real-proxy.spec.ts` from reviewed
candidate `bc3e49f86acc29cb3c330b2ec38d20882292fa7c` onto exact base
`0212bf3d18e26243afd594569794ee7dfbb2227c`. The product builder was not
edited. The candidate's independent1014 FAIL was repaired by making optional
C0 request annotations conditional rather than mandatory.

The final source preserves the original automatic-placement reconnect,
lost-ACK exact retry, Runtime/Vite restart, reload, guarded inverse, custody,
operation-route, and zero-old-route assertions. It adds strict request/reply,
canonical intended-delta/raw-preservation, Runtime `/commits`, history records,
and `undo_steps` checks. The local inverse matcher keeps exact path, scope,
base, command/publication, source, and key guards while admitting only the
authorized v2 metadata envelope.

## Qualification

PASS: scoped ESLint; exact auto-real-proxy Playwright `--list` (1 test); App
and Node TypeScript checks; `git diff --check`; EOF check; read-only
Composition 0.0.14 resolution from the private 819acf graph.

UNRUN by instruction: browser/body/HTTP, live sockets, build, full suite,
central service, daemon, or test-service request. The private 819acf graph has
no Playwright binary, so list used the existing repository runner without any
dependency mutation.

Next step: independent no-weakening review, then central browser qualification
on the integrated App/Agent/Runtime tuple.
