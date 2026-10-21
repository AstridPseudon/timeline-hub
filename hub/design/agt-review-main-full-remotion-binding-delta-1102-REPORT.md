# Agent review: main full Remotion binding delta

**Decision: CODE APPROVED / STORAGE HOLD**

Reviewed only the two-line delta from wrapper297 (`297fbe0e5`) to Agent base
`fc4c23d079f17aa4d8f167b385c7e5bda2edd299`.

## Exact approved identities

- Agent source: commit `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40`, tree
  `3467b7bffb0fe6edf9178c9a9de4d446c8ab8857`.
- Reviewed wrapper: commit `fc4c23d079f17aa4d8f167b385c7e5bda2edd299`, tree
  `7ce6a0b8022928cd98a2f7cd448bf9d24a442587`.
- Wrapper blob:
  `198a94ad1f1c9921705399febb7e7f71dffd419d`.
- Wrapper SHA-256:
  `0e1b5ccd2157788d53d6ba7fa6c0e1adc362e97f190e734cc023bf4ff92e87d`.

## Delta and coherence checks

The only changed file is
`scripts/full_coherent_public_current_integration.sh`, with exactly two
insertions and two deletions:

1. `EXPECTED_C13_SOURCE` changes from stale `30da0a5e05d4529a2b97b3c1818cf9e15842d628` to the target Agent commit `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40`.
2. The fallback `COMPOSITION_ROOT` changes from `agent-remotion-0013` to `agent-remotion-0014`.

The C13 package identity remains 0.0.13 with tarball SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; the
lock SHA-256 remains
`c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`; and
Node remains `v20.19.4`. The unchanged runtime lock pins client source
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` and producer digest
`sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
The `0014` name is only the new immutable runtime destination; it does not
change the C13 package identity or imply adopting Composition14.

The old and target tracked `remotion/` trees each contain 73 files. Exactly
two files differ: `remotion/scripts/fetch-shared-browser.mjs` and
`remotion/src/LiveSceneClip.tsx`. Their target blobs are respectively
`f82c1268bb6cfd7221faeb029a38ef8addfb155e` and
`1aace8ab33c39114c75aad60ba664a319dfeaacf`.

The unchanged guards retain the 164-pin carrier/hash, 166 RECORD files and
166 installed distributions, all76 source/wheel/install byte checks, private
import-origin checks, C13/Node/ffmpeg checks, and direct child exit/SIGTERM
propagation. The wrapper normalizes exactly from wrapper297 after the two
authorized substitutions; no other wrapper line changed.

## Live callers and hold

The durable MAIN caller is
`/home/user/work/main-timeline/coherent-public-current-b3c96a758/runner/approved-current-wrapper/full_coherent_public_current_integration.sh`, as recorded in
`run-on-main-agent-coherent-public-current.md`. Its required composition
root is `/home/user/work/runtimes/agent-remotion-0014`. The existing
`tests/integrations/test_d09_managed_scene_only.py` caller remains explicitly
bound to old `agent-remotion-0013`; it is not changed by or used as the MAIN
full wrapper caller.

At review time, `agent-remotion-0013/.source-commit` is the stale 30da source
and `agent-remotion-0014` is absent. Available storage was 11.623737 GiB,
below the unchanged >13 GiB floor; setup subtotal was 1.168587 GiB and the
`-n 3` transient peak remains UNKNOWN. No storage-ready decision is made.
The new runtime, private profile, build/install, full suite, body, and main
run are all unverified and remain blocked by the storage hold.

## Evidence commands

- `git diff --name-status 30da0a5e05d4529a2b97b3c1818cf9e15842d628 b3c96a758c1cfa2a609d1498e0e9ee401b32cc40 -- remotion` — exactly the two files above; both trees count 73.
- normalized wrapper comparison against `297fbe0e5` — PASS.
- `bash -n scripts/full_coherent_public_current_integration.sh` — PASS.
- `git diff --check fc4c23d079f17aa4d8f167b385c7e5bda2edd299^ fc4c23d079f17aa4d8f167b385c7e5bda2edd299` — PASS.

No full suite, build, install, profile probe, or main run was requested or run.
