# Handoff: ap2-P1 environment review

Status: **PASS — bounded environment review; live P1 body pending the central service.**

Reviewed candidate `38fbbc993e19e39615a99b7a5d524a0da11f91c3` (tree
`6f67994c411f78f9aedb0d244f48764326c5b1cd`) against base
`18354adfa3e8f12b24816a159f28a9a6cbb9a3f6`. The only candidate source change is
`tests/e2e/local/support/astrid.ts`: the exact child environment joins only
`ASTRID_CHECKOUT` first and the existing `RUNTIME_CHECKOUT` second. `spawnGroup`
still receives `exactEnv: true`; credential-file isolation and redaction are
unchanged. No shim, install, alternate executor, product source, or behavioral
spec change was made.

The actual service snapshot mechanism was inspected: `test-run` writes the
candidate tree and creates a snapshot commit with the worker `HEAD` as parent.
The existing `app ap2-P1-chain-h6` row is therefore ready under the updated
ancestry and uses the exact guard
`git merge-base 8770aa1625198826778828173ef6e2c55a3c07f3 HEAD =
8770aa1625198826778828173ef6e2c55a3c07f3`. Full row hash (including prefix and
newline) is `386b66411824e3d4318ef04e1e8414ef98571a1e4b53c49d1aa19b4413850242`;
all non-P1 rows retain hash
`81c9bd02376fccd395708954769b74511e6c2b94683e32968cbd727598a21310`.

Pinned source custody retained:

- Agent `f894c3c9dda25ab03527eeb7f52da5da31d627c1`, tree `d24f25a65be282a56b3fcd814a8718a3c0587b9b`.
- Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc`, tree `9853574865f25e08284e82ffb26c0bdecaa16a30`.
- P1 spec `dfcdee357a822bb8516fdcadae88a074a78c7bdaca3d053991d28721ebfae7d2`.
- Composition archive `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- The row retains `NODE_OPTIONS=--max-old-space-size=6144`.

Checks passed: `npm exec tsc -- --noEmit`; `npx eslint
tests/e2e/local/support/astrid.ts --max-warnings 0`; exact P1 `--list` (2 tests
in 1 file); `git diff --check`; and an offline, isolated-cwd child witness
importing Astrid and Runtime protocol from the two exact pins without sockets.

No build/browser/HTTP/body/full suite was run. The original service snapshot is
known to have failed before either body because the old child environment
dropped Runtime (`ModuleNotFoundError: runtime_protocol`). The next step is for
the manager to retry the unchanged two P1 cases through the central service;
this review claims no whole-chain/H3 credit.
