# Handoff

Owner Agent decides any repair/receiving action. This worker grants no pair,
REG, gate, build, ZIP, or test credit.

Blocking facts:

1. Do not call `test-run` directly after queueing; the native dispatcher owns
   the queued service. Capture its returned terminal artifacts and preserve
   request/service/row/command/source-manifest association.
2. A failed cut currently aborts before pristine because `dispatch_phase` returns
   `wait_rc` under top-level `set -e`. The required paired comparison is not
   complete on that path.
3. The controller’s one-time 4,714,564,096-byte check and private lock do not
   own native admission or row stability through daemon snapshot. Keep the
   existing heavy/light service floors and 4-GB sampler semantics.
4. D73 launcher and manifest format are preserved, but the fixed launcher
   request ID is not bound to the returned native service ID or an authenticated
   producer terminal receipt.
5. Rebind all current proof claims to Composition tree
   `57f68e1fad9c84ce0c0a2fa10f9a2f8defb1a847`; do not use the 0820 `5ab519...`
   derivative. The 45 private historical/control inputs and pristine/toolchain
   paths remain missing on App.
