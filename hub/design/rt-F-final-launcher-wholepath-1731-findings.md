# F-final launcher continuation findings

## F1 — current source11 delivery rows still omit sibling import setup

The actual registry and the current `runtime-final-service-rows.txt` both use
the hash-checked `python3 -c` body ending in `exec(...)`; neither delivery row
contains `sys.path.insert(0,str(p.parent))`. The caller remains
`run-final-delivery.py` SHA `0a043d1c...`, whose first non-stdlib import is
`from delivery_lifecycle import run_delivery` at line 23. The service shell
sets `PYTHONPATH` only to the detached Runtime snapshot, not the candidate
directory. This is the known actual10589 `ModuleNotFoundError`, exit 1, before
`run_delivery`.

Minimal reusable seam: preserve the existing regular-file check, caller SHA
check, argv rewrite, source/gate/lifecycle/D68 guards, and all existing args;
insert `sys.path.insert(0,str(p.parent))` in the same production hash-checked
exec immediately before `exec`. The 1719 author row demonstrates this exact
minimal seam. `installer.load_runner` is only a validation/in-process seam and
cannot substitute for the registered row.

## F2 — earlier 1719 successor has malformed dry-run argv

The prior private successor inserted the import setup in both delivery rows,
but its `delivery-v2-dryrun` row points `--wrapper` at
`candidate/delivery-v2-receipt.json` and omits `--wrapper-sha`, `--builder`,
`--builder-sha`, and `--receipt`. It therefore cannot reach the dry-run caller
with the reviewed required arguments. The protected review’s FAIL remains
controlling; no repair was made here.

## F3 — current installer preimage is stale against the actual registry

`candidate/install-final-services.py` declares
`REGISTRY_SHA256=7b1ffdd7...`; the immutable actual registry hash is
`0495919f9ab694d034ca53d77877c90d5553560ac3bbcbf7e90e8b268e227e15`.
The exact read-only no-install CLI fails with:

```text
ValueError: predecessor registry hash mismatch: 0495919f... != 7b1ffdd7...
```

The seven selected old Runtime row hashes do match, and the three current
candidate row constants match their candidate bytes. The full-registry
preimage pin is nevertheless stale, so the installer cannot qualify or reach
its install path against the actual registry.

## F4 — exact installer CLI cannot reach activation with copied tuple files

The candidate already contains concrete, regular, non-symlink tuple files:

- `final-source-tuple.json`, mode 0644, SHA
  `90b9da111d31a6f866795332521b6b6c660c1bfd2a9da92ee0c6d97683c1a561`;
- `final-gate-tuple.json`, mode 0644, SHA
  `eec639784d85238545dfa244d4c8f79a7385f9d946f0453dc12115e5b8dbbec8`.

`install()` rejects either existing path before writing. The exact CLI shape is
the candidate installer with `--registry`, `--candidate`, `--builder`,
`--source-tuple`, `--gate-tuple`, `--backup`, and `--install`; against the
actual registry it currently stops earlier at F3. If the registry preimage is
repaired, it reaches the existing-tuple refusal. The private receiving control
rebinds `installer.FINAL_TUPLE` and `installer.GATE_TUPLE` to a temporary
directory, so its PASS proves only private CAS mechanics, not unchanged CLI
reachability.

## Controls audited with no additional intrinsic defect

- The current candidate’s dry-run row has the full reviewed wrapper, wrapper
  hash, builder, builder hash, receipt, `--dry-run`, repositories, and extra
  tails. Its defect is the missing import setup, not the prior missing-argv
  defect.
- Current source, gate, wrapper, caller, lifecycle, core runner, inventory,
  and builder bindings are regular non-symlink paths. Candidate closure hashes
  and modes match its source manifest; all candidate files are UID/GID 0 with
  expected modes.
- Source tuple roots bind exactly to the recorded four worktrees, heads, and
  trees; those worktrees were clean at read time. The actual registry is a
  regular mode-0600 file with the immutable `0495919f...` SHA.
- Static side-effect review found installer writes only after its preimage,
  artifact, tuple, backup, and source/gate guards. No write path was invoked.

The original actual10589 failure, the first protected-review FAIL, all prior
guards, and all prior source/control/review receipts remain preserved and are
not reclassified.
