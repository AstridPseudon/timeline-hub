# Agent private15 native speech dependency resume

Status: blocked after the dependency repair. The required exact native node reached the real speech worker and the genuine Edge TTS synthesis path, but the central runner could not validate the proxy certificate.

## Dependency repair

The existing speech declaration was recovered from Agent commit `e0391711d60c29da14ebe2fe8e39f480cff6c183`: `edge-tts>=7.2,<8`. No product source, schema, or pin was changed.

The package was installed with the allowed package-install network access into this private worker overlay only:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-private15-edge-dependency-native-resume/edge-tts-overlay/site-packages
```

Resolved packages:

```text
edge-tts==7.3.1
aiohttp==3.14.5
certifi==2026.10.19
tabulate==0.10.0
typing-extensions==4.16.0
aiohappyeyeballs==2.7.1
aiosignal==1.4.0
attrs==26.1.0
frozenlist==1.8.0
multidict==7.1.0
propcache==0.5.4
yarl==1.25.1
idna==3.20
```

The `site-packages` suffix is required by the existing supported `dependency_pythonpath()` projection. I temporarily added that private root to the owned named-suite command, ran the suite, and restored the shared suite configuration afterward. The first attempt with the overlay root itself was rejected by that projection and failed at `ModuleNotFoundError`; the approved `site-packages` root resolved that import failure.

## Exact test evidence

Central named suite command requested (the only suite run for this worker):

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-m2-private15-edge-dependency-native-resume agt-m2-private15-requester-restart-prep) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$(basename "$R")"
```

Result: failed in 18.31s. Result log:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-private15-edge-dependency-native-resume-agt-m2-private15-requester-restart-prep-1021015525-19563/log.txt
```

The real child imported `edge_tts` from the private overlay, then both declared Edge TTS endpoints failed with:

```text
aiohttp.client_exceptions.ClientConnectorCertificateError:
Cannot connect to host speech.platform.bing.com:443 ssl:True
[SSLCertVerificationError: (1, 'CERTIFICATE_VERIFY_FAILED: self-signed certificate in certificate chain (_ssl.c:1032)')]
```

The preceding endpoint `api.msedgeservices.com:443` failed with the same certificate-verification error. No mock, synthetic WAV, fixture substitution, inner-identity shortcut, source-fence change, or TLS-verification disablement was used. Proposal/outbox/lost-ACK/restart/exact-retry/undo/ripple assertions therefore remain unverified because the genuine speech artifact was not produced.

## Blocker and next step

The remaining blocker is the central runner's proxy CA not being available to the isolated native speech child. The named suite uses `env -i`, while the runner's host environment has `/root/.ccr/ca-bundle.crt`; the child policy does not propagate arbitrary `SSL_CERT_FILE` values. Resolving that requires an orchestrator-owned runner/child trust configuration or a rerun in an environment with the approved CA. Do not change the speech action or weaken certificate verification.
