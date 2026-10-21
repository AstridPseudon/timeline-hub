# Runtime delivery template carrier — App response

## Answer

App cannot pass a template or gate-results path to the installed packer. The
normal owner inputs must exist at these exact paths on the machine that runs
the packer:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/README.template.md
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/gate-results.md
```

The source hard-codes `ORCH`, `DELIVERY`, `TEMPLATE`, and `GATE_RESULTS`
(`delivery-build`, lines 28–31). `render_readme()` opens `TEMPLATE` directly
and reads `GATE_RESULTS` directly when it exists (lines 300–319). The only
supported CLI inputs are `--dry-run`, `--repos`, and repeatable
`--extra DESTINATION=SOURCE` (lines 503–510); there is no template or
gate-results override.

For the final coordinated source delivery, the reviewed normal invocation is
the existing command in
`design/handoff-vw-m4-scanner-reviewed-carrier-COMMAND`: it calls
`python3 "$ORCH/bin/delivery-build" --repos "agent runtime app composition"`
with the reviewed scanner/owner-instruction and Composition-e7 `--extra`
arguments. Those `--extra` files are copied only after the generated
`README.md` is rendered (lines 548–555); they cannot supply or replace the
template or gate input. `--repos app` is the supported App-only subset, but it
does not change this carrier behavior.

The command's normal owner-input preflight is therefore:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
test -f "$ORCH/delivery/README.template.md"
test -f "$ORCH/delivery/gate-results.md"
python3 "$ORCH/bin/delivery-build" --repos "agent runtime app composition"
```

For the reviewed scanner carrier, append the exact `--extra` arguments from
`handoff-vw-m4-scanner-reviewed-carrier-COMMAND`; they do not change the two
preflight paths above.

Therefore, a supplied template path must first be installed/copied unchanged
by the normal owner workflow to `$ORCH/delivery/README.template.md`, and the
supplied gate-results text likewise to `$ORCH/delivery/gate-results.md`; App
cannot use an arbitrary supplied path directly. The existing inputs are
exported unchanged as the two adjacent handoff files:

- `runtime-app-delivery-README.template.md`
- `runtime-app-delivery-gate-results.md`

The gate text remains `DRAFT / BLOCKED`. Fresh11141 is recorded only as
rehearsal evidence; it is not a final ZIP, owner-film, macOS, physical-parity,
or all-gates-green result. Peer App’s missing `README.template.md` explains
its exit 1; no App-only equality result is upgraded here.

## Evidence inspected

- Installed source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`.
- Approved owner inputs: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/README.template.md` and `gate-results.md`.
- Scanner carrier instructions: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-scanner-delivery-instructions.md` and `handoff-vw-m4-scanner-reviewed-carrier-COMMAND`.

No delivery build, ZIP, test suite, browser, render, or four-repository replay
was run.
