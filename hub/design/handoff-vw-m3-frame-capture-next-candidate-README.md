# Next native frame candidate — READY artifacts only

This handoff is the post-capture-fix candidate. It preserves the original640
default analog baseline and the separately named native1920 Chrome155 profile,
all four cases, strict `2/255` and `.001` comparison limits, full transfer
checks, native media-error checks, and the original native-codec environment.

The bounded fix dismisses the actual rendered-film popup and waits for its
backdrop to detach before capturing the mounted Player. It does not hide or
rewrite authored pixels. The Agent/App theme background mismatch remains an
unresolved strict RED and is not changed here.

`run-native-frame-parity.mjs` and `setup-native-frame-parity.sh` require a new
manager grant and central flock for any real run. No grant, run marker, browser,
render, socket, or central request is present. The controller is frozen to App
`7989ee28242c866fe8ea34f28e2e116faeaa0d86` and rejects another source SHA.

Future manager-only invocation, after permission and registration, is the
existing named diagnostic suite through the central test service. Do not run
the setup script locally.
