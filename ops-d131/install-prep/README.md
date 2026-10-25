# D139 private retirement candidate — NOTREADY

The candidate is deliberately private until an independent review and an
atomic backup/CAS installation.  `retire_entry.py` is the only manager-facing
wrapper.  It accepts one exact `entry` and one owner-bound authorization JSON;
there is no force or age-only option.

Future manager shape (fixture-only until installed):

```sh
python3 ops-d131/retire_entry.py \
  --root /home/user/work/bench-store \
  --tests-dir /home/user/work/tests \
  --entry child-<64-hex-key> \
  --authorization /path/to/owner-retirement-audit.json
```

The authorization binds the owner, identity, path, entry and lease in the
candidate index. The exclusive lease excludes consumers using `Store.acquire`
through deletion and journal recovery. The test service uses that admission
route. Worker/queue/service and KEEP/ACTIVE producers have no shared admission
contract with this Store. `activity.json` is mutable self-consistency data;
its hash does not establish lifecycle authority. Quarantine and `/proc` scans
cannot exclude a new cwd, fd, command-line reference or marker after the final
observation. D139-F1/F2/F3 remain UNAPPLIED. Do not install or use this candidate
for live cleanup. Closing those findings requires an owner decision about
the cross-process admission contract and its producers/consumers.

The ordinary required guards remain age, the owner's not-before boundary,
KEEP/ACTIVE, real references, processes, leases, source identity, ownership,
locks, journal and rollback. These requirements have not been waived. They
are distinct from a stronger guarantee against arbitrary same-UID rewriting
of all persisted state; neither the file hashes nor advisory locks provide
that guarantee. The fixed-two `ensure` retention policy is unchanged.

New retirement receipts carry a `source` with the exact pre-retirement sequence,
affected registration records and their dependency entry records. The normal
retirement caller creates it from the locked index; recovery compares it with
the journal's exact before-index. After journal completion the loader validates
the source's owner, paths, identities, locks, ages, registration hashes and
dependency closure, then requires every flattened receipt field, registration
name and suite pair to match it. Registration/suite ownership cannot overlap
other receipts, and a receipt cannot claim a live entry's sequence. This checks
cross-association corruption; it is not authentication against coordinated
rewrites of the receipt and its retained source.

Receipts from the earlier private candidate lacking `source` are refused;
no historical fields are synthesized. The actual installed `123bb` Store also
lacks `owner.activity`, `activity.json`, entry `registered_at`/`not_before`, and
registration `anchor`/age fields. It is refused at owner/entry schema checks.
There is no migration or adoption route in this patch. In particular the
historical child `3e16336b…` remains SOURCEONLY/NOTREADY for cleanup, with no disk
fix established. The owner's 22:18 direction retains the not-before boundary
`2026-10-25T22:24:50Z` and all ordinary guards; passing that time alone grants
no retirement authority.

`check-cas.sh` is a read-only preflight for the expected installed-source
preimage `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2`
and mode `0755`; it performs no backup, install, Store operation or cleanup.
