# Agent public13 normal-pin source — independent D10 review

## Decision

**APPROVE HELD SOURCE ONLY.** The completed Agent normal-pin prep is a
source-ready 0.0.13 candidate, but this is not approval for activation, merge,
or an adoption request. The App-FIRST prerequisite remains uncleared: the
latest App owner13 handoff is a narrow reject, so Agent work must remain held
until App publishes its qualified actual13 source.

## Scope and identity

The reported product scope is limited to:

- `astrid/core/rendering/remotion_runtime.py` — literal
  `_COMPOSITION_PACKAGE_VERSION` `0.0.12` -> `0.0.13`;
- `remotion/package.json` and `remotion/package-lock.json` — exact local
  artifact path/version/integrity update;
- the 0.0.13 tarball and matching sidecar;
- direct package/admission/readiness test fixtures and the current capture hash
  map.

No dependency, toolchain, Runtime client/schema, compiler/provider, policy,
default/theme, renderer math, or source implementation change is present. The
existing package-consumer admission remains narrow: it still checks the one
literal current package version and the unchanged required export list; no
range or policy widening was introduced. The explicitly consumed public12
compatibility fixture and public11/public12 archive bytes remain retained for
their existing uses; no M4 cleanup is part of this source gate.

No other unowned scope was found.

Verified release identity:

- package: `@banodoco/timeline-composition@0.0.13`;
- artifact: 58,477 bytes, 77 regular members, SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`;
- lock integrity:
  `sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==`;
- sidecar checksum matches the artifact;
- old immutable hashes remain `0.0.12` =
  `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` and
  `0.0.11` =
  `dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601`.

The tar manifest contains only `package/` members. Its package exports point
to built files for the required root, evaluation, theme-api, registry, and
generated registry entries. `dist/evaluation.d.ts` declares the required
`encodedEnvelopeSource` function and `EncodedEnvelopeSource` type (alongside
the existing public envelope APIs); the emitted JavaScript contains the
runtime export.

## Evidence

Independent private replay of the supplied prep patch on a clean
`tl/integration` Agent archive:

- package/readiness lane: **6 passed, 1 deselected**;
- readiness neighbors: **2 passed**;
- artifact SHA-256, size, sidecar comparison, and 77-member safety: **passed**;
- `git apply --check --whitespace=error`: **passed**.

The package tests retain strict installed-only fixtures: missing dist and
deleted, missing-target, and package-escaping export negatives remain
refusals. They stage extracted package files under pytest temporary paths; they
do not prove npm installation, launch validation, or runtime availability.
The valid-source/four-forgery API test similarly runs against a private
artifact extraction and is overlay-only evidence.

No install, npm ci, network, registry publication, browser, renderer, socket,
full suite, or shared dependency/cache mutation was performed. The real
capture-scene lane was not run because the required provisioned Node
20.19.4 renderer executable is unavailable in this review environment.

## Owner-gated next step

After App publishes its qualified actual13 source, the owner should provision
an isolated Agent13 leaf, byte-verify the artifact/lock and all 77 members,
then run the direct readiness and capture lanes there. Do not activate or
merge this held source before that publication and owner decision.
