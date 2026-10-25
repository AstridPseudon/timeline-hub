Implemented the strict native Undo oracle in the two assigned files. Ready for fresh independent protected review.

Base remains `ec78b6be2386550ee5709adb8d1ebe90bead64cb`.

| File | Final blob |
|---|---|
| `three-products.p2-elements-assets.spec.ts` | `b3776a294cb7724c762574aff6111aac3baeb066` |
| `support/p2-elements-assets-receipt.test.mjs` | `29b2237688139549cf0459ec91c9e8796720d559` |

The complete predicate replacement is:

| Previous check | Replacement |
|---|---|
| Native request structure | Exact envelope, `fields`, `reads:[]`, command, submitted step, scope/base, and independently identified Undo target |
| Structural reads/expect/authorship/selections/bindings | Exact values derived from canonical input and authenticated target captures |
| Any valid nonempty step patch/dependencies | Complete endpoint-derived effects and source-normalized captured dependencies |
| Recorder echoes and cardinality checks | Exact reversed writes, reads, selections, compiler dependencies, mirror effects, stage ranges, physical bindings, owners, revisions and digests |
| Structural accepted result | Exact expected data, restored canonical document/revision, identity map, versions and publisher |
| Reply/history echo fixtures | Independent native transcripts for parameters, element creation, asset registration and child placement |
| Native history relationships | Complete expected recorder, target `undo_of`, `undo_steps:null`, unchanged prior entries, and exactly one new entry |
| Missing native canonical correlation | Every Undo reads the actual Runtime history head and its canonical closure, then checks document and digest |

Native reads now follow the Agent’s actual `{ref,path,state}` ABI. The second element Undo also keeps its earlier target publication separate from its current landing base.

All existing `doc.patch` request/reply/history branches remain byte-identical, including atomic, omitted-read and nonempty-patch guards. Existing raw import/selection, registry/config, closure/manifest, sibling isolation, geometry, no-legacy, reload, waits and original selectors remain. Protected blobs match the assigned base and reviewer0149:

```text
tour          2a275b182f213dd7e0d33c4b4ffbf11fcf1f98ad
parent        0b12316aef58bf2ece3f43c1b7f4b7ff944432c9
media         da75f00ac541b8bd0c8dca6a32a0249f6296361f
semantic      f6829667a5a22d2b589c824c1293d1c6e8072768
popup spec    d7da4c234fb921c448bc18e9ac174b1a11dbc4a6
popup control d77ecc3c116453e3b0c1106580f7c5dd905114ea
geometry      bd8e51535f4cb6d783c8f8e268543d6abf13bace
```

Source investigation covered App `commitSession`, `commitOutbox`, `dataProvider`; Agent recording/inverse/effect projection; Runtime acceptance/history; C0; and the completed wholepath0218 report. App native producer files match normal `c101477597`. Runtime source was `6634a17f3ffd885567ba3c91b6c7a560df7375a4`. Agent advanced from `8dadab251a9b9c1a0d31655125d62338f1ee4482` to `bd3c95b1cebe3bf27c4a82919e5839efb37519db`; I inspected the intervening legacy-materialization validation change.

Verification used:

```bash
NODE=/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node
```

- `"$NODE" --import tsx --test --test-concurrency=1 --test-reporter=spec` with the receipt, media-import, parent and transition control files: **138 passed, zero failed/skipped**.
- `"$NODE" --test /tmp/w-94333c4a94/native-oracle/prior-red.test.mjs`: **5 original tests passed; 9 new mutation controls failed against the prior helper**, exit 1. Those mutations are rejected by the current helpers.
- `"$NODE" node_modules/vitest/vitest.mjs run --config /tmp/w-94333c4a94/native-oracle/vitest-bundled.mjs --configLoader runner --no-cache --no-file-parallelism`: **7 semantic + 11 geometry = 18 passed**, using the existing App graph and private cache.
- Root, App and Node `tsc -p <config> --noEmit --incremental false`, under `/home/user/work/.app-tsc.lock`: **all passed**.
- Scoped ESLint on both assigned files with `--max-warnings 0`: **passed**.
- `git diff --check`, exact scope and preservation comparisons: **passed**.
- Supplemental e2e type probe retained **30 existing diagnostics on both versions, zero added**.

Ledger: original run15897 reached readiness/registry/history/reload checks and failed at the native atomic predicate. Current green evidence is the source/control verification above; no browser, full suite, build or service run was performed.

No implementation blocker remains. P2 `commit-msg` and `DONE` are written. Recommended next step: fresh independent protected review, followed by the authorized original journey qualification.