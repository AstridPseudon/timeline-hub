# Scanner 1.0.8 independent delivery gate

## Verdict

**APPROVE** the exact held artifact below:

- archive: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner108-codec-repair-1.0.8.tgz`
- SHA-256: `e87e88705679e320bc83b6c72dff31fe23bbd0122981f314b5890411d6449cfb`
- size: 18,116 bytes

The repair worker's DONE and REPORT are present. The artifact metadata remains
`HELD_PENDING_INDEPENDENT_AND_AGENT_POLICY_REVIEW`; this report supplies the
independent half of that gate. No owner-film data was used.

## Evidence

- Exact 1.0.7 baseline archive `baf2fd28f96670b02e4dc63e21bc680e2ab0339a97671515d79ab91f9cbd3e27`: extracted original suite **40 passed in 5.67s**.
- 1.0.8 archive has exactly four regular USTAR members. Modes, ownership,
  timestamps, sorted names, archive sidecar hash, metadata hash, and all four
  flat member bytes agree. Metadata status/hash/provenance were checked.
- Fresh extraction command:

  ```text
  /home/user/work/venv-agent/bin/python -I -B -m pytest -p no:cacheprovider --basetemp .../candidate108.a7ef16/pytest -q .../candidate108.a7ef16/tests --agent-root /home/user/work/wt/vw-m4-scanner108-independent-gate
  ```

  Result: **124 passed in 5.98s**.
- Independent bounded codec matrix: **130 cases**, covering every declared
  stored visual/audio family in scope (opacity, entrance, exit, four crops,
  speed, volume, both audio fades, both audio curves). **101 known-malformed
  cases failed closed** with the bounded authored source path; 29 settled
  controls (clears, valid values, and unknown string curves) preserved their
  existing policy. All families passed; no input mutation or raw marker leak.
- Machine-readable matrix evidence: [codec-matrix JSON](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner108-independent-gate-codec-matrix.json)
  (SHA-256 `8d480b6a593f7eccae567cae97a3642143e2fd19938118158f757fb193c46972`);
  preservation/repeat evidence: [text log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner108-independent-gate-preservation-repro.txt)
  (SHA-256 `6da776c4ece68aca6213e6cea0069debcad5c468bd0830b4576b80540f45a722`).
- Independent preservation checks passed: explicit `asset=None` clear and
  opaque extension survive the Agent projector without appearing in bounded
  output; free-form transition mapping remains accepted; malformed transition
  remains bounded; one projector call per scan; two repeated scans are byte-
  equal.
- Relevant Agent codec files at the current clean Agent worktree are identical
  to the repair worker's recorded HEAD `86405964ecb713ad42a375f9de7960b3f9dc259b`.

The repair worktree path was removed after worker completion, so a later direct
attempt naming that path produced setup errors. It was not used for the
verdict; the extracted archive was rerun against the current clean Agent
worktree above, and the relevant codec files were confirmed identical.

## Not run / next step

No full Agent suite, owner data, browser, renderer, listener, network, install,
macOS, or product-repository mutation was performed. Agent canonical-policy
review remains the required follow-up before release adoption.
