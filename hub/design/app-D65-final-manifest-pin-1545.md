## Report

Updated only [public/install-manifest.json](/home/user/work/wt/app-D65-final-manifest-pin-1545/public/install-manifest.json):

- Agent: `57779274a0e4a1ae7defef1a6f7239b79d411d55`
- Runtime: `8b32cacea617c6d45241d7db90b34893a06d3026`
- Schema: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`

The post-write `--plan` confirmed identical pins/digest.

Tests:

- Manifest skew Vitest: PASS, 2/2.
- Runtime schema guard: PASS, 2/2.
- Manifest/update-manifest Node tests: 3/4 passed; updater fixture fails because it hard-codes obsolete schema `sha256:4118…` instead of current `sha256:867f…`.
- `git diff --check`: PASS.

Runtime and Agent checkouts were clean at the reported heads. No source, generated files, or tests were modified.

Blocked marker recorded due the out-of-scope stale updater fixture.