# F/D141b validation

Disposition: `PASS_SOURCE_READY`.

The packet is static and source-only. No pytest, collection, import, socket,
request-test, request-checkout, suite installation, or body execution was run.

Checks performed:

- `bash -n evidence/command.sh` — required; command has no Python operational
  source and therefore no Ruff or `py_compile` check applies.
- `jq empty evidence/source-manifest.json evidence/admission.json` — PASS.
- Final command/row SHA guards, exhaustive root membership, pytest settings,
  and the five `git cat-file`/`git ls-tree` absence checks — PASS.
- Frozen Agent, Runtime, App, and Composition checkout receipts were read from
  the actual `queue/done` paths named in `source-manifest.json`; all four
  pinned paths were checked clean.
- Frozen Agent SHA/tree and the current authoring base SHA/tree were checked;
  the command never uses the current base as test source.
- The exact 17-root inventory was checked with `git ls-tree`; inventory hash:
  `b1f106c00a6d40804082192e160c80718227acb85af38df2bbebec382411b820`.
- Each exact excluded root was checked with `git cat-file -e HEAD:<root>`
  (exit `128`) and `git ls-tree` (zero lines).
- JSON syntax, source SHA/tree fields, root membership, pytest settings, clean
  checkout state, exact interpreter path/version guards, separate 4.6 GB source
  admission and 4.7 GB body-dispatch floors, and the 4.0 GB stop threshold were
  checked.
- The candidate row is documented only in `service-row.txt`; it was not added
  to `tests/suites.conf` and no service was submitted.
- Final SHA guards are bound after the durable publication copy is verified;
  the exact values are recorded in `admission.json`.

The wrapper records durable command, interpreter, source-before/source-after,
disk, status, separate raw stdout and raw stderr, a combined compatibility log,
body and monitor exit witnesses, and JUnit XML under the fixed manager run path.
It refuses unless both manager-installed PASS gate markers exist, admits the
source only at `>=4600000000` bytes, dispatches the body only at
`>=4700000000` bytes, stops the body below `4000000000` bytes, and holds one
heavy-body lock. An unreadable monitor measurement terminates the wrapper-owned
body and returns a failure status.

Unsupported or intentionally deferred:

- The actual U2 final-freeze receipt and independent reviewer PASS are future
  controller inputs; the body is not admitted by this source worker.
- No Farm result exists in this packet, so no REG or ship credit is inferred.
