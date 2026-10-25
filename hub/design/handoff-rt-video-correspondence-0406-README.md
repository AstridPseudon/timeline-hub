# F-D86 actual9211 video correspondence

Safe, source-only projection for exactly the four retained video12 selectors
requested by the 2026-10-25T0356Z handoff. The retained actual9211 XML and body
log are private; this packet contains identifiers, hashes, and bounded coverage
only. No setup/inverse pair, source mapping, materialization binding, or
semantic verdict is reconstructed.

Every requested correspondence field is `EXACTMISSING`. The four selected XML
records are error records whose first exception is `CommandError: missing or
ambiguous identity 'occ-a'` at `astrid/sdk/timeline/_command_state.py:154`.
The selected records retain no accepted setup/inverse payload.

Private artifact hashes inspected:

- actual9211 XML: `eef3d52683227fe57b2d5e63abce044d11fd68cb31960e9a4ff5194cfeb5aab2`
- actual9211 body log: `796efbbcbed165da591506305129f7fce9a99a172b6a0576a2e3bf8134c61981`

The safe four-row source projection used for selector identity is retained at
the producer worker as `actual9211-video12.json`, SHA-256
`45ca7797941ee9e86476e02ab755604442681d064026e6b92a57288ef655a6e4`.
