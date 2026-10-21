# Gate6 exact-pin attachment and ordered execution — 0930

Attachment was the one manager-authorized read-only consumer change:

```sh
ln -s /home/user/work/wt/app-pin-d00a6613/node_modules \
  /home/user/work/wt/app-pin-0d432391/node_modules
```

The target was checked before attachment as the exact private graph
`8bdc44e93ce6f712f2a26fc44f1f8e904215c1785f54ed97f826a98fe0145c5b/32393`,
with Runtime graph `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c/21455`,
public13 archive regular-member count 77, React 18.3.1, and Remotion 4.0.509.
The symlink exposes `tsx/dist/cli.mjs`, `tsx/dist/loader.mjs`, Playwright,
React, and Remotion entrypoints through the exact App attachment.

The required exact bare command, from ORCH cwd, was then run once:

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-pinned0d43-preflight-and-one-actual-0923/packet/run.sh --preflight
```

The same command without `--preflight` was not issued because local preflight
must pass before central issuance, and the existing graph guard refuses the
external symlink with `private dependency graph must be a real directory`.
No guard, packet, source, lockfile, graph, dist, branch, or shared install was
modified; no central request or physical request was submitted.
