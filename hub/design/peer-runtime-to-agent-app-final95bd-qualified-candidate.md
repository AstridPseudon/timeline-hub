# DRAFT — Runtime final95bd candidate announcement

**Do not send, mark `PUBLISHED`, or make current until Runtime manager
acceptance.**

Runtime full31902 is green on the exact candidate:

- server commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`
- tree `d3a290b407fa61e6ab2d476f50c068073f70df00`
- contract/client `0.2.14` / `0.2.14`
- schema `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`
- 76 artifacts; artifact version
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`
- full31902: **5,988 passed, 26 skipped, 15 xfailed, 12 warnings**, exit 0

After acceptance, Agent should use the verified producer checkout
`/home/user/work/wt/rt-pin-95bd3c5f` as `RUNTIME_PRODUCER`, run its normal
`vendor_lock.py update` and lock check, and report the resulting consumer
identity. App should use the exact `contract/artifacts.json` from this Runtime
commit with its normal `scripts/vendor-lock.mjs` updater and checker, then
report the resulting consumer identity. Both consumers must qualify this exact
tuple together; no public/current adoption is implied by this draft.
