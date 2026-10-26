# D141 P5 cut route

This is a private, installable route description for the P5 acceptance cut.
It has no service registration and does not launch Runtime, Agent, a product
test, or a renderer. The route remains pending until a reviewed final Agent
cut receipt supplies the actual checkout, commit, tree, provider/client
origins, schema metadata, and lock values.

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
argv, source hashes, testcase IDs/counts/outcomes, raw exits, disk and KEEP
witnesses. Every required artifact and every existing receipt ancestor
must be free of symlinks before it creates any output.

Private installer destinations use mode `0700`, with `0600` files. Existing
candidates must satisfy the same modes and exact bytes. Ancestors retain
the existing owner/write-bit safety policy; `0755` ancestors are allowed.

Use `route.py --config /absolute/qualified-config.json render` or `install
/absolute/private-candidate` with a reviewed receipt binding. `control
/absolute/new-output` uses that same qualified row with only the product
pytest invocation replaced by one harmless private pytest test; its JUnit
comes from pytest itself. These controls do not qualify the 38 P5 cases.
Retain a completed normal service result with
`receive.py /absolute/service-output /absolute/new-receipt.json`.
The checked-in pending configuration still refuses rendering/installing
or running a qualified control until its receipt is supplied.
