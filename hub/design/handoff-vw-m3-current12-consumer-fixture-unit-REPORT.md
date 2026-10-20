# Current12 consumer fixture companion report

## Result

No worktree patch was created. The current owner source `5f6c81309d96e7cd7abc2f22b32a377621c29092` already contains the exact approved six-file f29 consumer-test delta and the three-file presenter12 companion adaptation. The package test is the intentional overlap between those sets, leaving eight unique test paths. Its merge `ed60bf152b1b468d8d794f2c90ac8a3e1f233691` is available in the Agent refs.

Compared with staging cohort `082cf265b448712b031730d61cf3b9f63b813ab3`, the owner source changes only the requested test expectations for the six consumer files plus presenter scene capability Python/MJS. No product component, package, lock, pin, registry, artifact, xfail, skip, or historical SSR fixture change was copied into this worker.

## Validation

Validation used a disposable overlay made from staging HEAD, with only those eight test files overlaid from `5f6c81309`, the exact 0.0.12 artifact, and a private copy of the provisioned Remotion peers. The artifact guard was SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; its tarball contains 77 files.

`pytest -q -o addopts= -p no:cacheprovider --tb=short -m 'not integration'` on the six consumer tests: **277 passed, 2 deselected**.

`pytest -q -o addopts= -p no:cacheprovider --tb=short -m integration` on presenter scene capability and crop tests: **17 passed**. This exercised the 286 historical SSR hashes with explicit historical theme data and the public12 navy default assertion, without setting the optional artifact override.

The full export-adapter module was not claimed: its pre-existing integration case requires the separately provisioned generated registry absent from this staging cohort (`remotion/src/effects.generated.ts`). Its ordinary/non-integration cases passed in the 277-case run.

No browser, socket, install, network, full suite, Runtime pair, normal source activation, or parity claim was made.
