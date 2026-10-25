# Future D139a CAS installation recipe

This is a future manager-only command. It was not run by this source join.
The normal operational caller is the existing maker/checker route:
`apply-reviewed-maker.sh` invokes `verify_gate_artifacts.py` for the supplied
decision, extracts `ops-child-custody/make-child-venv` from the exact reviewed
source commit, and performs the descriptor-bound CAS replacement. The checker
and canonical census CLI are diagnostic/source controls, not an alternate
installer route.

## Exact command

```sh
ORCH=/approved/orch/root \
SOURCE_CHECKOUT=/approved/composition/checkout \
TMPDIR=/approved/private/tmp \
D137_DECISION=/approved/gates/d137-decision.json \
bash ops-child-custody/install-prep/apply-reviewed-maker.sh
```

Required source and target paths:

- source: `$SOURCE_CHECKOUT/ops-child-custody/make-child-venv`
- target: `$ORCH/bin/make-child-venv`
- backup: `$ORCH/backups/make-child-venv.$STAMP.bak`
- lock: `$ORCH/bin/.make-child-venv.install.lock`
- private extraction: `$TMPDIR/ops-inventory-install.XXXXXX/ops-child-custody/make-child-venv`

The source candidate must be exactly
`fd83c9e2017f75fb0d76a2d633d4a63aed090df37c4d7417b03152e7a4fc22b5` / 111171
bytes / mode 0755. The predecessor target must be a regular, non-symlink,
single-link file exactly
`f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f` / 75541
bytes / mode 0755. The timestamped predecessor backup is also regular,
non-symlink, single-link, owned by the invoking user, and mode 0755; an
existing backup path refuses rather than clobbers it. The target is checked
again under the receiving lock for device/inode identity before atomic rename.

## Genuine evidence required before and after

The manager must supply a genuine D137 decision JSON accepted by
`verify_gate_artifacts.py`: `authorization=D137`, fixture gate WITHDRAWN,
`e2e_result=NOTRUN`, `e2e_pass=false`, `install_route=CAS_MANAGER_ONLY`,
`production_install=false`, exact candidate/preimage hashes and sizes,
`reviewed_installer=installer1826`, and an exact 40-hex `source_commit`.
The source checkout must be clean and the pinned installed schema input must
be authenticated from the genuine Agent environment by its 18-row RECORD
closure (12 hashed rows plus the six named unhashed rows), pinned direct URL,
and D139a route. `tree_tie=UNAVAILABLE` remains disclosed until a genuine
pinned source object is actually held; no acquisition is implied here.

After a successful install, retain the exact candidate, preimage, backup,
target readback, protected helper hashes, source commit, receipt status, and
the kit propagation receipt. If a final-review receipt is still required,
its precise name is the genuine manager-supplied **D139a combined kit
receipt** (including the final-review/D137 decision input and post-install
readback); no such receipt is created by this task.

## Expected propagation route

The manager installs the reviewed maker into the approved ORCH kit, runs the
normal kit verification/registration path, then propagates that same sealed
kit identity to the Agent child venue and Farm/Runtime consumers through the
existing reviewed handoff. The Agent installed schema RECORD closure is the
genuine future input. No child/core run, Store publication, registration, or
provider acceptance is claimed by this join.
