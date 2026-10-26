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
