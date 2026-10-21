# Partial-crop retention review assertion map

| Contract | Evidence and verdict |
|---|---|
| Existing explicit 799 px behavior | Reused 0901/0912/0916 evidence; not rerun. Natural pairs, threshold, padding16, mismatch, registration, source, public13, Node, frame0, and cleanup remain unchanged. |
| Existing partial 697 px behavior | Reused 0916 pure/collection evidence; no physical qualification claimed. Natural pairs, threshold, padding16, mismatch, registration, source, public13, Node, frame0, and cleanup remain unchanged. |
| Compact result serialization | Three output-only lines after all partial assertions; values are existing PNG hashes, crop tuples, natural fractions, and planted controls. No second oracle. |
| Selection | Collection is 2; future physical selection is 1 partial node; explicit physical node is not replayed. |
| Raw retention | Four PNGs and `inspection.json` are copied from the owned pytest scratch before the EXIT trap removes only that scratch. SHA-256, `cmp`, regular-file link count, distinct inode, and destination realpath checks are present. |
| Destination custody | Foreign, symlink-leaf, and symlink-ancestor destinations are rejected; worker/result ancestry resolves without symlinks. |

This review did not run a browser, helper, renderer, socket, central suite,
Runtime, Node host, install, full suite, or physical capture.
