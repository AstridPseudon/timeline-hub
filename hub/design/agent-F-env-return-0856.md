# Agent F environment return 0856

## Result

Bounded repair PASS; independent post-exit durability review remains
required. The two existing Agent service rows now point at the durable private
projection `/home/user/work/agent-runtime-projection-0856/site-packages`,
whose `runtime_protocol` link resolves to the read-only live Runtime checkout
at `/home/user/work/runtime/runtime_protocol`. The old worker-temporary
`/tmp/w-5829dd9212/site-packages` path is absent from both rows.
The private root also retains the initial unused direct link; only the
`site-packages` projection is referenced by the service rows.

The first durable-parent attempt correctly exposed the sanitizer's existing
`site-packages` path policy: the service targeted probe reached three renderer
groups but the generic child failed to import `runtime_protocol`. The final
projection uses the sanctioned `.../site-packages/runtime_protocol` shape and
the exact four representative nodes pass: `4 passed in 20.03s`, central
request `agt-F-env-return-0856-targeted-1023085807-14726`.

Static bash/env parsing, positive module origins, missing-source negative
import refusal, Node 22 negative refusal, Node v20.19.4, and the normal
Composition 0.0.14 renderer graph (normal identity
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`) all
pass. No product, source, test,
fixture, generated, pin, shared dependency, launcher, process, contract, or
security guard changed. The original full result remains
`16388 passed, 240 failed, 140 errors, 40 skipped, 5 xfailed`, exit 1; no full
rerun was requested. D09's exact `agent-remotion-0013` fixture remains
visible and absent, with no alias.

Independent review must repeat startup after worker exit before claiming the
durability gate PASS.
