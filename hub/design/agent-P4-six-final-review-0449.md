## PASS — P4/G2/G3 independent final scoped source review

Reviewed committed `tl/agt-P4-final-six-join-0442` at
`9b658b28c3a7bc3ebda3ad5a7b5b417d78553720`.

- Actual committed Git tree: `84bd8ef3429c06ced18c0639388be8b2c8ecd030`.
- Parent `246f92507f15ac16c3bb559b7ce1576a608c86d8` tree:
  `1358a918b2d20413e86c4cd56031a5b92e9b8842`.
- The author’s intended `3b95d9e5a9397ab2084819ceecd09b0bdfdf25c6` used
  noncanonical `040000` directory modes in its manual hash; canonical Git
  modes produce the actual committed tree above. The content is still exactly
  parent plus the approved one-file addition.
- Six P4 blobs match the 0420 note exactly:
  `85218e8e99a1c7602d2b7ee399f3847fac759186`,
  `1ed257c4604552793d2eaabfc117babe93c5b445`,
  `80c15e2944b5660a18077aa38f84cf3b3ced09bb`,
  `fd248182a0e1c120fa6440994da545c4e13219ad`,
  `05f7aa2bd862fc608ee17515d373c5f5b47c27eb`,
  `5ee8dd5b863c164e0ea5f03257ac61849a425061`.
- Public `Timeline.undo` facade and caller test equal the 9fbb blobs; d106
  canonical schema and f252 schema-test blobs are preserved.
- Normal lock/artifact/generated-client state equals normal `f894c3c9`, with
  15 mappings and frozen Runtime source `34eac0041b0891e9011966b39bcbd26053fde5bc`.
  R2/R3/meta/R1-native/U4a ancestry is retained. Separate home `ccc` and G4
  create-empty qualification are out of scope.
- Production CLI → sheet/emitter → session/outbox → generated HTTP → provider,
  plus show/history/readback and inverse, is callable in source (the staged
  Runtime proof asserts those paths; its HTTP body was not executed here).
  Local numeric undo remains preserved.
- Controls: P4 SDK **15**, public/schema **107**, local numeric undo **2**;
  HTTP nodes **2 collected only**; scoped Ruff/private mypy PASS; normal Ruff
  **2149/2149**; normal mypy **1915/1915**; vendor/artifact/diff checks PASS
  (the exact donor’s intentional EOF blank line is the only parent-to-target
  `diff --check` diagnostic).

No full/browser/live HTTP/native/crash suite was run. Proof owns the immediate
real single-HTTP then ten-HTTP execution. Full evidence is in the worker report.
