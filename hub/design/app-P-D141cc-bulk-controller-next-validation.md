# D141cc bulk controller validation

## Result

`p2-transition-none-bulk@original` passed through the unchanged production D66 builder and normal service. Exactly one native `--submit` invocation created one preflight request and one normal request. The normal request passed with exit 0; the supported `wait-test` for that exact normal ID also exited 0.

## Exact evidence

- Recipe: `dispatches[3]` in `dispatch-recipes.json`, SHA-256 `d665c4907abd063edc9da0f29c887b56f7b66fb80febbe52f14732ea66e95d0d`.
- Native command: the JSON-derived argv/cwd/environment from that recipe; one invocation, exit 0.
- Preflight ID: `app-pin-82e9e13d-full-d141-p2-transition-none-bulk-82e9e13d-submit-preflight-1026113625-5394`, pass, exit 0.
- Normal ID: `app-pin-82e9e13d-full-d141-p2-transition-none-bulk-82e9e13d-submit-1026113655-27060`, pass, exit 0 in 220 seconds.
- Tests passed: D28 mounted readiness and `P2 mounted transition None bulk: atomic raw clears preserve unknown fields/order and guarded Undo`.
- Raw request `KEEP` markers were created immediately for both genuine IDs; the assigned output `KEEP` and worker `KEEP` were present before artifacts.

## Safety and limits

The four detached clean pins, builder SHA/blob, command/row hashes, and recipe environment were verified before the sole submit. The sampler recorded 73 foreground samples, with a minimum of 5,185,191,936 available bytes; the 4 GB standing stop was not reached. No source, product, registry, queue, or generated source files were changed. The first read-only pin check compared the wrong recipe metadata field, was corrected before admission, and did not start a request.

This result is only the admitted original bulk selector. It is not an overall P2/platform GO, REG0, final build, ZIP, or qualification of any other selector.
