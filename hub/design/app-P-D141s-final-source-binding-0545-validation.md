# D141s actual final post-REG source binding

Status: `PROSPECTIVE_PRODUCTION_BUILDER`; `registration=false`; `execution=none`.

## Authenticated source and builder

Read-only Git checks against the normal `tl/integration` homes found clean
sources: App `4de54db14bdc9ddc2ce2e5887258b03acbffd30d` / tree
`84c3fb7f73f08c22220f8e808962fe3f24aaa0aa`; Agent
`8585ed9c0404d0187b2ce70242d25114a32747c2` / tree
`92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`; Runtime
`95d98f038320d5d46bd679ac000ab3e15825c935` / tree
`78df31d62c5b9ba4c84dee4ea346e43a767718c1`; Composition
`635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / tree
`5ab5191a296980a0a6bcd1178ab6902d6478a148`.

Agent, Runtime, and Composition exact detached checkouts were directly read
back at `/home/user/work/wt/agt-pin-8585ed9c`,
`/home/user/work/wt/rt-pin-95d98f03`, and `/home/user/work/wt/vw-pin-635f4de0`;
all were clean and matched their full pins and receipts. The planned App
checkout `/home/user/work/wt/app-pin-4de54db1` is absent. Its absence is
reported honestly: no App checkout metadata or receipt was inferred or
claimed. The later manager-owned normal `request-checkout` must materialize
and verify it before real D66 submit/body work.

The normal App source builder was authenticated before the pure import:
`/home/user/work/app/scripts/testing/d66-plain-stack.mjs`, final Git blob
`59b65214bc74c1ca118b097bc3b13c0ffe480a93`, SHA-256
`2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`, 49,914
bytes. It is byte-identical to the required old blob from 0459. The only
exports used were `buildSubmitPlan`, `serviceRecipe`, and
`exactCheckoutPath`; no submit/run/bootstrap/provider/diagnostic-helper import
was used.

## Exact first pair and all eight rows

The first selector is `p2-automatic-child-placement`, target
`app-pin-4de54db1`, repo `app`, with normal suite
`d141g-p2-automatic-child-placement-4de54db1-submit` and preflight suite
`d141g-p2-automatic-child-placement-4de54db1-submit-preflight`.

- `normal-command.txt`: 966 UTF-8 bytes, no terminal newline, SHA-256
  `55da9058c938ce4ba362670b1322c49097441007d460677f6f5b2726c7f4c2aa`.
- `preflight-command.txt`: 978 UTF-8 bytes, no terminal newline, SHA-256
  `f20ab22c427e46fb06edbc2f91ea11ad27faf7a1b38c11abbc20895e465471a4`.
- Exact row bytes are the UTF-8 row plus exactly one LF (0x0a), with no CRLF:
  normal 1,022 bytes / `c921243a9fbd154ed5ef16c27154212b6626e59748d7f3d34d5592fc38e32362`;
  preflight 1,044 bytes / `6d69ba5b21658c4f4acf5b6ecfd946089fd442b86bcb9683ac1b9dc63b9f6f83`.

The eight selector order is placement, unchanged D141j popup ADD, parent move,
transition-none single, transition-none bulk, registerAsset, P1, P3. The
binding packet records every pair's command length/hash and row length/hash,
and the source manifest records all eight source spec blobs/SHA-256 values and
their unchanged full tails/inputs.

## Original 5344 comparison and registry guard

App final `4de54db1` is a two-parent result whose first parent is the original
`5344c53e`; its entire tree differs from `5344c53e` only at
`public/install-manifest.json:runtime.sha` and `runtime.lock.json:source_commit`.
All eight scripts/spec blobs and full tails remain byte-exact. Compared with
the immutable 0459 packet, only the App and Runtime pins/checkout paths and
the corresponding final suite names change; selector, command tail, guards,
source specs, and the Agent/Composition pins do not change. The old 0459
receipt is not retargeted.

The current registry preimage was read-only: `suites.conf` is 733,192 bytes,
SHA-256 `e100f177f029aedc17b5e4ad3fb697e1c9e98142ca88e6c91101c5f0046ac5f7`.
All 16 prospective `d141g-*-4de54db1-submit[-preflight]` names are absent.
No registry, queue, metadata, kit, pin, or checkout file was written.

## Checks run

- Supported Node `v20.19.4` pure import invoking the genuine
  `buildSubmitPlan` + `serviceRecipe` for all eight selectors: **PASS**.
- Recomputed 16 command/row hashes and compared them with the packet; first
  command files compared byte-for-byte: **PASS**.
- `python3 -m json.tool` on `binding.json` and `source-manifest.json`: **PASS**.
- `git -C /home/user/work/app diff --check 5344c53e... 4de54db1...`: **PASS**.
- Composition worker `git diff --check`: **PASS**.

No test, typecheck, lint, browser, collection, localhost, socket, provider,
preflight, submit, queue, or body run was performed; the source is unchanged
and this task is limited to pure production-builder evidence.

## Caller condition

The later production D66 caller uses this same genuine `serviceRecipe` builder.
Before either paired part (preflight or normal) is dispatched, its registered
bytes MUST equal the corresponding output recorded here byte-for-byte. This
packet is not an installed pair, not a source checkout receipt, and not a
behavior result. Runtime receiver0519 remains the normal receiving owner under
the 06:00Z PASS_INSTALL deadline; otherwise normal floors and existing holds
remain in force.
