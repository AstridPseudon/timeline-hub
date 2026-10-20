from pathlib import Path
import difflib
import hashlib
import json
import subprocess

root = Path.cwd()
own = Path(__file__).parent
base = '78599b3809f18e9e87542d71b03b92a340e1e579'
read_base = lambda path: subprocess.check_output(['git', 'show', f'{base}:{path}'])
sha = lambda data: hashlib.sha256(data).hexdigest()
protected = json.loads((own.parent/'vw-m3-chrome155-parity-environment-prep/scope-check.json').read_text())['product_paths_unchanged']
for path, digest in protected.items():
    assert sha((root/path).read_bytes()) == digest, path
unchanged = ['playwright.viewing-parity.config.ts', 'playwright.viewing-parity.native-codec.config.ts']
unchanged += [f'tests/e2e/timeline/viewing-parity/{name}.ts' for name in ['media', 'download', 'authority', 'admission', 'bootstrap', 'browser-profile']]
unchanged += [f'tests/e2e/timeline/viewing-parity/{name}.test.ts' for name in ['download', 'diagnostics', 'compare', 'authority', 'admission', 'harness', 'bootstrap', 'browser-profile']]
for path in unchanged:
    assert (root/path).read_bytes() == read_base(path), path
# Canonical publication/readback/digest construction differs only in the authored output size.
fixture_path = 'tests/e2e/timeline/viewing-parity/fixture.ts'
fixture = (root/fixture_path).read_text()
fixture = fixture.replace("import { ORIGINAL_640, type ParityCanvas } from './canvas';\n", '')
fixture = fixture.replace('generatePlayableVideo, mediaHash, PARITY_FPS }', 'generatePlayableVideo, mediaHash, PARITY_FPS, PARITY_HEIGHT, PARITY_WIDTH }')
fixture = fixture.replace('harness: DirectHarness, canvas: ParityCanvas = ORIGINAL_640)', 'harness: DirectHarness)')
fixture = fixture.replace('`${canvas.width}x${canvas.height}`', '`${PARITY_WIDTH}x${PARITY_HEIGHT}`')
assert fixture == read_base(fixture_path).decode(), 'fixture changes exceed explicit canvas/resolution argument'
# Exact reverse of the move, indentation, explicit canvas argument and import changes.
s = (root/'tests/e2e/timeline/viewing-parity/cases.ts').read_text()
line = 'export function registerFrameParityCases(canvas: ParityCanvas = ORIGINAL_640): void {\n'
preamble, body = s.split(line)
assert body.endswith('}\n')
body = '\n'.join(text[2:] if text.startswith('  ') else text for text in body[:-2].splitlines()) + '\n'
s = preamble + body
s = s.replace("\nimport { ORIGINAL_640, readCanvasFrameMarker, type ParityCanvas } from './canvas';\n", '')
s = s.replace('\ntest.use({ parityCanvas: canvas });\n', '')
s = s.replace('canvas.width', 'PARITY_WIDTH').replace('canvas.height', 'PARITY_HEIGHT')
s = s.replace(', canvas)', ')').replace('readCanvasFrameMarker(', 'readFrameMarker(')
s = s.replace('new RegExp(`frame 52: \\\\d+/${PARITY_WIDTH * PARITY_HEIGHT} pixels exceed 2/255; max channel error=`)', r'/frame 52: \d+\/230400 pixels exceed 2\/255; max channel error=/')
s = s.replace('mediaHash, VIDEO_START_FRAME', 'mediaHash, readFrameMarker, VIDEO_START_FRAME')
s = s.replace('PARITY_FPS, PARITY_FRAMES,\n', 'PARITY_FPS, PARITY_FRAMES, PARITY_HEIGHT, PARITY_WIDTH,\n')
s = s.replace("'../../../../src/", "'../../../src/").replace("'../../local/support/", "'../local/support/")
for name in ['authority', 'admission', 'download', 'diagnostics', 'harness', 'media', 'fixture', 'frames']:
    s = s.replace(f"from './{name}'", f"from './viewing-parity/{name}'")
original = read_base('tests/e2e/timeline/player-export-frame-parity.spec.ts').decode()
if s != original:
    (own/'case-normalization.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True), s.splitlines(True))))
assert s == original, 'shared case bodies differ beyond enumerated move/canvas arguments'
report = {'base': base, 'product_paths_unchanged': protected,
          'unchanged': {path: sha((root/path).read_bytes()) for path in unchanged},
          'original_four_case_bodies_exact_after_enumerated_reverse': True,
          'fixture_exact_except_authored_output_canvas_argument': True,
          'no_proposal_helper_copies_adopted': not list((root/'tests/e2e/timeline/viewing-parity').glob('normal-profile-native1920.*'))}
assert report['no_proposal_helper_copies_adopted']
(own/'scope-check.json').write_text(json.dumps(report, indent=2) + '\n')
print('PASS: seven approved product paths, original inputs/configs/tests, exact shared case semantics')
