# App media CORS final review

Verdict: **APPROVE**

Authorized current SHA: `946d25b8de76b9f21b57afc35f4dfccdcc005882`

The authorized source change matches the supplied proposal for the helper: it
adds only an HTTP(S) absolute-URL arm gated by the existing canonical
`isGatewayUrl` predicate. The existing `isManagedObjectUrl(url)` arm is
unchanged and remains the other arm of both decisions. The authorized product
diff is limited to:

- `src/shared/lib/media/mediaCrossOrigin.ts`
- `src/shared/lib/media/mediaCrossOrigin.test.ts`

There is no HoverScrubVideo product diff. The original two
`HoverScrubVideo.gateway.test.tsx` cases and their input bodies remain
unchanged. The direct test covers HTTP and HTTPS gateway URLs, anonymous CORS,
omitted browser credentials, and the prior blob/data/custom/external/
protocol-relative/wrong-port counterexamples. Relative managed routes retain
anonymous CORS and omitted credentials. No AuthContext/provider, routing,
retired-path, or content-liveness claim was added.

## Evidence

Successful focused run against the actual authorized source in a disposable
archive overlay, with the shared `node_modules` symlink read-only and Vitest
cache disabled:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --pool=forks --maxWorkers=1 --no-file-parallelism src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx src/shared/lib/media/mediaCrossOrigin.test.ts
Test Files  2 passed (2)
Tests       23 passed (23)
```

The requested cache-free `--configLoader=runner` variant was also attempted,
but this repository's config uses `__dirname` and fails before test discovery
under that loader; the supported bundled config-loader run above is the passing
evidence. No full suite, build, browser, socket, TypeScript, or install run was
performed. The review worktree is clean and no shared dependency/cache changes
were observed.
