# Gate6 pin-loader attachment and one-actual report — 0930

## Result

FAIL CLOSED during the one exact local preflight invocation after the one
authorized read-only attachment. No central preflight request and no physical
request were issued.

## Attachment

Added exactly one top-level symlink:

`/home/user/work/wt/app-pin-0d432391/node_modules -> /home/user/work/wt/app-pin-d00a6613/node_modules`

The target was verified before attachment as the existing private graph
`8bdc44e93ce6f712f2a26fc44f1f8e904215c1785f54ed97f826a98fe0145c5b/32393`.
The frozen Runtime graph was `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c/21455`; the public13 Composition archive was
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` with 77
regular members. React/React DOM were 18.3.1; Remotion, Player, and Media
were 4.0.509; tsx was 4.21.0; Playwright was 1.60.0. `tsx` and all packet
imported tool paths resolved through the attachment.

The App pin remained clean and exact at
`0d4323913b92c4e0e3830bf14ec7f35d981475ca/tree5a1e0e85d0f336f642426b91ccf3b3f1984ebd14`.

## Tests and commands

- Read-only graph/controller precheck: PASS; exact graph `8bdc.../32393`,
  Runtime `4913.../21455`, public13 `77`.
- Cleanup wait: 30 seconds; no active partial697 process or browser-lock
  holder remained.
- Exact local command from ORCH cwd:
  `bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-pinned0d43-preflight-and-one-actual-0923/packet/run.sh --preflight`
  Result: FAIL before central submission in `prepare.mjs:46`, while spawning
  `/home/user/work/venv-runtime/bin/python`: `spawnSync ... EPERM`. Static
  checks, storage budget (`11516743680` free, threshold `11320247244`, floor
  `10737418240`), short-temp claim/cleanup, and fd9 lock ownership passed.
  The raw invocation log is retained at
  `packet/invocation-preflight-ZgsduJ.log`.
- Independent read-only probe of the exact attached path reached the existing
  private-graph guard and refused it with the exact message:
  `private dependency graph must be a real directory`.
- The no-flag physical command was not run because preflight did not pass.

## Decisions and blockers

The existing guard was preserved exactly per instruction; it was not relaxed
to accept an external graph symlink. The packet remains otherwise unchanged,
including the retained d00 dist and its equality guard. The authorized
attachment and target manifest are recorded in the flat ORCH design record and
lease. The local EPERM and the packet's symlink refusal both block central
preflight/physical execution under the current packet; manager direction is
required if the packet is to accept this exact read-only attachment without
weakening its guard.
