# D141 Farm input-producer commands

This is a source-only receiving packet. It does not run Farm census, child,
imports, controls, services, core, Store, acquisition, or Git operations.
Every command below is an owner command to run at the normal venue after the
named source is supplied. A missing input remains `NOT_READY`.

## Frozen source and producer identities

```sh
# Read-only source custody, in each owning checkout:
for row in \
  "/home/user/work/wt/agt-pin-28e56cac 28e56cacb42d3da85b02e5b3543895b44f3d0f70 2ebe2ddf5a61f013953ab1e21d51ebaab746e58a" \
  "/home/user/work/runtime 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d ac5b862744bece65b2e30565db1777bacd60da28" \
  "/home/user/work/app 867cb2737af1b46dc608c7cd37c349e920fe9422 2b44a46ca51d880c6a00da4c19aa8629b55eb7dd" \
  "/home/user/work/composition 635f4de06fda22a85fc2e4cfc764d0153a4c9f40 5ab5191a296980a0a6bcd1178ab6902d6478a148"; do
  set -- $row
  git -C "$1" rev-parse HEAD HEAD^{tree}
  git -C "$1" status --porcelain --untracked-files=all
done

# Existing reviewed operational sources; read and hash, never replace shared files:
sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/{make-child-venv,request-child-venv,check-child-imports,verify_dependency_seed.py,verify_farm_distribution_inputs.py}
```

The expected maker/requester/checker are respectively `fd83c9e2…` (111171
bytes, 0755), `60d2238a…` (18066 bytes, 0755), and `8215f5d9…` (14033 bytes,
0755). The seed verifier is `116b4e6b…`; the Farm distribution verifier is
`c2163184…` and is not an installed dependency seed.

## Owner supply commands

1. D139a kit owner: publish the genuine CAS2309/installed2314 summary and
   installation receipt. The receiver consumes them through
   `FARM_INSTALLED_KIT_SUMMARY` and `FARM_KIT_INSTALLATION`; do not bind the
   historical D137 JSON as current evidence.

2. D139a schema owner: bind the already-installed physical distribution and
   adjacent files, then verify them without acquisition:

   ```sh
   SCHEMA_INSTALLED_DISTRIBUTION=/approved/physical/banodoco_timeline_schema-0.0.2.dist-info
   SCHEMA_RECORD_CLOSURE="$SCHEMA_INSTALLED_DISTRIBUTION/RECORD"
   SCHEMA_DIRECT_URL="$SCHEMA_INSTALLED_DISTRIBUTION/direct_url.json"
   SCHEMA_SOURCE_MANIFEST=/approved/physical/d139a-schema-source-manifest.json
   ```

   The values must close to ArtAgents commit
   `242f9c4306bf3b501222cb041a9eb246ef47bc85`, subdirectory
   `packages/timeline-schema/python`, tree
   `75a5a697f630affee40632e500b3f5b704a9b834`; `RECORD` must have 18 rows,
   12 hashed rows and the six named unhashed rows. This is the physical
   installed carrier, not a source checkout or a historical claim.

3. D139 census owner: provide the unchanged 2149 input census at its venue
   path and bind it:

   ```sh
   CANONICAL_CENSUS=/approved/physical/agt-F-D139-import-input-census-2149-input-census.json
   sha256sum "$CANONICAL_CENSUS"  # be9e8bc9c6d2411809da2d99126a9b3eef72678de2066bb6ad196d5d16ebcd30
   ```

   The 2216 packet is review/reconciliation provenance only; it is not a new
   census and must not be substituted.

4. Farm control-plane owner: bind the normal producer/control inputs. The
   dependency seed must be the original authenticated wheelhouse directory,
   not the bootstrap tgz:

   ```sh
   DEPENDENCY_SEED=/approved/farm/original67-wheelhouse
   CENTRAL_SERVICE=/approved/farm/central-service
   CENTRAL_SUITE=/approved/farm/central-suite.conf
   D73_DRY_ROUTE=/approved/farm/p4-d73-dry-route
   CORE_ROUTE=/approved/farm/agent-core-route
   PROFILE=/approved/farm/remotion-profile
   DISK_ADMISSION=/approved/farm/output/disk-admission.txt
   RETAINED_ROOT=/approved/farm/retained
   ```

   These are bindings, not permission to create guessed files. The D73 dry
   route must run the existing reviewed Agent launcher
   `tools/p4-d73-pinned-launch.sh` (SHA `9f668e39…`), and CORE_ROUTE must use
   the unchanged D124 command in `ops-d140-farm/commands.md:201-232`.

5. Farm receipt owner: bind the corrected full-SHA Composition receipt and
   digest from `evidence/qualified-inputs/`; request genuine Runtime/App
   checkout receipts through the normal `make-checkout` route rather than
   fabricating queue files.

## Normal route, once all pre-child inputs are real

```sh
"$NORMAL_REQUEST_ROUTE" venv-agent-child-d140 "$AGENT_SHA" \
  --source-carrier "$AGENT_CHECKOUT" "$RUNTIME_CHECKOUT" "$RUNTIME_SHA" \
  --dependency-wheelhouse "$DEPENDENCY_SEED" \
  --schema-installed-distribution "$SCHEMA_INSTALLED_DISTRIBUTION" \
  --schema-source-manifest "$SCHEMA_SOURCE_MANIFEST"
```

This is the only qualified child producer command. It is refused if the
installed schema is combined with Farm schema authority. After the normal
request, bind the actual child receipt/interpreter/bootstrap and run the
existing post-child census. Only a genuine import PASS permits the D134
positive/poison controls; only both controls and all retained inputs permit
the unchanged D124 core command. The full sequence remains in
`ops-d140-farm/commands.md`.
