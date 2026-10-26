# One decision for you: compact the hub repo (frees about 1–3 GB per machine)

## Why
Every machine runs at 4.4–4.7 GB free, just above the 4.0 GB stop line. That is now the main thing slowing the ZIP. Agent's full test runs on the new upstream need about 4.6 GB, and Agent is at 4.55 GB.

The cause is the shared hub repo. Its history is kept as individual loose files that were never compacted:
- 3.1 GiB of loose files on the Agent machine;
- 1.3 GiB on this machine.

## What the tool does
`bin/hub-repack` packs those loose files into compressed packs. It deletes nothing that isn't safely kept elsewhere first:
- **It waits for the hub sync.** It runs under the hub sync's lock, so the two never run at once.
- **It won't run during tests.** If any test run is going, it does nothing.
- **It works in small batches.** Each batch runs only while free disk is at least 4.3 GB, because a pack is written before anything is removed.
- **Copies are removed only after a check.** For each batch, the tool checks the new pack and confirms every file in the batch is inside it. Only then does it remove the loose copies. Nothing is lost.
- **Each run is logged** in that machine's deletion ledger.

I tested it on a throwaway repo. All 150 objects were identical afterwards and the repo check was clean.

## Why I need you
Removing the loose copies counts as a deletion under your rule. Your delegation to me doesn't cover deletions, and an approval only counts if you type it in that machine's session. If you want this, paste the line below into **each** session where you want it (Agent first, then App, Farm and this one):

> I approve running the kit's guarded `bin/hub-repack <area>` once on this machine now (lossless git pack + prune-packed under the hub-sync lock, as described in design/owner-ask-20261026T0450Z-hub-repack.md).

Replace `<area>` with agent, app, farm or runtime. If you don't approve, everything keeps going, just more slowly: the full runs wait until there is enough disk.
