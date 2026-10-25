# D134 setup proof

The fork setup now supplies `client=lambda: client`, where `client` is an
`AstridClient.open(...)` connection to the daemon realm that owns `service`.
The daemon loads the registered `astrid` provider through its normal startup
profile; no provider, history, item, or media record is synthesized.

The ordinary fixture already admits its exact raw media pin. Its missing
occurrence video row cannot be restored by adding a guessed row or shot item:
the supported occurrence-media caller requires Runtime-verified catalog media,
which this fixture's authored raw-byte ingest does not create. Changing that
input/topology is therefore reported as an exact UNAPPLIED dependency.
