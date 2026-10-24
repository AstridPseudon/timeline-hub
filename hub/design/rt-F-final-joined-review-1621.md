## PASS — F-final joined candidate review

Reviewed joined candidate commit `ed39ab99cb6f5026be58cd4d18191d6e87fcd2e2`.

Artifacts and SHA256:

- `evidence/candidate/install-final-services.py` — `2262201fe5c3a062c4c82afc9925abbf6e9d432887e777c8afc4bdbb3e4756e2`
- `evidence/candidate/run-final-services.py` — `c2f319acb45bc5dbb7bc94336c0ab23980e3d681d74325ab0714672bb7f2fe15`
- `evidence/candidate/run-final-delivery.py` — `64c83b4e99a3b46f966b0d056122f6a58626e38d4ee490dc152a33937332455d`
- `evidence/candidate/runtime-final-service-rows.txt` — `5d678805fde6d840d07f32f3587ef5c38267b81fe10dab424199aef3934c3019`
- Reviewed D68 wrapper — `bae840fad6ea496457a3d6138609ce9d89b0b10825827c94f855257bce6c6779`
- Installed builder — `f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708`

Checks passed:

- Python compilation.
- `ruff check --select F`.
- `mypy --no-incremental`.
- Shell syntax for all three service rows.
- 84 unique Python targets plus TypeScript command.
- Original 81 selector test files byte-identical.
- Core row routes to joined runner; delivery rows route through the reviewed wrapper caller.
- No direct delivery-builder bypass row.
- Installer, caller, runner, wrapper, and builder hashes agree.
- No-install/preimage validation.
- Pending tuple markers remain pending; tuple files are absent.
- Stub caller verified reviewed-wrapper argv and exact extras forwarding.
- Contract hash remains identical to design contract: `4581ea85...`.
- Candidate changed only the four private candidate artifacts.

No product/test body, full/core/gate suite, installation, build, ZIP, network, fetch, or tuple-dependent execution was performed. Fresh-main staging and broader D68 controls are reused from the exact-byte-matching predecessor proof and remain unrerun here.

Evidence:

- `workers/rt-F-final-joined-review-1621/evidence/independent-review.txt`
- `workers/rt-F-final-joined-review-1621/evidence/independent-controls.log`

No findings. `DONE` and commit message markers were created.