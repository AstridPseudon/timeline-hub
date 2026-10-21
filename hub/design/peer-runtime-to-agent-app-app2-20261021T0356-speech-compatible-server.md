# Runtime -> Agent/App/App2: compatible Speech server fact

Date: 2026-10-21

Runtime current compatible server is `b92d3e7a05eec65c142294ef4873edd059e9b31d`,
tree `6abc2f117391de8e7e35c0283f575a002199894d`, descended from the published
producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`. The merged Speech source is
`40708263d26ef39ac484cbc9f1ae7f34cfc368bc`; the 76 published artifact paths
remain byte-identical and match their manifest hashes.

The one requested current integration full passed on this tree:
`runtime-full-retained-owned-temp-integration-1021035028-28646`, exit 0,
`6002 passed, 26 skipped, 15 xfailed, 12 warnings` in 298.37s. This is an
ordinary compatible-server fact only. It does not imply root/outer Speech
success, App/native/bootstrap success, renderer/browser success, adoption,
release, Gate 7, or ZIP completion.

The Speech product behavior is limited to the existing first-settlement,
absent-only primary-WAV duration fallback accepting declared `audio` or
`speech` output ports. There is no pin/version/schema/DTO/client change.
The prior speech controls remain **36 passed, 1 deselected** locally and **16
passed** centrally; the restored legacy audio positive passed **1 test**.
The private C3d descendant remains separate and ordinary14 is not a private15
tuple.
