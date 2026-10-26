> **Superseded (26 Oct, 20:00 UTC).** The current, self-contained version is in `../followups/` (start at `followups/README.md`). This file is kept as a source only.

# Follow-up: editing-tool trust fixes

Source: chat-33 assessment.
- **One counter:** diff, status and publish share a single change counter. The working-copy diff reports "1204 clip changes" for 1 (cli.py:1522 compares the split head against the flattened working copy). This overlaps shot-layering `differences()` normalisation (§3.2).
- **`--gap-after`:** limit it to the named line. Today `tl.reflow()` re-applies every line's gap.
- **SDK `Checkout...set()`:** use bounded memory and fail loudly. Today it keeps two full timeline JSON copies per set() (checkout.py:812-818), and was killed with exit 137 without saving.
- **Whole-array re-anchor:** warn when a whole-array set clears per-entry offsets (model.py:660).
- **am-discord schema:** declare `composer`.
