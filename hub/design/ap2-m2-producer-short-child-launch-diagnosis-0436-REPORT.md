# Producer Chromium short-child launch diagnosis

## Result

The preserved actual `1021043055-14352` failed at Chromium startup, before the
producer test body, because the existing public13 runner derived its child
temporary/profile root from the long App worktree path. This is the known
long-child-root environment failure, not producer behavior. The precise
Chromium internal syscall is not identified by the preserved stderr: the
profile/socket path length is the causal environmental evidence.

The source/preflight/isolation/build prerequisites had already passed in the
preserved run. The failed child was Chromium 141.0.7390.37 at:

```text
/opt/pw-browsers/chromium-1194/chrome-linux/chrome
sha256 85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95
```

The exact Playwright launch retained the normal installed arguments and the
existing harness arguments (`--no-sandbox`, `--disable-dev-shm-usage`,
`--no-proxy-server`, resolver/certificate/address-space guards,
`--remote-debugging-pipe`, and `--no-startup-window`). No browser option,
sandbox/security setting, source hash, assertion, or timeout was changed.

## Preserved failed paths

The actual argv contained:

```text
--user-data-dir=/home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/.public13-effective-ordinary/tmp/playwright_chromiumdev_profile-LBh0mh
```

Measured lengths:

| Path | Bytes |
| --- | ---: |
| App run root | 96 |
| `TMPDIR` prefix | 101 |
| Chromium `--user-data-dir` profile | 138 |
| inferred Chromium `SingletonSocket` under that profile | 154 |
| full launch line | 2,106 / 2,111 in the two retained log lines |

The argv did not contain a pathname for a Unix socket: it used
`--remote-debugging-pipe`. `SingletonSocket` is the profile-local Unix-socket
path Chromium conventionally derives from `--user-data-dir`; its 154-byte
length exceeds Linux's 108-byte Unix-domain socket pathname limit. The
preserved stderr only showed crashpad's missing cpufreq sysfs files, followed
by `signal=SIGTRAP`; those messages do not identify the internal failing call.

The existing central diagnosis independently reproduced the same full Chrome
and normal Playwright launch with a 306-byte long root: the long-TMPDIR case
SIGTRAPed before a page, while the same binary/options passed page, JavaScript,
DOM, and clean-close checks with a short TMPDIR. That central result was:

```text
app-m3-chromium141-launch-diagnose-chromium141-launch-diagnose-integration-1020133523-30467
PASS, exit 0
```

This confirms the environment cause at the launch boundary. It does not claim
a Chromium native stack trace or an exact threshold beyond the measured paths.

## Corrected binding prepared

`scripts/testing/run-producer-public13-list.sh` now binds only the invocation
of the existing public13 runner to a unique, owned short alias:

```text
/tmp/tla-XXXXXX/a -> the original App worktree
```

It also creates private XDG cache/config directories under the same unique
`/tmp/tla-XXXXXX` root and removes the alias/root on every exit. The public13
runner remains unchanged, so its existing `TMPDIR`, Playwright cache, npm
cache, Vite cache, profile, build, source, and cleanup behavior remains in
force. The real App checkout and all source guards remain bound to the caller's
original path.

With a representative generated root `/tmp/tla-ABC123`, the expected child
paths are:

| Path | Bytes |
| --- | ---: |
| corrected `TMPDIR` | 50 |
| corrected profile | 88 |
| corrected `SingletonSocket` | 104 |
| corrected XDG cache | 33 |
| corrected XDG config | 34 |

The central command remains the existing producer command, with the updated
wrapper hash bound by independent custody review before any actual:

```sh
sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh \
  /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 run
```

The prepared wrapper hash is:

```text
95e5a901b599d3202788fb7ce5cbc6d0b6517d63a3a5c9e40e43a90979ce2983
```

The existing public13 runner hash is unchanged:

```text
be59b3da5c01e0df22ec556cc84cd25a2a1a4304cf4542035829003eecb2e75b
```

No shared runner was changed. The central producer suite currently hardcodes
the old wrapper hash, so custody must update that binding and independently
review the small environment-only diff before a new preflight/actual can be
authorized.

## Prerequisites and validation

Verified on this worker:

- `/tmp` is mode `1777`; the worktree is mode `755`; Chromium is executable
  mode `755`.
- Free disk was `15,367,880 KiB` (about 14.65 GiB), above the 10 GiB gate.
- `node_modules` remains the existing symlink to
  `/home/user/work/app/node_modules`; no shared dependency or cache was
  changed.
- Source keeper remains commit `97187ce3c1576559239f869067a9cef8ffb5f357`,
  tree `4acab858b0f12a1878fc231a33f3d06af9b0bdc0`.

Commands:

```sh
sh -n scripts/testing/run-producer-public13-list.sh       # PASS
git diff --check                                          # PASS
```

The one local wrapper `preflight` invocation was intentionally made before
the harness commits the wrapper. It failed closed on `app-clean`,
`app-baseline`, and `approved-body` because this environment-only diff makes
the worker dirty; it did not build, launch Chromium, or mutate dependencies.
The corrected producer-bound central launch-smoke/preflight result is therefore
**UNKNOWN**. The prior existing central launch-smoke PASS above is the
available smoke evidence; no producer journey or actual was retried.

No full suite, native bootstrap, install, shared dependency mutation, browser
retry, or live-caller/product change was made. No producer assertion is
qualified by this report.

## Next step

Independently review the wrapper hash/binding and run the existing central
producer preflight on the committed snapshot. If it passes, one bounded
central launch smoke/preflight may be run on the short environment. Do not
submit another producer actual from this worker until that custody review and
smoke are green.
