# D139a installed-custody validation

## Source and installation identity

Commands:

```text
git status --short --branch
git rev-parse HEAD
git rev-parse HEAD^{tree}
git diff --quiet
sha256sum ops-child-custody/make-child-venv ops-child-custody/request-child-venv ops-child-custody/check-child-imports ops-child-custody/install-prep/install_atomic.py
```

Result: PASS. The source is clean at commit
`0921ec1c8eb7cab668203963c5a5eeb0e4616c00`, tree
`577a3cca4e23c94d051e839eb47d7b1bd7a1c9c3`; source hashes are the reviewed
maker `fd83c9e2…4fc22b5`, wrapper `60d2238a…412504`, checker
`8215f5d9…a272d7c`, and helper `81eb0818…60ef9`.

Installed readback:

```text
stat -c '%n type=%F mode=%a links=%h uid=%u bytes=%s' \
  "$ORCH/bin/make-child-venv" "$ORCH/bin/request-child-venv" \
  "$ORCH/bin/check-child-imports" "$ORCH/bin/bench_store.py" \
  "$ORCH/bin/verify_dependency_seed.py" \
  "$ORCH/backups/make-child-venv.20261025T231036Z.bak" \
  "$ORCH/backups/request-child-venv.20261025T231055Z.bak"
sha256sum <same paths>
find "$ORCH/bin" -maxdepth 1 -name '.*install.lock' -print
```

Result: PASS. All installed targets and backups are regular single-link,
non-symlink, mode 0755, owner UID 0; the lock listing is empty. Installed and
source bytes match exactly. Maker and wrapper backups match the f07 and bdda
authorized preimages. Protected helper hashes are unchanged.

The prior backup hashes were compared with the earlier D137 receipts; all
recorded prior backups remained unchanged. The checker’s initial absence is
historical receipt evidence only because the target now exists.

## Gate and receiving controls

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  ops-child-custody/install-prep/verify_gate_artifacts.py \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-D139a-combined-CAS-install-2309/evidence/d137-decision.json
```

Result: PASS. The receipt is authorized D137, WITHDRAWN/NOTRUN with
`e2e_pass=false`, CAS_MANAGER_ONLY, and `production_install=false`.

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B - "$TMPROOT" \
  ops-child-custody/install-prep/install_atomic.py <<'PY'
  # copy() controls against private regular source and destinations:
  # symlink destination, existing destination/no-clobber, and wrong-preimage
PY
```

Result: PASS. Symlink destination and existing-backup controls refused with
nonzero status without clobbering; wrong-preimage hash mismatch refused before
any helper write. No real target was replaced.

## Installed-byte bounded tests

```text
bash -n "$ORCH/bin/make-child-venv" "$ORCH/bin/request-child-venv"
```

Result: PASS.

An inline Python control extracted the seven named blocks from the installed
maker (`STORE_PY`, `STORE_VERIFY`, `STAGING_INVENTORY`, `RELOCATE`,
`PROVENANCE_SCRIPT`, `DIST_METADATA_SCRIPT`, `IDENTITY_SCRIPT`) and ran
`compile(..., 'exec')` for each. Result: PASS 7/7.

The same inline control executed the installed maker’s serialized
`run_stage` boundary with private temporary roots:

- `install-agent`: exit 17, exact stderr retained privately at mode 0600,
  payload-free bounded public failure marker.
- `pinned-requirements`: timeout exit 124, exact stderr retained privately at
  mode 0600, payload-free bounded public failure marker.

Wrapper controls used the existing test module against the installed wrapper,
without live queue or Store:

```text
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-c5d08e0b31 \
PYTHONPATH=ops-child-custody/tests \
/home/user/work/venv-runtime/bin/python - "$ORCH/bin/request-child-venv" <<'PY'
  # set test_request_schema_carrier.REQUESTER to the installed wrapper;
  # run RequestSchemaCarrierTests
PY
```

Result: PASS 5/5. Canonical schema pair/source-carrier emission, dispatcher
word-split delivery, malformed/duplicate/partial/unsafe/conflicting refusal,
legacy no-schema shape, and no legacy same-name reuse all passed.

Read-only genuine installed-schema admission used the installed maker’s
admission block with the real
`/home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema-0.0.2.dist-info`
and a private manifest copy:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B - "$ORCH/bin/make-child-venv" "$TMPROOT"
```

Result: PASS. Input kind `installed_distribution`, RECORD 18 rows, 12 hashed
rows, six named unhashed rows, `tree_tie=UNAVAILABLE`; no acquisition or Store
mutation.

Canonical checker diagnostic:

```text
/usr/bin/python3.13 "$ORCH/bin/check-child-imports" \
  --child /usr/bin/python3.13 \
  --launcher /home/user/work/agent/tools/p4-d73-pinned-launch.sh \
  --census-file "$ORCH/design/agt-F-D139-import-input-census-2149-input-census.json" \
  --output "$TMPROOT/checker-result.json"
```

Result: expected exit 1. Output has 1146 census rows, 22 attempted probes,
12 missing canonical names, 12 failures, and an empty
`missing_installed_distributions` list. Status is diagnostic failure; it is
not real-child acceptance.

Static normal-caller checks also passed: installed wrapper parser/emitter,
normal `queue/pending/childvenv-$N` key, source-carrier pair, maker schema
parser, schema source/manifest forwarding, and
`__timeline_schema_identity__` Store-key binding.

No 63/44 review suite, Store whole-make, live request, child, venv,
registration, provider, browser, Farm, D130, or full suite was run. A first
ad hoc schema runner omitted its `tempfile` import; the corrected bounded
command above passed and no product or installed file changed.
