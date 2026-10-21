# Partial-crop retention assertion map

The only product-tree change is the final three-line output carrier in
`tests/packs/rendering/presenter_crop_capture.py::test_actual_registered_presenter_partial_crop_pixels`.
It runs after every existing assertion and serializes values already computed
by that test; it does not alter an assertion or calculate a second comparison.

## Existing assertions retained

| Area | Explicit 799 px node | Partial 697 px node |
|---|---|---|
| Central admission and held browser lock | `VIEWING_CROP_CENTRAL`, nonblocking `flock` refusal | unchanged |
| Registered source/frames | `_capture` uses the registered presenter; frames `0,3,4,5`; four PNGs | unchanged |
| Input/format | explicit params, `(640,360)` PNG size/format, frame-zero row, presenter clip | partial `{x,y}` input, same guards |
| Geometry | old/compat `(298,202,345,219)`, erase `(300,206,343,215)`, areas `799/799/387` | private `(298,202,339,219)`, compat/erase unchanged, areas `697/799/387` |
| Pixel registration | old/compat crop bytes equal; crop self-comparisons zero | private crop equals the public crop restricted to private width |
| Natural comparator | every crop has a strict `>.02` change pair; 799 old/compat verdicts agree | every crop has a strict `>.02` change pair |
| Planted controls | counts `8,15,16,20`; old/compat threshold at `16`; erase always above | counts `8,15,16,20`; private threshold at `15`, compat at `16`, erase always above |
| Padding/mismatch | padding16 is `16/799` for old+compat and zero for erase; planted points avoid erase | padding16 is `16/697`, `16/799`, zero; strict boundary remains |
| Source/cleanup | helper subprocess cleanup, browser close, build cleanup, source and PNG SHA checks | unchanged |

The existing pure geometry suite continues to cover natural, boundary,
padding, mismatch, source/public13, frame-zero, registration, and cleanup
contracts. Collection of `presenter_crop_capture.py` remains exactly two
tests; the future runner selects only the partial node.

## New retention-only behavior

The partial test prints one compact JSON line containing `png_sha256`, crop
tuples, natural pair fractions, and planted scalar controls. The future
runner captures that line, copies the exact four PNGs and `inspection.json`
from the owned pytest scratch tree into the worker result directory, checks
`cmp`, SHA-256, regular-file link count, distinct source/destination inode,
destination realpaths, and writes a checksum list. Its EXIT trap removes only
the ordinary scratch tree. The pure `--retention-control` branch refuses a
foreign destination, a symlink leaf, and a symlink ancestor.
