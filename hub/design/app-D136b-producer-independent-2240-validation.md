# D136b independent validation

Result: PASS. Static-only validation; no product imports or execution.

Commands run:

```text
python3 - <<'PY'
  stdlib ast/hashlib/json/pathlib/subprocess audit of source-manifest.json,
  producer-map.json, classification.json, immutable joined Agent source,
  immutable Runtime ab1e source, exact AST definitions/call sites/guards,
  boundary spans, predicates, test bodies, conservation, and referenced hashes
PY
```

Result: `PASS independent static audit: 25 immutable source hashes/line counts; 24 ASTs; 52 node citations; 43 exact call sites/guards; 15 boundary spans; 43 predicates; 11 bodies; 135 UNKNOWN; 50 referenced packet hashes; clean Agent worktree.`

```text
git diff --check
```

Result: PASS.

```text
git status --short --branch
```

Result: clean `tl/app-D136b-producer-independent-2240` worktree.

The audit read source with `git show` from the joined Agent source and Runtime immutable ab1e; it did not checkout, import, or execute product code. The Runtime tree identity matched the supplied manifest. No full, targeted, collection, pytest, browser, service, or comparison suite was run or requested.
