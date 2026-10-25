# D73 qualified receiving route

1. The Agent owner receives exactly launcher blob
   `f1bde17ea107a8b669cb6924fbdbd2f3979da988` (SHA-256
   `9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`) at
   the existing dispatcher/installed-entrypoint route. No dispatcher or
   entrypoint edit is needed.
2. Keep the captured D73 tuple and request 18455 immutable. If the owner adopts
   the blob into the frozen Agent checkout, publish a new Agent commit/tree and
   recompute the manifest’s Agent SHA/tree/parent fields; do not silently
   rewrite the old manifest or retarget its tuple.
3. Run the existing guarded preflight against that explicitly received tuple,
   then run the same two focused controls with the owner’s actual launcher path.
   Require positive body exit 17 exactly once, both-subshell environment
   clearing, exact private origins, preserved guard fields, and poisoned-manifest
   zero body execution before any operational body request.
4. Keep the qualification labeled source-only until a separately authorized
   harness has genuine frozen Runtime/App/Composition inputs. This review does
   not authorize provider, browser, Remotion build, acquisition, kit install,
   or production-request execution.
