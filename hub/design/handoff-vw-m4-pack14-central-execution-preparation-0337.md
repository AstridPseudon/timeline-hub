# Composition 0.0.14 central release command — prepared, held

The normal central release command is prepared but not submitted while
release14-ordering-HOLD-0335.md remains active. It targets the existing
exact retained source /home/user/work/composition:

- commit 7bb54bbd64107e5090643ecca1e4d33164173e85
- tree 20467712e66dbadff4d562c0d5baae22b8c077a7
- package 0.0.14

Command:

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-pack14-central-execution-preparation-0337/COMMAND

SHA-256:

c3d3a02fd2d9b4dce8e072f9b2d27fd581f077b007f33f56f9425a0ee6786163

When the manager clears the hold after worker0335 proves the physical
boundary, register and request exactly this named suite:

composition release14-normal bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-pack14-central-execution-preparation-0337/COMMAND

The command pins Node 20.19.4, verifies the exact source/tree/version and
registry freshness, runs build/build:test and the required focused tests,
packs normally, runs package smoke, and records the archive hash/member
manifest. Output is confined to the worker's persistent release-output;
existing artifacts cause refusal. Public13 remains guarded at SHA-256
9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738.

No archive, central request, source edit, pin change, or consumer change was
made.
