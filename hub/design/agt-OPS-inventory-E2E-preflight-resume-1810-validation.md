# D128/F validation

- `bash -n` passed for the durable wrapper and its TMPDIR copy.
- Exact numeric parser passed real `df` output (`6707691520` bytes at preflight),
  representative header/data output, and rejection cases for missing,
  noninteger, multiple, and negative values.
- Start reserve `5905580032` bytes and stop line `4000000000` bytes were kept
  unchanged.
- Source1747 runner/manifest, protected helper, candidate maker, and qualified
  local wheel hashes passed read-only guards.
- The one service terminal result was exit 1 with an empty log. Its first
  boundary was the wrapper's initial executable check: missing
  `/home/user/work/venv-runtime/bin/python`.
- No input writer, offline wheel build, fixture Git commit, Store initialization,
  maker, verifier, registration, network acquisition, or production request ran.
