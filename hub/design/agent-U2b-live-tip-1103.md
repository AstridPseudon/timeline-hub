# U2b live upstream verification

- Probe: `u2b-live-upstream-1103`
- Worker: `agt-U2b-live-tip-1103`
- Test ID: `agt-U2b-live-tip-1103-u2b-live-upstream-1103-1023110248-4676`
- Result: pass, exit `0`, reported duration `1s`
- Service candidate tree: `3020d0a43a6174b627bef13a5337d06ed1e40881`

Captured stdout:

```text
LS_REMOTE_STDOUT=74f3f7edba35230d0a01824eae7b663143e6aa5b	refs/heads/main
LIVE_UPSTREAM_SHA=74f3f7edba35230d0a01824eae7b663143e6aa5b
ORIGIN_MAIN_SHA=74f3f7edba35230d0a01824eae7b663143e6aa5b
CANDIDATE_HEAD_SHA=8186c130bd4b178dada39bd103476db5853fa180
```

The bounded host-side `git ls-remote` output had the exact expected SHA/ref syntax. The live SHA matched the service candidate clone's `origin/main`, and `git merge-base --is-ancestor LIVE HEAD` passed. No fetch, merge, commit, product/test/pin, environment, or proxy changes were performed.
