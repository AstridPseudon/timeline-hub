# Runtime RT08 item/global witness source

Prepared on Runtime `42a7203f49bb89f299ec854cfbf2b1444e815a7c` (tree
`1f220b3d3a27e8eb061b15c944bad784c8fdb82e`) with Agent pin
`4b7a27127fb9b642be8ad118e6aa663bd7761611` (tree
`a6126ed13a7b4dad8124894ebced1cf1b5977d5f`).

The source adds `test_startup_provider_materializes_source_items_and_refuses_global_item_occupancy`
to `tests/test_timeline_projection_occupancy.py`. Its setup publishes opaque source items to
the already-owned `shot-2` and `shot-3` heads through Runtime's normal
`publish_parent_composition` API, then starts the normal Astrid Runtime daemon. The test body
uses the real Agent move command and startup-loaded provider to check source-shot/item and
occurrence-owner bindings, restart plus inverse/rematerialization reuse, and an unrelated
same-project catalog item collision with an unchanged durable-store snapshot.

This is source preparation only. The positive body was not run: Runtime ownership coordination
and independent review remain prerequisites. The two existing occupancy/materialization lanes
were not replayed.
