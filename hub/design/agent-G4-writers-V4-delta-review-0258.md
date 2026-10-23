# Agent G4 writers V4 delta review

PASS for `d32744b33d4a87557d50b085557f11fe8abd02d2`.

The tree is exactly `fbd602303047aa104dff1c8be6b90543a5ba8fea`. Relative to
`135a1ab5a`, only the six approved V4 live-scenes paths are deleted; all other
blobs, including narration/update-element callers, word recipes, generated
client, lock, and manifest, are byte-identical. Targeted evidence is 42 writer
tests passed, 131 validation tests passed with 41 existing skips, 3 catalog
tests passed, current artifact manifest, exact official 21482 pin, Ruff
2150/2150, private mypy 1915/1915, and clean diff check.

Actual wire remains separately HELD at the known Runtime-owned text-binding
alias failure (10 pass/11 fail); it is not Agent acceptance evidence. The
official generated client’s known `merged` decoder defect is unchanged.
