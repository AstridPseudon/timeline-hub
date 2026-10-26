# D141 App note intake — installed

Installed the exact one-line note from the independently protected review into
both canonical delivery inputs. No ledger, product, test, pin, kit, registry,
source, hub, or Git file was changed.

## Custody and identity

- Protected full note: `app-A2-D141-read-interface-protected-review-0203-zip-note.md`,
  SHA-256 `76dd3661042efe7580c170caad669ed5bbf690f5301c6662aa70475df89a3e8d`.
- Protected review JSON SHA-256:
  `e6f66a9d69362f4f524d5bd0c5e4d507be7c98fdb7e97ddd584e2d69c6701d20`; verdict
  `PASS`, findings empty.
- Normal App merge: `5fe3e4debec5fb030f772ca41f16c86cc80e6150`; tree
  `af51793b7cc9b2d0426e629bce1d9e4529a7edb6`.
- Candidate: `a1955216f947f9d84c3154d3bd715e65bc945452`, tree
  `af51793b7cc9b2d0426e629bce1d9e4529a7edb6`, direct parent
  `867cb2737af1b46dc608c7cd37c349e920fe9422`.
- Source was read from normalhub/sourceblobs at `/home/user/timeline-hub/hub/design`;
  no hub write or network access was used.

## Installation receipt

- README installed SHA-256:
  `2cb99445661f9466864da05836e3188925c8c6320f7adf3d9c767e2c9b26319e`.
- gate-results installed SHA-256:
  `b50d138e697d90f7bc04f3171dbb21d12d223c41103aaa9790216daa0e424467`.
- Both targets are regular non-symlinks, mode `0644`.
- Exact preimage backups are in `evidence/backups/`, with README preimage
  `5738d66d75b5f784fd42991b8dd542fcc37e1cbc95b2cee769abf059b538ab72` and gates
  preimage `f4bb7346af865be1876e5890d655a4cfb22762fddbec00cb7d1f440cf7f714d4`.
- Pairwise staged `os.replace`, rollback staging, delivery-directory fsync, and
  CAS preimage checks passed; rollback was not used. The 568 non-target delivery
  files remained unchanged.
- The existing SWAP and Element paragraphs compare byte-for-byte unchanged in
  both documents; the exact note occurs once in each installed document.

## Controlled production-caller render

Command:

```sh
python3 - <<'PY'
import importlib.machinery, importlib.util
loader = importlib.machinery.SourceFileLoader('delivery_build', '/home/user/timeline-hub/hub/kit/bin/delivery-build')
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec); loader.exec_module(module)
repos = []
for name in ('agent', 'runtime', 'app', 'composition'):
    repos.append({'name': name, 'tip': '0' * 40, 'base': '1' * 40, 'shortstat': '',
        'split': {'product': (0, 0, 0), 'tests': (0, 0, 0)}, 'ranged': True,
        'ahead': 0, 'applied': 0, 'status': 'PASS', 'seconds': 0,
        'applied_tree': '2' * 40, 'bundle_tree': '2' * 40, 'want_tree': '2' * 40,
        'problems': []})
rendered = module.render_readme(repos,
 '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/README.template.md',
 '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/gate-results.md')
assert all(token not in rendered for token in ('{{UTC}}', '{{REPO_SUMMARY}}', '{{REPO_SECTIONS}}', '{{GATE_RESULTS}}'))
assert rendered.count('```') % 2 == 0
assert rendered.count('`A2 D141 REG:') == 2
assert rendered.count('**SWAP.**') == 2 and rendered.count('**Element.**') == 2
print('PASS controlled production caller render_readme')
print('placeholders=0 headings=7 fence_lines=16 balanced_pairs=8 exact_note_occurrences=2')
PY
```

Result: PASS; zero placeholders, 7 headings, 16 fence lines/8 balanced pairs,
two exact-note render occurrences (README plus gate input), and unchanged SWAP /
Element paragraphs.

`git diff --no-index --check` against each byte-exact preimage returned no
diagnostics (exit 1 is the expected content-difference status). No pytest,
typecheck, lint, full suite, real build, ZIP, service, or render-body run was
performed; none is applicable to this prose-only installation.
