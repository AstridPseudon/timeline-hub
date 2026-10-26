# D141 P5 cut route

This is a private, installable route description for the P5 acceptance cut.
It has no service registration and does not launch Runtime, Agent, a product
test, or a renderer. The checked-in configuration binds the existing final
Agent make-checkout receipt to commit `28e56cacb42d3da85b02e5b3543895b44f3d0f70`
and tree `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`. Both the row and receiver
derive the checkout, provider/client origins, schema metadata, and lock
values from that receipt and clean frozen source. A different commit or tree
is refused even if the configuration omits its optional expected commit.

The eventual service row is `runtime d141-p5-cut <command>`. It keeps the
existing `-m pytest -q -n3 -p no:cacheprovider -m integration` command and
both complete reviewed source files, and writes JUnit plus the normal D66
disk, raw-exit, argv, origin/hash, and `KEEP` witnesses under the runner's
`D66_OUTPUT_DIR`. It does not select individual tests, collect the product
suite, or capture test bodies.

The Agent binding is accepted only from an existing `make-checkout` done
receipt. Commit, tree, provider/client origins, schema digest, and lock
metadata are derived from that clean checkout; they are not configuration
claims.

The row retains the existing `argv.json`, `module-origin.json`, and
`source-hashes.json` witnesses from the bound checkouts before the service
removes its snapshot. Its argv includes the expanded JUnit output path.
The XML suite name is pytest's default `pytest`; `d141-p5-cut` identifies
the service request and JUnit filename. The receiver checks the exact row,
argv, source hashes, all 38 frozen testcase IDs/counts/outcomes, raw exits, disk and KEEP
witnesses. Every required artifact and every existing receipt ancestor
must be free of symlinks before it creates any output.

Only pytest exit `0` without failed/error cases or exit `1` with a failed/error
case can be retained. Exits `2..255` are refused, including green XML paired
with exit `2`. A retained failure stays failed; outcomes are never rewritten.
The 38 identities were derived statically from frozen Git sources, including
the imported retained fixture parameters, without product collection.

Private installer destinations use mode `0700`, with `0600` files. Existing
candidates must satisfy the same modes and exact bytes. Ancestors retain
the existing owner/write-bit safety policy; `0755` ancestors are allowed.

Use `route.py --config /absolute/qualified-config.json render` or `install
/absolute/private-candidate` with a reviewed receipt binding. `control
/absolute/new-output` uses that same qualified row with only the product
pytest invocation replaced by one harmless private pytest test; its JUnit
comes from pytest itself. `control --fail /absolute/new-output` exercises an
actual private assertion failure and returns exit `1`. These controls do not
qualify the 38 P5 cases. Receive them only with the explicit `--control` flag;
normal receipt acceptance refuses the one-case harmless membership.
Retain a completed normal service result with
`receive.py --config /absolute/qualified-config.json /absolute/service-output
/absolute/new-receipt.json`. Render, install, control, and receive all default
to the same checked-in qualified configuration and accept the same explicit
`--config` override. A pending configuration still refuses qualified work.

The service executes the row in a temporary snapshot whose tree equals the
frozen Runtime tree and whose parent is the frozen commit. Its `snap` file
names the original bound checkout. The row permits this exact snapshot
relationship and retains the original frozen source witnesses before cleanup.
Private controls execute the same row in the original checkout, with only
the product invocation replaced. They do not create a service registration
or authenticate an actual P5 result. The final tuple and P5 GO recorded by
the orchestrator remain inputs; independent source review precedes the body.
