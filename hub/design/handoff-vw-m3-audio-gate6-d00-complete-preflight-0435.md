# d00 Gate6 preflight handoff

The d00 source binding is intact and HOME ancestry is now valid:

- App pin: `d00a66134f330672ea7471dc69db38c1566d94cf` /
  `a8bf53d5d5e865aa88825bbc20f6f530bfbaa7ba`.
- Final observed HOME: `bc6f9dd39c7e5154ddf075cb87b7202cf5702e65` /
  `4cd13d09b7cffd60612d8521f1a2921ca4e762d2`; d00 and 822 ancestry pass.
- d00 dist is 339 files with index hash
  `aeb5d83399b453b15a8cbc67b31260cf2820f8d65770ccd458986ddd551e257b`.
- Frozen d0a/8f/producer2c4/b70/5a4/public13/4913/Node43d6/Chrome155
  identities and wrapper hashes pass existing custody checks.

This preflight remains blocked. The exact d00 source pin has no private
`node_modules` graph, so App peer, physical-isolation, imports, and test
collection are not qualified. The 0431 current helper worker ended blocked
before execution with no result ID. Final free bytes were `10,845,581,312`;
the `314,671,104` stage requires `11,052,089,344` before staging, leaving a
`206,508,032`-byte shortfall. No grant, marker, browser, export, Runtime,
helper, or physical request was made.

Manager next step: materialize the exact private d00 App graph without
touching shared installs, restore at least `206,508,032` more bytes, then run
the existing 0417 `--preflight` command. A fresh grant/marker is still a
manager-owned pending input and must not be fabricated or reused.

