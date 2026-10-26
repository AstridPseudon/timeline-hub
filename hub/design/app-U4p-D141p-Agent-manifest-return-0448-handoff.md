# U4p D141p handoff

The App manifest now pins qualified Agent `8585ed9c0404d0187b2ce70242d25114a32747c2` and retains qualified Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` plus the existing schema digest. Vendor provenance records the same Agent commit/tree. The normal vendor tool produced 160 payloads, and a private refresh comparison plus direct Git tree/blob checks proved every payload and every other App path unchanged from `8f278b91accec5852e39bb84822e99124fccb81d`.

The source checkout was verified clean and exact before either updater. The required installer User-Agent behavior is present. No source merge, fetch, Git metadata write, service request, or scope expansion was performed.

The manifest and vendor provenance changes are ready for manager review. The update-manifest test file was not altered; its direct run remains environment-blocked by nested Node subprocess output suppression in this sandbox. The manager should rerun the required acceptance command in the normal test environment.
