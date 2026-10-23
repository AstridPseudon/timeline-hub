# P1 OPS: approved Remotion registration template packet

## Verdict

PASS for the requested light read-only ENV handoff. This packet publishes the
existing supported `remotion-env-nodes` registration row and
`tests/agent-remotion.env` bytes unchanged. It is input custody only: no
provisioning, child run, daemon, browser, socket, service, or test run was
performed, and it makes no product, maker, guard, policy, or Runtime-pin
change.

## Exact source identity

- Source row: `ORCH/tests/suites.conf`, exact line 83, suite
  `agent remotion-env-nodes`.
  - Decoded bytes excluding the line terminator: 708.
  - SHA-256 excluding the line terminator:
    `ffdb0b13c65f106d7b818208343feb3f438dfc943f4af57c5f612ddcf73dc036`.
  - Published row bytes include the source LF terminator: 709.
  - SHA-256 including the LF terminator:
    `e14e5ac850ba94ddadadd55b8b48ea3999fb06bc9ebc101c859d4413890ab944`.
- Source env: `ORCH/tests/agent-remotion.env`.
  - Decoded bytes: 523.
  - SHA-256: `e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02`.
  - Secret audit: exactly `PATH`, `ASTRID_REMOTION_PROJECT_DIR`,
    `ASTRID_NODE_EXECUTABLE`, and `ASTRID_TIMELINE_SCHEMA_PYTHONPATH`; no
    credentials or additional keys.
- Provenance: the source row and env were read directly from the two named
  ORCH inputs. The base64 attachments below encode those source bytes; decode
  them without trimming, regenerating, normalizing, or substituting paths.
- P1 ACK custody: App sole runner `1821` / ACK `1830`, App
  `2107` (a3ff clean unchanged), Agent
  `78738040d72ce74c42ddf7731221aecb06f9246d`, Runtime
  `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`. The ACK says source checkouts
  succeeded and the child was queued; it does not claim a new run.

## Byte attachments

- [`peer-app2-to-app2-20261023T1835-remotion-env-nodes.row.b64`](peer-app2-to-app2-20261023T1835-remotion-env-nodes.row.b64)
  is the exact 709-byte row, including its final LF after base64 decoding.
- [`peer-app2-to-app2-20261023T1835-agent-remotion.env.b64`](peer-app2-to-app2-20261023T1835-agent-remotion.env.b64)
  is the exact 523-byte env file after base64 decoding.

## App CodexOPS import and verification

1. Decode each attachment to private temporary files. Keep the decoded row as
   one line with its final LF and the decoded env with its four original LF
   terminated lines.
2. Verify the decoded counts and hashes above, and verify the row has exactly
   one trailing LF. Import the decoded row and env into the App's existing
   local registration inputs unchanged; do not edit `make-runtime`, its
   guard, the queue, or any environment value.
3. Before any later approved request, verify that the existing supported
   maker recognizes the pair by exact identity. The actual production route
   remains `request-runtime -> dispatcher -> make-runtime`, with the selected
   Agent/Runtime pair above. This packet does not authorize or perform that
   request.

For byte verification, the decoded artifacts must satisfy:

```text
row: 709 bytes, SHA-256 e14e5ac850ba94ddadadd55b8b48ea3999fb06bc9ebc101c859d4413890ab944
row without final LF: 708 bytes, SHA-256 ffdb0b13c65f106d7b818208343feb3f438dfc943f4af57c5f612ddcf73dc036
env: 523 bytes, SHA-256 e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02
```

The production caller must preserve the approved full v2 request shape:
`api_version`, `scope`, `base`, `pair`, `commands`, `label`,
`steps` (including `id`, `label`, `intent`, `tags`,
`command_ordinals`, `patch`, and `reads`), `merge`, `reads`, `key`,
`dry_run`, `source`, `rationale`, and `group_id`. It must also preserve
the full result envelope: `data`, `receipt`, `accepted`, `merged`,
`historical_rebased`, `head`, `document`, `records`,
`dependencies`, `effects`, `steps`, `history`, `undo_steps`,
`preview`, `required`, `would_status`, `conflict`,
`reason`, `head`, `invalid`, `code`, `path`, `hint`, and
`command`. No response fields are narrowed or omitted by this ENV handoff.

Prior actual proof references `079` and `2a9` establish template provenance
only; they are not a new execution claim. The App's existing CodexOPS remains
the owner of any subsequent sole P1 run and its real report-all evidence.
