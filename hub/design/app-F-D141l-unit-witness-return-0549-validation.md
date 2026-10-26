# D141l isolated normalized-data validation

Result: PASS for the existing normal D89d validator’s canonical input format.
The source result remains a finite bracket qualification, not a continuous
peak claim.

## Direct validator control

Fixture ID: `d141l-data-format-fixture-20261026` (private, isolated, not a live
service job), under `$TMPDIR`:

```text
/tmp/w-db193df03d/d141l-data-format-fixture-20261026
```

Exact command run:

```text
python3 -I /home/user/timeline-hub/hub/kit/bin/d141-validate-receipt.py /tmp/w-db193df03d/d141l-data-format-fixture-20261026/tests/d141l-data-format-fixture-20261026/recorded-measured-floor.json /tmp/w-db193df03d/d141l-data-format-fixture-20261026 d141l-data-format-fixture-20261026 app full /home/user/work/app 4de54db14bdc9ddc2ce2e5887258b03acbffd30d 84c3fb7f73f08c22220f8e808962fe3f24aaa0aa 'npm test -- --maxWorkers=3'
```

Observed stdout: `4793895424`  
Exit: `0`  
Validator: `/home/user/timeline-hub/hub/kit/bin/d141-validate-receipt.py`  
Validator SHA-256: `2987adbcd888400a41afbbd60e22ea2e4afe6c4580b084a4d63dcced6943a7f6`  
Schema: `timeline.d89d.measured-floor.v1`  
App source binding: `4de54db14bdc9ddc2ce2e5887258b03acbffd30d` /
`84c3fb7f73f08c22220f8e808962fe3f24aaa0aa`  
Registered command: `npm test -- --maxWorkers=3`

The fixture root and both witness files were manager-owned (`uid=0 gid=0`)
with no symlink components. The validator’s exact witness bytes were
`Avail\n5433016320\n` and `Avail\n4839120896\n`; its returned floor matches
the raw-derived arithmetic:

```text
X = 5433016320 - 4839120896 = 593895424
floor = max(4600000000, 4000000000 + 593895424 + 200000000)
      = 4793895424
```

This direct call was a data-format control only. The installed `test-run` was
read and hashed but not invoked; no test body, localhost/browser/live socket,
service request, receipt attachment, live job ID, new `df` sample, kit change,
or repository fixture was used.

## Independent conservation and source checks

- `normalized-start.df` SHA-256:
  `42ea80dcbc160c2195fd638bc7dc27281ec5b6805fca5a23243edb14c7b67716`.
- `normalized-stop.df` SHA-256:
  `8af93918517a4e48289462a64d52c4f8f0ec20c4f90dfcc84f2f1a141db0f0a3`.
- Admission source SHA-256:
  `79149911f6b4c21fa7a48b64032f6b4c27188d06491273a323c0ba688dbaa5ae`;
  numeric field byte range `[104, 135)` and exact value `5433016320`.
- Normal closed-log source SHA-256:
  `720b56d6f058d8aa5ed7770b1e2e5c54a5703ebb68a6403edccfc7a8f6e4302d`;
  stop row byte range `[1157219, 1157291)` and exact value `4839120896`.
- `grep -aboF` independently located the normal stop row at byte `1157219`;
  all source hashes, samples, run IDs, heads/trees, custody, and comparator
  ranges are recorded in `source-manifest.json`.
- `git diff --check` on the assigned Composition worktree: PASS; no product
  or Composition bytes changed.
