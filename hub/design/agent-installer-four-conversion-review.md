# Installer-four assertion-conversion review

Decision: **APPROVE**.

Reviewed exact ref `tl/agt-m4-full21969-installer-four-source-repair-0605` at
commit `abdc8021b1fbdddad050513b8a8d42350b94465d`, tree
`6534c94af8beac70e0cbef43e20c55b7f9ffb106` (parent
`6accf0f7be925f47d7fb9b4b522bb66ecf0d89ef`).

Mapping verified:

| Old assertion/fixture | Current assertion/fixture |
| --- | --- |
| `launchd.plist`, `systemd.service`, and `task.xml` each contained one extra blank line after the renderer's terminal newline | Each fixture removes only that final blank line. `astrid/installer/service.py` is unchanged, so rendered MAIN service definitions are unchanged. |
| `test_remotion_lock_pins_the_transitive_schema_package` required Composition 0.0.6 plus a separate `@banodoco/timeline-schema` 0.0.1 lock entry | `test_remotion_lock_pins_the_immutable_composition_public_entry` requires the local immutable Composition 0.0.13 archive, exact file URL/resolved path and integrity, absence of separate schema/theme lock entries, and the eight public exports resolving to present compiled `./dist/` files. |

The replacement is behavior-bearing package readiness, not a bare import or
synthetic pin. The artifact computes to SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` and the
asserted SHA-512 integrity. The unchanged
`tests/packs/rendering/test_composition_package.py` retains the valid-package
readiness checks and missing/invalid negatives (missing dist, deleted export,
missing export target, and package-escaping target).

Evidence:

- Target-archive pytest for the changed schema assertion and one service
  fixture (`linux-systemd.service`): **2 passed**.
- `git diff --check parent target`: passed.
- Changed paths are exactly the three installer fixtures and
  `tests/test_installer_schema.py`; no package, lock, service renderer, or
  generated source changed.

No full suite was requested. The darwin and Windows parameter cases were not
executed; their fixture diffs were independently verified as the same
one-terminal-blank-line correction.
