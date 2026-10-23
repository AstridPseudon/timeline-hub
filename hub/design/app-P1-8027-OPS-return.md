# App P1 D21 OPS selector-collection return

The actual service8027 result was an ordinary harness failure, not a P1 body
failure. Its preflight passed global setup, actual beforeAll, and trivial
native boot; selector collection then failed before either original body.

The retained target's node_modules graph has no .bin directory. The approved
Remotion environment's PATH still contains /opt/node22/bin, so npm's
Playwright script resolved the ambient Node22 launcher. That launcher loaded a
different Playwright module instance from the copied @playwright/test package
in the retained graph, producing “Playwright Test did not expect
test.beforeAll() to be called here” and “Total: 0 tests in 0 files”.

The existing ap2-P1-chain-h6 row now prepends
/home/user/work/app/node_modules/.bin before the Node20 directory. This is a
read-only harness PATH correction; no graph, dependency, cache, product
source, test body, or generated file was changed. The exact npm list command
then passed twice with Node20.19.4/npm10.8.2 and listed both required
selectors. The manager may queue one changed-service run; this return makes
no claim about the original P1 bodies.
