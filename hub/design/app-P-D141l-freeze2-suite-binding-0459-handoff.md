# D141l → Runtime/App caller handoff

Use the exact first route below after the reviewed paired Runtime kit and
ordinary manager admission exist. This handoff is prospective only.

- target: `app-pin-5344c53e`
- repo: `app`
- selector: `p2-automatic-child-placement`
- normal suite: `d141g-p2-automatic-child-placement-5344c53e-submit`
- preflight suite: `d141g-p2-automatic-child-placement-5344c53e-submit-preflight`
- normal command: `normal-command.txt`, SHA-256 without newline
  `98522d5511c5e66fcfeaa68044f84eaf9fb45b22e9a1145613a5262be47f21a6`
- preflight command: `preflight-command.txt`, SHA-256 without newline
  `97277b3a42e033819b830ff4f1e450616073d6ea3f6d8e4bd598e32681541ad7`
- normal row SHA-256 with exactly one terminal LF:
  `0ff8814a6f3a6b62ddff3737aafd2e2d0260b50bc0fb647752f172b2a5de4f5d`
- preflight row SHA-256 with exactly one terminal LF:
  `bb42880db0cf7987c74ae7da7b82377b467e0e0c76a5439dedfdd86580facbc1`

The source tuple and all eight selector pair summaries are in `binding.json`;
the exact eight selectors and protected source facts are in
`source-manifest.json`. The primary source is App
`5344c53e3063001bb3255bd0c9cd32cc5e77967f` / tree
`dd989783046aeff652486a1ba39db42aea86e201`. The fixed producer members are
Agent `8585ed9c0404d0187b2ce70242d25114a32747c2`, Runtime
`6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`, and Composition
`635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, with their full trees recorded in
the packet.

`registration=false` is intentional. Normal D66 `--submit` will preserve its
resume path by atomically registering the paired rows only after actual kit
admission; no pre-registration is valid. Before dispatch, the caller must
run the genuine builder with this same tuple and compare actual registered
bytes byte-for-byte against this packet. Do not retarget old rows 18617 or
19479, use `full-e2e-timeline`, use direct `--run`, edit the registry by hand,
or claim a kit/body result from this source-only preparation.

The eventual controller-owned artifact belongs at
`workers/app-P-D141g-final-journeys-controller-0303/evidence/runs/p2-automatic-child-placement/submit-plan.json`;
it was deliberately not created here. The eight selector order is placement,
popup ADD, parent move, transition-none single, transition-none bulk,
registerAsset, P1, and P3. The source manifest preserves the approved
placement expectation and full tails.
