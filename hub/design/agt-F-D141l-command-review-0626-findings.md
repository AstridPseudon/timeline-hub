# F D141l command review — FAIL

The firstreturn0515 pair does not qualify under PLAN §3 F/U2. No authoring fix was made.

## F-D141L-001 — blocking: stale integrated tuple and false finite receiving

`command-cut.sh:110-113` and the author `source-manifest.json` pin integrated Agent `8585ed9c/tree92a3ff` and Runtime `6a011d/treeac5b`, while the final qualified normal tuple is Agent `ecdc242e/tree d362fe9d`, Runtime `95d98f/tree78df31`, App `4de54d/tree84c3fb`, Composition `635f4d/tree5ab519`. The current normal checkouts were read-only verified clean. The author packet therefore describes a stale checkout as finite `NOT_READY_RECEIVING`, although the genuine Agent U4a normal-home receipt `agent-U4a-D141-postREG-home-0622.json` exists and the normal Agent/Runtime paths have advanced. This is not the permitted missing-receipt/tool-receiving condition; the executable source needs another edit. The App receipt also embeds the old Agent binding.

## F-D141L-002 — blocking: pristine executable selection is not backed by source

The 17-root array in `command-pristine.sh:255+` names `tests/v10/timelines_create.py`. Direct source inspection of pristine Agent `64197afa/tree6c0488` found that path missing; the actual file is `tests/v10/test_timelines_create.py`. The other 16 listed roots exist. The author check only counts 17 regex lines (`check-source.py:94-95`) and never checks paths, so the claimed pristine collection is not executable source.

## F-D141L-003 — blocking: admission validation remains self-authorizable and imprecise

Both scripts accept a caller-supplied JSON file and validate only locally supplied fields (`command-cut.sh:152-193`, `command-pristine.sh:134-165`). They do not validate an existing request-test/test-run receipt record, exact service row/service identity, canonical receipt schema and producer, authenticated request/body hash, exact tuple/command/manifest/source-manifest/brief owner bindings, or immutable lifecycle state. `service_id` is printed but never checked. A fabricated JSON object with the expected strings and hashes can pass; this violates the no-self-authorized/no-invented-receipt-route requirement and the precise identity/binding requirement.

## F-D141L-004 — blocking: pristine manifest binding is miswired

`command-pristine.sh:134-155` passes `SOURCE_MANIFEST` as both the manifest and source-manifest argument. There is no distinct `MANIFEST` input or production command manifest in the pristine path. The validator therefore compares two hashes of the same file and cannot prove the required command-manifest/source-manifest distinction or their owner bindings. The token check accepts this because it only looks for `manifest_sha256` tokens.

## F-D141L-005 — blocking: required tiny-launcher result/dataflow is absent and current execution refuses

The expected positive stub hash is present (`38afc8a5...ca360ad0`), but `controls.json` says the positive/poison checks were `DEFINED_NOT_RUN_THIS_RETURN`. I ran the actual positive and agent-sha-only poison manifests against the existing stub in private scratch: both returned `rc=1`, `calls=0`, with `D73 launcher: agent SHA mismatch`, because the manifests still name stale Agent `8585ed9c`. Thus there is no evidence for the required positive `exit17/call1` and poison `exit1/call0` behavior on the actual qualified tuple. Token/presence checks cannot establish the required dataflow.

## F-D141L-006 — blocking: author check script cannot verify the claimed controls

The required invocation passed, but `check-source.py:39-47` verifies only frozen Git objects, `:49-79` performs syntax/JSON/hash/token assertions, `:81-82` checks only those frozen objects, and `:84-95` checks tokens and a root-line count. It does not execute either command, inspect actual root existence, parse the command AST/dataflow, validate adversarial receipts, invoke the admission route, or run the tiny launcher. It also does not verify current normal checkout identity. The script is therefore incapable of proving the controls it reports as PASS; under the review rule this is itself a finding.

## F-D141L-007 — blocking: custody and lifecycle controls do not close the claimed chain

The scripts create custody rows, but `check_custody` removes every hash line before comparison (`command-cut.sh:220-224`; same pattern in pristine), so source/raw/JUnit/trace/KEEP content changes are not detected. It checks existence rather than non-empty/parseable raw/JUnit data, exact mode/owner/immutable KEEP state, interpreter/runtime/service/caller records, or hash/dataflow linkage. `chmod` failures are ignored. In `finish`, status is written at `command-cut.sh:242-248` before final custody/checking at `:249-251`; a later evidence/custody failure can change the process exit while leaving `evidence_exit` in the already-written status stale. The same lifecycle pattern exists in pristine `:211-251`. This leaves the required source-before/after, raw/JUnit, durable KEEP, monitor/body/evidence exits, and cleanup/trap chain unproven even though the source contains the relevant token names.

## Preserved disclosures and non-findings

The D89d arithmetic in the packet is `4714564096` from dispatch `4826488832`, minimum `4311924736`, plus the 4 GiB and 0.2 GiB terms; the source also contains the 5-second trace and 4,000,000,000-byte stop tokens, one-heavy sequencing, no ownprep re-gate, and the requested `-n3/addopts cleared/no-cacheprovider/timeout45` settings. These are source declarations only because no production body or acceptance admission was run. Original sources `26496`, `27388`, and `10086` were read as retained inputs only. F009's historical pre-05:00:57 trace gap is disclosed and is not retroactively claimed as continuous. Old `19479` remains held/unstarted; no P4 scope was reviewed.
