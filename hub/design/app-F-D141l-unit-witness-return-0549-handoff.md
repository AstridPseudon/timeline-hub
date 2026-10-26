# D141l corrected witness normalization

The corrected source qualification is `SOURCE_QUALIFIED_UNDER_MAIN` with the
finite bracket `5433016320 - 4839120896 = 593895424` and floor
`4793895424` bytes. The retained controller admission is the permitted
same-controller bracket start; the normal full-run `df -B1` row at
`00:48:37Z`, byte offset `1157219`, is the in-body stop. The pristine
timestamped comparator delta is `11431936` bytes and does not enlarge the
normal bound. Sampling gaps remain unobserved and no continuous peak is claimed.

`normalized-start.df` and `normalized-stop.df` are deliberately derived data
projections for the existing `timeline.d89d.measured-floor.v1` input format.
They are not original stdout and do not create a historical sample or a new
consumption measurement. `normalization.json` records the exact raw source
field/row, absolute source, hash, byte range, time, extraction rule, output
bytes, and output hash. The raw admission, closed manager logs, run result
records, and custody metadata were not modified.

The installed validator was run directly once in an isolated private fixture
under `$TMPDIR`, with manager-root ownership checks intact, actual App
`4de54db14bdc9ddc2ce2e5887258b03acbffd30d` / tree
`84c3fb7f73f08c22220f8e808962fe3f24aaa0aa`, schema
`timeline.d89d.measured-floor.v1`, and the retained registered command
`npm test -- --maxWorkers=3`. This was only a data-format control; no
`test-run`, test body, service request, receipt attachment, or live ID was used.

The default heavy floor remains `5200000000` until a manager accepts this
corrected data and a later controller attaches a real supported job receipt.
Current available space below `4793895424` admits no body; D130/D141 stops and
all raw KEEP/private ownership gates remain unchanged.
