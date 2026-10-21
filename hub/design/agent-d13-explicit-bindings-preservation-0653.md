# D13 explicit bindings preservation review

**REQUEST CHANGES / HOLD for `3547a9f24` (tree `adfe8294`).**

The fixture now has explicit manager-selected source, profile, wheel, and tool
inputs. It compares selected paths, source digest, wheel hash/member bytes,
tool hashes, installed origins, and the existing four-field profile without
adding authority fields. The original native positive, strict legacy xfail,
ownership/refusal/cleanup controls, and result/auth assertions remain.

Two issues prevent approval:

1. `agent_commit` and `agent_tree` are validated only as 40-hex strings; they
   are not compared to the selected installed source or wheel. The source/wheel
   comparison therefore does not prove the declared source commit/tree.
2. The merge parent `18a89a0d2` is not sufficient evidence of its contents.
   The resolved target and installed `6f2d8c350...` source use the first-parent
   `3df918ba...` custody and `d97a3124...` outbox files, not public 18a89’s
   `8df3369e...` custody cleanup and `144cfad3...` Runtime-platform outbox
   locking. WC8 and the active RLE positive are retained; doctor behavior is
   present, but the public missing-Runtime doctor regression is absent.

Current manager binding: Agent `6f2d8c350...`, tree `698ae4df...`, wheel
`fa2f824d...`, source digest `74bea6e5...`, and the selected private staging
venv/site-packages profile. Before refreshing that wheel, merge public
`98da6867` and `4b3a209f`, plus the required document-diff repair `fa36a85f4`
and its qualification companion where applicable, then regenerate the exact
binding. Targeted offline/preflight evidence is **4 passed in 2.06s**; no
native/Node/browser/daemon/full/18/688 run was performed.
