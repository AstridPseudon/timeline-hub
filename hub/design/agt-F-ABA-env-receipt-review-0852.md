## PASS — F-ABA receipt review

Verified:

- Live registry SHA-256: `5ada85961e709386b7d7aa328338fda01af6bfc2c8efea6ddd9170671dbe851f`
- Reconstructed original registry: `83ff4c2bd6b2c7ee4f9376c2cc06ad77c185be2a03213e22327af0de90902d27`
- Old row: `f7bd322a453615d89a4322803fa7e79f7fdad425657aa6e01a6a034f0593de31`
- New/source/live row: `61b7e27edf66fcdfd21edbf98233a1961a2cc473dd9a7b4ed3db9a1e9978067d`
- Outside-byte identity: PASS; outside hash `afd6f92fe8208bcc211208ca80e3aca7446dede50f2c64e968bc359ea7e5d9bc`
- Exactly one live key, line 173; regular non-symlink mode `0600`

Checks:

- `bash -n` registry: PASS
- `bash -n` `request-test`: PASS
- Independent committed-old-row reconstruction: PASS
- `git diff --check`: PASS
- Worktree remains clean

No service request, preflight, pytest body, browser, realm, or operational mutation was performed. The temporary backup is absent; custody is limited to the installer’s permanent report and the directly verified live registry/source bytes. The production caller’s actual execution remains unverified.

Commit message written and `DONE` marker created.