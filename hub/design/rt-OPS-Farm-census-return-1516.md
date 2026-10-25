# OPS Farm census return 1516

## Result

The published diagnostic is read-only, bounded, and ready for independent review. The actual Farm census is `EXACTMISSING`, not `PASS` or `COMPLETE`: the exact retained `a4e016` child root, `/home/user/work/bench-store`, and dependency child-root inputs are absent here. The prior flat refusal log remains observed separately at:

`farm-childvenv-a4e016-REFUSED-unowned-retained-source-directory-20261025T1452Z.txt`, SHA-256 `907094a18ae5773692ce67d5394611835cb781ed5513f4d1c16d420b864e40ac`.

The diagnostic does not reconstruct the child, use the old 9ea/369 layout, install, build, reissue, register, or execute installed content.

## Coverage

The exact installed source was read and hashed before/after the census. The source inventory found:

- embedded `STORE_VERIFY`: 46 `fail()` sites;
- `bench_store.py`: 121 `check()` calls and the Store construction/ensure/registration/projection path;
- `verify_dependency_seed.py`: 143 `fail()` sites and the installed/bootstrap/Farm verification modes;
- maker call graph: all required links to the three verifier layers were present.

The diagnostic reports visited, refused, skipped, and error boundaries independently. It does not infer that a later guard ran after a missing interpreter, missing root, exception, or limit. Limits are a 20-minute monotonic deadline, 100,000 entries, 512 MiB read budget, 16 MiB per file, and 8 MiB report output; any cap is `INCOMPLETE`.

The source-carrier allowlist is derived from exact installed `e62f` source: authenticated committed files below `.child-venv-source-*/{agent,runtime,schema}` or authenticated `.source-inputs/{agent,runtime,schema}.tar`, with only manifest-implied parent directories. No narrow remedial fix is proved from the refusal string alone because the log omits the offending path; no production edit is proposed.

## Focused evidence

The private fixture observed simultaneous hardlink, symlink, and writable-path failures without importing or executing installed content. A second fixture with a caller-bound but absent dependency wheelhouse returned explicit `EXACTMISSING`. These are limited diagnostic probes, not Farm-root evidence.

## Supported invocation and minimum inputs

```text
python3 rt-OPS-Farm-census-return-1516.py \
  --maker <installed e62f make-child-venv> \
  --root <actual retained a4e016 staged child root> \
  --client '<PACKAGES/PYTHON/ASTRID_RUNTIME_CLIENT_PATH=SHA256_LINES>' \
  --agent-checkout <authenticated physical Agent checkout> --agent-sha a4e016b6a9f91fbe372672bdcf382c630bf59186 \
  --runtime-checkout <authenticated physical Runtime checkout> --runtime-sha 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344 \
  --work-root /home/user/work --python python3.13 --staging --output <safe output>
```

Farm must retain the exact child root, normal Store `owner/index/entry/lock/marker` metadata, all distribution `RECORD`/`METADATA`/`WHEEL`/`direct_url.json` rows, the authenticated source carrier and manifests, and any caller-bound dependency/bootstrap inventories. No alternate route is supported.

Exact commands, exits, hashes, and probe receipts are in `rt-OPS-Farm-census-return-1516/evidence/receipts.md`.
