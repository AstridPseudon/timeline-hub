# Runtime journey checkout environment

This checkout is the isolated Runtime environment for the M0 App journey. The
App harness must use:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-m0-journey-runtime-env
```

The checkout's `.venv` is an ignored symlink to the shared dependency-only
environment at `/home/user/work/venv-runtime`. No dependency installation or
package metadata change is part of this setup; Python imports resolve the
Runtime source directly from this checkout.

The harness must not recycle this checkout until the journey worker is done.
The environment is based on `tl/integration` at Runtime commit
`8c1830d1ca64a3934c37611a28ffe8db7df879ea`, with package version `0.1.0`.
