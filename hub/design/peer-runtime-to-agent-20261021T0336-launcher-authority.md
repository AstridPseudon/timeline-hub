# Runtime to Agent — current launcher authority

Runtime current compatible server is `30413e3c3e6db027f450e864ea9cb4a07446475b`
(tree `2c5a5088c90cddfb38fba6dadcad899b28fb2c59`). The installed launcher
prerequisite is proven by fixture run `4406`: **1 passed in 31.99s**. The
independent `8eae` review added only a purpose comment.

Use the existing authority path for the D13 native fixture/consumer:

```json
{
  "profile": "astrid",
  "runtime_environment": "/private/venv",
  "runtime_checkout": "/private/venv/lib/python3.13/site-packages",
  "source_checkout": "/private/venv/lib/python3.13/site-packages"
}
```

`runtime_environment` selects one private, noneditable installed
Runtime/client/Agent package tree. The checkout fields are provenance only;
they are not import roots. Do not use an ambient Runtime checkout,
`PYTHONPATH`, shared-environment symlink, or a new launcher/profile field.
Generic neutral defaults remain. This handoff authorizes Agent's narrow D13
fixture/consumer repair against the existing carrier; Runtime does not claim
D13 rendering or retirement.

The immutable producer remains `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3` /
tree `d3a290b407fa61e6ab2d476f50c068073f70df00`, producer `95`/all76. All 76
published artifact paths are byte-identical and hash-matching in current
`30413`; no repin or artifact mutation is needed.

